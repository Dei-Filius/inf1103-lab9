import json
from datetime import datetime
from pathlib import Path

from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier
from utils import (
    get_int_input,
    get_product_id_input,
)

INVENTORY_FILE_PATH: str = "data/inventory.json"
inventory_file: Path = Path(INVENTORY_FILE_PATH)


def load_inventory() -> Inventory:
    print()
    print("Loading inventory...")
    inventory = Inventory()
    try:
        with inventory_file.open("r") as file:
            for product_info in json.load(file):
                product_info: dict
                supplier_info = product_info["supplier"]
                supplier = Supplier(
                    supplier_info["id"],
                    supplier_info["name"],
                    supplier_info["contact_email"],
                )
                product = ProductFactory().create(
                    product_info["type"],
                    product_info["id"],
                    product_info["name"],
                    product_info["price"],
                    product_info["stock"],
                    supplier,
                    weight=product_info.get("weight"),
                    download_size=product_info.get("download_size"),
                )
                inventory.add_product(product)
    except FileNotFoundError:
        inventory_file.parent.mkdir(parents=True, exist_ok=True)
        inventory_file.touch()
    except (json.JSONDecodeError, ValueError) as err:
        print("Inventory file might be corrupted.")
        print(f"Error Msg: {err}")
        print("Exiting...")
        exit()
    return inventory


def save_inventory(inventory: Inventory) -> None:
    print()
    print("Saving inventory...")
    with inventory_file.open("w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    print("Inventory saved successfully to", INVENTORY_FILE_PATH)


def add_product(inventory: Inventory) -> None:
    product = ProductFactory.create_from_input()
    if inventory.find_product(product.product_id):
        print("Product already exists.")
        return
    
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print()
    print("Update Stock")
    product_id = get_product_id_input()
    product = inventory.find_product(product_id)

    if product is None:
        print("This Product is not in Inventory.")
        return

    print("Product Found!")
    print("------------------------------------------------")
    product.display_information()
    print("------------------------------------------------")

    stock = get_int_input("New Stock Quantity: ", 0)
    product.update_stock(stock)

    print()
    print("Product Updated!")
    print("------------------------------------------------")
    product.display_information()
    print("------------------------------------------------")


def find_product(inventory: Inventory) -> Product | None:
    print()
    product_id = get_product_id_input()
    product = inventory.find_product(product_id)
    if product is None:
        print("This Product is not in Inventory.")
        return None

    print("Product Found!")
    print("------------------------------------------------")
    product.display_information()
    print("------------------------------------------------")
    return product


def calculate_order(inventory: Inventory) -> None:
    order_id = f"O{int(datetime.now().timestamp())}"
    order = Order(order_id)
    print("Ctrl+C to stop adding to order.")
    try:
        while True:
            product = find_product(inventory)
            if product is not None:
                quantity = get_int_input("Quantity: ", 1)
                order.add_order_line(product, quantity)
                print("Added!")
    except KeyboardInterrupt:
        pass
    print()
    order.display()


def exit_app(inventory: Inventory):
    save_inventory(inventory)
    print()
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")
    exit()


def main() -> None:
    try:
        inventory: Inventory = load_inventory()

        menu: list[dict] = [
            {"text": "Exit", "action": lambda: exit_app(inventory)},
            {"text": "Display All Products", "action": lambda: inventory.display_all()},
            {"text": "Add Product", "action": lambda: add_product(inventory)},
            {"text": "Update Stock", "action": lambda: update_stock(inventory)},
            {"text": "Search Product", "action": lambda: find_product(inventory)},
            {"text": "Save Inventory", "action": lambda: save_inventory(inventory)},
            {"text": "Order Calculator", "action": lambda: calculate_order(inventory)},
        ]

        print("""
========================================
INVENTORY MANAGEMENT SYSTEM
========================================
        """)
        while True:
            try:
                display_menu(menu)
                option = get_int_input("Enter option: ", 0, len(menu) - 1)
                try:
                    menu[option]["action"]()
                except KeyboardInterrupt:
                    continue
            except KeyboardInterrupt:
                exit_app(inventory)
                break

    except json.decoder.JSONDecodeError:
        print(f"Error decoding json file {INVENTORY_FILE_PATH}")
        print("Exiting...")
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
