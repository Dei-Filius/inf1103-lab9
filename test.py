# Test your implementation

import importlib
from pathlib import Path
import csv

import pytest
from pytest import CaptureFixture, MonkeyPatch
from pytest_mock import MockerFixture

from discount_strategy import DiscountStrategy
from inventory import Inventory
from order import Order
from percentage_discount import PercentageDiscount
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from student_discount import StudentDiscount
from supplier import Supplier
from utils import get_positive_float_input

smart_auditor = importlib.import_module("inf1103-labs-smart-auditor")


supplier = Supplier("S009", "SK", "sk@sk.com")
product = PhysicalProduct("P009", "Thumbdrive", 100, 5, 0.1, supplier)
product_order_quantity = 1
order = Order("O001", PercentageDiscount(10))
order.add_order_line(
    product,
    product_order_quantity,
)


def test_calculates_totals_with_strategy(mocker: MockerFixture):
    """Order calculates totals through a DiscountStrategy and contains no discount if/elif logic."""
    spy = mocker.spy(PercentageDiscount, "apply")
    order.calulate_total()
    spy.assert_called()


def test_new_discount_strategy():
    """A new discount strategy can be added without changing Order."""
    arbitrary = 67.67

    class newDiscountStrat(DiscountStrategy):
        def apply(self, total: float) -> float:
            return arbitrary

    tmp_order = Order("O067", newDiscountStrat())
    tmp_order.add_order_line(
        product,
        1,
    )
    assert tmp_order.calulate_total() == arbitrary


def test_change_discount_with_setdiscount():
    """The strategy on an existing order can be changed with set_discount()."""
    order.set_discount(StudentDiscount())
    order_lines = order.order_lines
    assert len(order_lines) == 1
    assert order_lines[0].product is product
    assert order_lines[0].quantity == product_order_quantity


def test_unknown_product_raise_value_error():
    """An unknown product type raises a ValueError with a clear message."""
    with pytest.raises(ValueError, match="Unknown product type: idk"):
        _ = ProductFactory().create("idk", "P005", "P005", 1.0, 1, supplier)


@pytest.mark.parametrize(
    "type, price, stock, order_quant",
    [
        ("PHYSICAL", -1, 1, 1),
        ("PHYSICAL", 1, -1, 1),
        ("PHYSICAL", 1, 1, -1),
        ("DIGITAL", -1, 1, 1),
        ("DIGITAL", 1, -1, 1),
        ("DIGITAL", 1, 1, -1),
    ],
)
def test_invalid_prices_stock_order_quant_raise_value_error(
    type, price, stock, order_quant
):
    """Invalid prices, stock quantities and order quantities are rejected."""
    with pytest.raises(ValueError):
        _ = ProductFactory().create(type, "P005", "P005", price, stock, supplier)
        tmp_order = Order("O001")
        tmp_order.add_order_line(product, order_quant)


@pytest.mark.parametrize(
    "user_inputs, expects",
    [
        (["", "25"], ["Please enter a valid number, e.g. 12.50", "25.0"]),
        (["one", "25"], ["Please enter a valid number, e.g. 12.50", "25.0"]),
        (["-1", "25"], ["Please enter a number greater than zero.", "25.0"]),
    ],
)
def test_user_input_validation_(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
    user_inputs: list[str],
    expects: list[str],
):
    """Invalid user input is handled without crashing, and the user is asked again."""
    iter_user_inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(iter_user_inputs))
    print(get_positive_float_input(""))
    lines = capsys.readouterr().out.splitlines()
    assert lines == expects


def test_missing_products_csv(capsys: CaptureFixture[str]):
    """A missing products file is handled gracefully."""
    fake_file = Path("./") / "nonexistent_csv.csv"
    smart_auditor.load_inventory(fake_file, Inventory(), supplier)
    capture = capsys.readouterr().out.splitlines()[-1]
    assert capture == f"Products file not found: {smart_auditor.INVENTORY_FILE_PATH}"


def test_skip_invalid_row(monkeypatch: MonkeyPatch):
    """Bad rows in the products file are reported and skipped, and valid rows still load."""
    monkeypatch.setattr(
        "csv.DictReader",
        lambda _: [
            {
                "product_type": "PHYSICAL",
                "product_id": "P01",
                "name": "P01",
                "price": 1,
                "stock_quantity": 1,
            },
            {},
        ],
    )
