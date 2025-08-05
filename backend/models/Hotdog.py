"""Hotdog models and enumerations for Steve's Place.

This module defines hotdog-related classes and enumerations including
meat options, toppings, and the main Hotdog class with pricing logic.
"""

from enum import Enum
from typing import List, Optional

class HotDogMeat(Enum):
    """
    Enumeration of available hotdog meat options.
    
    Defines the different types of hotdog meat available,
    including traditional and specialty sausages.
    """
    RED = "Red (Pork & Beef)"
    RED_FOOTLONG = "Red Footlong (Pork & Beef)"
    ITALIAN_SAUSAGE = "Italian Sausage"
    BEEF = "Beef (100%)"
    BEEF_FOOTLONG = "Beef Footlong 1/3lb"
    RED_HOT_SAUSAGE = "Red Hot Sausage"
    TURKEY = "Turkey"
    SMOKED_BEEF = "Smoked Beef"
    JALAPENO = "Jalapeno"
    KIELBASA = "Kielbasa"
    SAUSAGE = "Sausage (Pork & Beef)"


HOT_DOG_PRICE_MAP = {
    HotDogMeat.RED: 3.25,
    HotDogMeat.RED_FOOTLONG: 4.25,
    HotDogMeat.ITALIAN_SAUSAGE: 4.75,
    HotDogMeat.BEEF: 3.25,
    HotDogMeat.BEEF_FOOTLONG: 6.00,
    HotDogMeat.RED_HOT_SAUSAGE: 3.50,
    HotDogMeat.TURKEY: 3.25,
    HotDogMeat.SMOKED_BEEF: 4.00,
    HotDogMeat.JALAPENO: 4.00,
    HotDogMeat.KIELBASA: 4.00,
    HotDogMeat.SAUSAGE: 4.00,
}


class HotDogTopping(Enum):
    """
    Enumeration of available hotdog toppings.
    
    Lists all condiments and toppings available for hotdogs,
    from classic condiments to specialty toppings.
    """
    MUSTARD = "Mustard"
    KETCHUP = "Ketchup"
    CHILI = "Chili"
    ONIONS = "Onions"
    SLAW = "Slaw"
    PICKLES = "Pickles"
    KRAUT = "Kraut"
    CHEESE = "Cheese"
    RELISH = "Relish"
    GRILLED_ONIONS = "Grilled Onions"
    GRILLED_PEPPERS = "Grilled Peppers"
    SPICY_MUSTARD = "Spicy Mustard"
    RED_ONION_SAUCE = "Red Onion Sauce"
    JALAPENOS = "Jalapenos"
    MAYO = "Mayo"
    HOT_CHERRY_PEPPERS = "Hot Cherry Peppers"

class Hotdog:
    """
    Represents a hotdog order with customizable meat and toppings.
    
    The Hotdog class handles hotdog customization including meat selection
    and various toppings. Pricing is based on the specific meat type
    and quantity ordered.
    
    Attributes:
        quantity (int): Number of hotdogs ordered
        dog_type (HotDogMeat): Type of hotdog meat
        toppings (List[HotDogTopping]): List of selected toppings
        special_instructions (Optional[str]): Special preparation notes
        price (float): Total price for all hotdogs
    
    Example:
        >>> hotdog = Hotdog(
        ...     quantity=2,
        ...     dog_type=HotDogMeat.BEEF,
        ...     toppings=[HotDogTopping.MUSTARD, HotDogTopping.RELISH],
        ...     special_instructions="Extra mustard"
        ... )
        >>> print(f"Price: ${hotdog.price:.2f}")
        Price: $6.50
    """
    def __init__(
        self,
        quantity: int,
        dog_type: HotDogMeat,
        toppings: Optional[List[HotDogTopping]],
        special_instructions: Optional[str],
    ):
        self.dog_type = dog_type
        self.toppings = toppings
        self.special_instructions = special_instructions
        self.quantity = quantity
        self._validate()
        self.price = HOT_DOG_PRICE_MAP[dog_type] * quantity

    def _validate(self):
        """
        Validate hotdog configuration.
        
        Ensures that the number of toppings doesn't exceed the available
        topping options and that all toppings are valid enum instances.
        
        Raises:
            ValueError: If toppings configuration is invalid
        """
        if self.toppings and len(self.toppings) > len(HotDogTopping):
            raise ValueError("Toppings must be a list of instances of HotDogTopping enum")


    def __str__(self):
        """
        Return a formatted string representation of the hotdog order.
        
        Returns:
            str: Human-readable description including quantity, meat type,
                 toppings, and any special instructions
        """
        result = (
            f"{self.quantity} X {self.dog_type.value} Hot Dog\n"
        )
        if self.toppings:
            result += f"Toppings: {', '.join(t.value for t in self.toppings)}\n"
        
        if self.special_instructions:
            result += f"Special Instructions: {self.special_instructions}\n"
        
        return result
