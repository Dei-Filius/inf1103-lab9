from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    def __init__(self) -> None:
        self.__multiplier = 0.95

    def apply(self, total: float) -> float:
        return total * self.__multiplier
