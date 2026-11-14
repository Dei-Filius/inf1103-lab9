from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, quantity_requirement: int, int_percent_off: int) -> None:
        if quantity_requirement < 0:
            raise ValueError()
        if not (0 <= int_percent_off <= 100):
            raise ValueError()
        self.__multiplier: float = 1 - int_percent_off / 100

    def apply(self, total: float) -> float:
        return total * self.__multiplier
