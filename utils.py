from typing import Literal
import re


def get_str_input(msg: str) -> str:
    """
    Get non-empty string from user
    """
    while True:
        user_input = input(msg)
        if user_input:
            return user_input
        print("Invalid. Input is empty. Try again.")


def get_int_input(msg: str, minimum=None, maximum=None) -> int:
    """
    get int from user within min max value.
    """
    while True:
        try:
            user_input = int(input(msg))
            if minimum is not None:
                if user_input < minimum:
                    raise ValueError()
            if maximum is not None:
                if user_input > maximum:
                    raise ValueError()
            return user_input
        except ValueError:
            print("Invalid. Try again.")


def get_price_input(msg: str) -> float:
    """
    Get valid price from user, price >=0
    """
    while True:
        try:
            user_input = round(float(input(msg)), 2)
            if user_input < 0:
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid. Try again.")


def get_product_id_input() -> str:
    """
    Get valid Product ID from user, starts with P then followed by digits.
    """
    while True:
        try:
            user_input = input("Product ID (Pxxx): ").strip().upper()
            if not (user_input.startswith("P") or user_input[1:].isdigit()):
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid Product ID. Try again.")


def get_supplier_id_input() -> str:
    """
    Get valid Supplier ID from user, starts with S then followed by digits.
    """
    while True:
        try:
            user_input = input("Supplier ID (Sxxx): ").strip().upper()
            if not (user_input.startswith("S") or user_input[1:].isdigit()):
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid Supplier ID. Try again.")


def get_email_input(msg: str) -> str:
    """
    Get valid email
    """
    while True:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        email = input(msg).strip().upper()
        if re.fullmatch(pattern, email) is None:
            print("Invalid email")
        else:
            return email


def get_product_type_input() -> Literal["PHYSICAL", "DIGITAL"]:
    """
    Get valid Product type from user.
    """
    while True:
        try:
            user_input = input("Product Type: ").strip().upper()
            if user_input not in ["PHYSICAL", "DIGITAL"]:
                raise ValueError()
            return user_input
        except ValueError:
            print("Invalid Product ID. Try again.")


def display_menu(menu: list[dict]) -> None:
    print()
    print("----------- MENU -----------")
    for i, page in enumerate(menu, 0):
        print(f"{i}. {page["text"]}")
    print("----------------------------")
