"""Combo meal model for Steve's Place.

This module defines the Combo class which represents combination meals
that include a side item and a drink at a discounted price. Combos have
specific restrictions on side sizes and types.
"""

from typing import Optional
from .Side import Side, SideSize, SideName
from .Drink import Drink, DrinkSize

COMBO_BASE_PRICE = 4.25
DRINK_UPGRADE_COST = 0.50

class Combo:
    """
    Represents a combination meal with a side and drink.
    
    A combo meal offers a discounted price for ordering a side item and drink
    together. Combos have restrictions: only regular-sized sides are allowed,
    and premium sides (chicken salad, tuna salad) are excluded. Large drinks
    and bottled drinks incur an upgrade cost.
    
    Attributes:
        side (Side): The side item included in the combo
        drink (Drink): The drink included in the combo
        special_instructions (Optional[str]): Special preparation instructions
        quantity (int): Number of combo meals ordered
        price (float): Total price for the combo meals
    
    Raises:
        ValueError: If side is not regular size or is a premium side
    
    Example:
        >>> side = Side(1, SideName.FRENCH_FRIES, SideSize.REGULAR, None, None)
        >>> drink = Drink(1, DrinkSize.REGULAR, FountainDrink.COKE, None)
        >>> combo = Combo(2, side, drink, "Extra napkins")
    """
    def __init__(
        self,
        quantity: int,
        side: Side,
        drink: Drink,
        special_instructions: Optional[str],
    ):
        self.side = side
        self.drink = drink
        self.special_instructions = special_instructions
        self.quantity = quantity
        self._validate()
        self.price = self._calculate_price()

    def _validate(self):
        """
        Validate combo meal restrictions.
        
        Ensures that the combo meets the restaurant's requirements:
        - Only regular-sized sides are allowed
        - Premium sides (chicken salad, tuna salad) are excluded
        
        Raises:
            ValueError: If side size is not regular or side is premium
        """
        if self.side.size != SideSize.REGULAR:
            raise ValueError("Combo includes only regular size sides.")

        if self.side.name == SideName.CHICKEN_SALAD \
            or self.side.name == SideName.TUNA_SALAD \
            or self.side.name == SideName.CHEESE_FRIES \
            or self.side.name == SideName.CHILLI_CHEESE_FRIES:
            raise ValueError("Combo does not include chicken salad, tuna salad, cheese fries, or chilli cheese fries.")
    def _calculate_price(self) -> float:
        """
        Calculate the total price for the combo meal.
        
        Starts with the base combo price and adds upgrade costs for large
        or bottled drinks. The price is calculated per combo and then
        multiplied by quantity.
        
        Returns:
            float: Total price for all combo meals, rounded to 2 decimal places
        """
        price = COMBO_BASE_PRICE
        if self.drink.size in [DrinkSize.LARGE, DrinkSize.BOTTLE]:
            price += DRINK_UPGRADE_COST
        return round(price, 2)

    def __str__(self):
        """
        Return a formatted string representation of the combo meal.
        
        Returns:
            str: Human-readable description of the combo including quantity,
                 side details, drink details, and any special instructions
        """
        result = (
            f"{self.quantity} X Combo:\n"
            f"  Side: ({self.side.size.value}) {self.side.name.value}\n"
            f"  Drink: ({self.drink.size.value}) {self.drink.name.value}\n"
        )
        if self.special_instructions:
            result += f"special instructions: {self.special_instructions} \n"
        return result
