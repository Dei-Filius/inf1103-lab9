from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier
from utils import (
    get_email_input,
    get_int_input,
    get_float_input,
    get_str_input,
)


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float | None = None,
        download_size: int | None = None,
    ) -> Product:
        match product_type:
            case "PHYSICAL":
                if weight is None:
                    raise ValueError("Product type is PHYSICAL, but no weight given.")
                return PhysicalProduct(
                    product_id, name, price, stock_quantity, weight, supplier
                )
            case "DIGITAL":
                if download_size is None:
                    raise ValueError(
                        "Product type is DIGITAL, but no download size given."
                    )
                return DigitalProduct(
                    product_id, name, price, stock_quantity, download_size, supplier
                )
            case _:
                raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def create_from_input() -> Product:
        print()
        print("Add New Product")

        product_type = get_str_input("Product Type: ").strip()
        product_id = get_str_input("Product ID (Pxxx): ").strip()
        name = get_str_input("Product Name: ").strip()
        price = get_float_input("Price (omit $ sign): ")
        stock = get_int_input("Stock Quantity: ", 0)
        supplier_id = get_str_input("Supplier ID (Sxxx): ").strip()
        supplier_name = get_str_input("Supplier Name: ")
        supplier_contact_email = get_email_input("Supplier Contact Email: ")

        supplier = Supplier(supplier_id, supplier_name, supplier_contact_email)

        match product_type:
            case "PHYSICAL":
                weight = get_int_input("Product Weight(kg): ", 0)
                return PhysicalProduct(product_id, name, price, stock, weight, supplier)
            case "DIGITAL":
                download_size = get_int_input("Product Downlaod Size(MB): ", 0)
                return DigitalProduct(
                    product_id, name, price, stock, download_size, supplier
                )
            case _:
                raise ValueError(f"Unknown product type: {product_type}")
