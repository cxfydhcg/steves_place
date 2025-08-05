"""Side item models and enumerations for Steve's Place.

This module defines side item-related classes and enumerations including
side sizes, chip flavors, side names, and the main Side class with
pricing logic.
"""

import enum
from typing import Optional

class SideSize(enum.Enum):
    """
    Enumeration of available side item sizes.
    
    Defines the different sizes available for side items,
    with different pricing for each size.
    
    Attributes:
        REGULAR: Standard side item size
        LARGE: Large side item with premium pricing
    """
    REGULAR = "Regular"
    LARGE = "Large"


class Chips(enum.Enum):
    """
    Enumeration of available chip flavors.
    
    Lists all chip flavor options available as side items,
    from classic plain to specialty flavored varieties.
    
    Attributes:
        LAYS_PLAIN: Plain Lays potato chips
        LAYS_BBQ: BBQ flavored Lays chips
        JALAPENO_KETTLE_CHIPS: Spicy jalapeno kettle chips
        SOUR_CREAM_ONION_KETTLE_CHIPS: Sour cream and onion kettle chips
        SALT_VINEGAR_KETTLE_CHIPS: Salt and vinegar kettle chips
        COOKIES: Cookie option
    """
    LAYS_PLAIN = "Lays Plain"
    LAYS_BBQ = "Lays BBQ"
    JALAPENO_KETTLE_CHIPS = "Jalapeno Kettle Chips"
    SOUR_CREAM_ONION_KETTLE_CHIPS = "Sour Cream N' Onion Kettle Chips"
    SALT_VINEGAR_KETTLE_CHIPS = "Salt N' Vinegar Kettle Chips"
    COOKIES = "Cookies"


class SideName(enum.Enum):
    """
    Enumeration of available side item types.
    
    Lists all side item options available at Steve's Place,
    from fried items to cold salads.
    
    Attributes:
        CHIPS: Potato chips (various flavors)
        SLAW: Coleslaw salad
        POTATO_SALAD: Potato salad
        MACARONI_SALAD: Macaroni salad
        DEVILED_EGG: Deviled eggs
        FRENCH_FRIES: French fries
        TUNA_SALAD: Tuna salad
        CHICKEN_SALAD: Chicken salad
        CHEESE_FRIES: Cheese-topped fries
        CHILLI_CHEESE_FRIES: Chili and cheese-topped fries
    """
    CHIPS = "Chips"
    SLAW = "Slaw"
    POTATO_SALAD = "Potato Salad"
    MACARONI_SALAD = "Macaroni Salad"
    DEVILED_EGG = "Deviled Egg"
    FRENCH_FRIES = "French Fries"
    TUNA_SALAD = "Tuna Salad"
    CHICKEN_SALAD = "Chicken Salad"
    CHEESE_FRIES = "Cheese Fries"
    CHILLI_CHEESE_FRIES = "Chilli Cheese Fries"


# Price configuration
SIDE_PRICES_MAP = {
    SideName.CHIPS: 1.75,  # Same price for all chips
    SideName.SLAW: {
        SideSize.REGULAR: 3.00,
        SideSize.LARGE: 5.75
    },
    SideName.POTATO_SALAD: {
        SideSize.REGULAR: 3.00,
        SideSize.LARGE: 5.75
    },
    SideName.MACARONI_SALAD: {
        SideSize.REGULAR: 3.00,
        SideSize.LARGE: 5.75
    },
    SideName.DEVILED_EGG: {
        SideSize.REGULAR: 3.00,
        SideSize.LARGE: 5.75
    },
    SideName.TUNA_SALAD: {
        SideSize.REGULAR: 4.00,
        SideSize.LARGE: 8.75
    },
    SideName.CHICKEN_SALAD: {
        SideSize.REGULAR: 4.00,
        SideSize.LARGE: 8.75
    },
    SideName.FRENCH_FRIES: {
        SideSize.REGULAR: 2.75,
        SideSize.LARGE: 3.50
    },
    SideName.CHEESE_FRIES: {
        SideSize.REGULAR: 3.25,
        SideSize.LARGE: 3.75
    },
    SideName.CHILLI_CHEESE_FRIES: {
        SideSize.REGULAR: 3.75,
        SideSize.LARGE: 4.25
    }
}


class Side:
    """
    Represents a side item order with customizable options and pricing.
    
    The Side class handles side item customization including size selection,
    side type, and chip flavor selection for chip orders. It calculates
    pricing based on side type and size, with chip flavor included at no
    extra charge.
    
    Attributes:
        quantity (int): Number of side items ordered
        name (SideName): Type of side item
        size (Optional[SideSize]): Size of the side item
        chips_type (Optional[Chips]): Chip flavor (only for chip orders)
        special_instructions (Optional[str]): Special preparation notes
        price (float): Total price for all side items
    
    Example:
        >>> side = Side(
        ...     quantity=2,
        ...     name=SideName.CHIPS,
        ...     size=None,
        ...     chips_type=Chips.LAYS_BBQ,
        ...     special_instructions="Extra crispy"
        ... )
        >>> print(f"Price: ${side.price:.2f}")
        Price: $3.50
    """
    def _validate(self):
        """
        Validate side item configuration.
        
        Ensures that chip orders specify a flavor and non-chip orders
        have proper size specifications. This prevents invalid
        combinations like unsized salads or flavorless chips.
        
        Raises:
            ValueError: If chips don't have a flavor specified, or if
                       non-chip items don't have size specified
        """
        if self.name == SideName.CHIPS and (self.chips_type is None or self.chips_type not in Chips):
            raise ValueError("Chips type must be specified for chips")
        elif self.name != SideName.CHIPS and (self.size is None or self.size not in SideSize):
            raise ValueError("Size must be specified for non-chips sides")
            
    def __init__(
        self,
        quantity: int,
        name: SideName,
        size: Optional[SideSize],
        chips_type: Optional[Chips],
        special_instructions: Optional[str]
    ):
        """
        Initialize a side item order.
        
        Args:
            quantity (int): Number of side items to order
            name (SideName): Type of side item
            size (Optional[SideSize]): Size for non-chip items
            chips_type (Optional[Chips]): Chip flavor for chip orders
            special_instructions (Optional[str]): Special preparation notes
        
        Raises:
            ValueError: If configuration is invalid (e.g., chips without flavor)
        """
        self.name = name
        self.size = size
        self.chips_type = chips_type
        self.special_instructions = special_instructions
        self.quantity = quantity
        self._validate()
        self.price = self._calculate_price()

    def _calculate_price(self) -> float:
        """
        Calculate the total price for the side item order.
        
        Calculates price based on side item type and size (for non-chips),
        multiplied by quantity. Chip flavors are included in the base price
        at no extra charge.
        
        Returns:
            float: Total price for all side items in the order
        """
        if self.name == SideName.CHIPS:
            return SIDE_PRICES_MAP[self.name] * self.quantity
        if self.size in SIDE_PRICES_MAP[self.name]:
            return SIDE_PRICES_MAP[self.name][self.size] * self.quantity

    def __str__(self):
        """
        Return a formatted string representation of the side item order.
        
        Returns:
            str: Human-readable description including quantity, side name,
                 chip flavor or size (as applicable), and any special instructions
        """
        result = f"{self.quantity} X {self.name.value}\n"
        if self.chips_type:
            result += f" {self.chips_type.value}\n"
        else:
            result += f"Size: {self.size.value}\n"
        if self.special_instructions:
            result += f" ({self.special_instructions})\n"
        return result
