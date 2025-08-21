"""Order model for Steve's Place.

This module defines the Order class which manages collections of food items
and calculates totals including fees for complete customer orders.
"""

from typing import List, Union
from .Sandwich import Sandwich
from .Drink import Drink
from .Combo import Combo
from .Hotdog import Hotdog
from .Side import Side
from .EggSandwich import EggSandwich

class Order:
    """
    Represents a complete customer order containing multiple food items.
    
    The Order class manages a collection of food items and provides
    functionality to calculate totals, add items, and apply fees.
    It supports all food item types available at Steve's Place.
    
    Attributes:
        items (List[Union[Sandwich, Drink, Combo, Hotdog, Side, EggSandwich]]):
            List of food items in the order
    
    Example:
        >>> order = Order()
        >>> order.add_item(hotdog)
        >>> order.add_item(drink)
        >>> print(f"Total: ${order.total_price():.2f}")
        Total: $7.50
        >>> print(f"With fee: ${order.total_price_with_fee():.2f}")
        With fee: $7.80
    """
    def __init__(self):
        self.items: List[Union[Sandwich, Drink, Combo, Hotdog, Side, EggSandwich]] = []
        
    def add_item(self, item: Union[Sandwich, Drink, Combo, Hotdog, Side, EggSandwich]):
        """
        Add a food item to the order.
        
        Args:
            item: Any food item instance (Sandwich, Drink, Combo, Hotdog, 
                  Side, or EggSandwich) to add to the order
        """
        self.items.append(item)
    
    def total_price(self) -> float:
        """
        Calculate the total price of all items in the order.
        
        Returns:
            float: Sum of all item prices, rounded to 2 decimal places
        """
        return round(sum(item.price for item in self.items), 2)

    def total_price_with_fee(self) -> float:
        """
        Calculate the total price including a 4% processing fee.
        
        Applies a 4% fee to the total order price, typically used
        for payment processing or service charges.
        
        Returns:
            float: Total price plus 4% fee, rounded to 2 decimal places
        """
        return round(self.total_price() * 1.04, 2)

    def __str__(self):
        """
        Return a formatted string representation of the complete order.
        
        Returns:
            str: Human-readable order summary including all items and total price
        """
        result = ["🧾 Order Summary:"]
        for idx, item in enumerate(self.items, 1):
            result.append(f"{idx}. {item.__class__.__name__}: {item}")
        result.append(f"💰 Total: ${self.total_price():.2f}")
        return "\n".join(result)
