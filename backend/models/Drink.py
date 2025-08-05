"""Drink models and enumerations for Steve's Place.

This module defines drink-related classes and enumerations including drink sizes,
fountain drink options, bottled drink options, and the main Drink class with
pricing logic.
"""

import enum
from typing import Optional

class DrinkSize(enum.Enum):
    """
    Enumeration of available drink sizes.
    
    Defines the different sizes available for drinks, with different
    pricing for each size. Bottle size is only applicable to bottled drinks.
    
    Attributes:
        REGULAR: Standard fountain drink size
        LARGE: Large fountain drink size with premium pricing
        BOTTLE: Bottled drink size (fixed size)
    """
    REGULAR = "Regular"
    LARGE = "Large"
    BOTTLE = "Bottle"


class FountainDrink(enum.Enum):
    """
    Enumeration of available fountain drink options.
    
    Lists all the fountain drinks available at Steve's Place, including
    sodas, teas, and specialty drinks. These drinks are available in
    regular and large sizes.
    
    Attributes:
        COKE: Coca-Cola
        DIET_COKE: Diet Coca-Cola
        MOUNTAIN_DEW_YELLOW: Mountain Dew
        HI_C: Hi-C fruit punch
        ROOT_BEER: Root beer
        DR_PEPPER: Dr Pepper
        SWEET_TEA: Homemade sweet tea
        UNSWEET_TEA: Homemade unsweetened tea
        LEMONADE: Homemade lemonade
    """
    COKE = "Coke"
    DIET_COKE = "Diet Coke"
    MOUNTAIN_DEW_YELLOW = "Mountain Dew Yellow"
    HI_C = "Hi-C"
    ROOT_BEER = "Root Beer"
    DR_PEPPER = "Dr Pepper"
    SWEET_TEA = "Homemade Sweet Tea"
    UNSWEET_TEA = "Homemade Unsweet Tea"
    LEMONADE = "Homemade Lemonade"


class BottleDrink(enum.Enum):
    """
    Enumeration of available bottled drink options.
    
    Lists bottled drinks available at Steve's Place. These drinks
    come in a fixed bottle size and have different pricing from
    fountain drinks.
    
    Attributes:
        BOTTLED_SODA: Various bottled soda options
    """
    BOTTLED_SODA = "Bottled Soda"


DRINK_PRICES_MAP = {
    DrinkSize.REGULAR: 2.00,
    DrinkSize.LARGE: 2.50,
    DrinkSize.BOTTLE: 2.50
}

class Drink:
    """
    Represents a drink order with size, type, and pricing.
    
    The Drink class handles both fountain drinks (available in regular/large)
    and bottled drinks (fixed size). It validates that the correct drink type
    is used for each size and calculates pricing based on size and quantity.
    
    Attributes:
        quantity (int): Number of drinks ordered
        size (DrinkSize): Size of the drink (regular, large, or bottle)
        name (FountainDrink | BottleDrink): Specific drink selection
        special_instructions (Optional[str]): Special preparation notes
        price (float): Total price for all drinks
    
    Raises:
        ValueError: If drink type doesn't match size requirements
    
    Example:
        >>> drink = Drink(2, DrinkSize.LARGE, FountainDrink.COKE, "Extra ice")
        >>> print(f"Price: ${drink.price:.2f}")
        Price: $5.00
    """
    def __init__(
        self,
        quantity: int,
        size: DrinkSize,
        name: FountainDrink | BottleDrink,
        special_instructions: Optional[str],
    ):
        self.quantity = quantity
        self.size = size
        self.name = name
        self.special_instructions = special_instructions
        self._validate()
        self.price = DRINK_PRICES_MAP[size] * quantity
        
    def _validate(self):
        """
        Validate drink size and type compatibility.
        
        Ensures that bottled drinks use the BottleDrink enum and fountain
        drinks (regular/large) use the FountainDrink enum. This prevents
        invalid combinations like a bottled fountain drink.
        
        Raises:
            ValueError: If drink type doesn't match the size requirements
        """
        if self.size == DrinkSize.BOTTLE and not isinstance(self.name, BottleDrink):
            raise ValueError("Bottled Soda must use BottleDrink enum.")
        
        if self.size in [DrinkSize.REGULAR, DrinkSize.LARGE] and not isinstance(self.name, FountainDrink):
            raise ValueError("Regular/Large drinks must use FountainDrink enum.")
        
    def __str__(self):
        """
        Return a formatted string representation of the drink order.
        
        Returns:
            str: Human-readable description including quantity, size, drink name,
                 and any special instructions
        """
        result = (
            f"{self.quantity} X {self.size.value} {self.name.value} \n"
        )
        if self.special_instructions:
            result += f"special instructions: {self.special_instructions} \n"
        return result

