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


def get_positive_float_input(msg: str) -> float:
    """
    Get valid float from user
    """
    while True:
        try:
            user_input = round(float(input(msg)), 2)
            if user_input < 0:
                print("Please enter a number greater than zero.")
                continue
            return user_input
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


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


def display_menu(menu: list[dict]) -> None:
    print()
    print("----------- MENU -----------")
    for i, page in enumerate(menu, 0):
        print(f"{i}. {page["text"]}")
    print("----------------------------")
