"""Food category enumeration for Steve's Place menu system.

This module defines the main food categories available in the restaurant's
menu system. These categories are used throughout the application for
organizing menu items and routing API requests.
"""

import enum


class Category(enum.Enum):
    """
    Enumeration of food categories available in Steve's Place menu.
    
    This enum defines all the main food categories that customers can order from.
    Each category corresponds to a specific type of food item with its own
    customization options and pricing structure.
    
    Attributes:
        HOTDOG: Hot dogs with various meat types and toppings
        SANDWICH: Cold and hot sandwiches with customizable ingredients
        EGGSANDWICH: Breakfast sandwiches with eggs, meats, and toppings
        SALAD: Fresh salads with various toppings and dressings
        SIDE: Side items including chips, fries, and salads
        DRINK: Beverages including fountain drinks and bottled options
        COMBO: Combination meals with main item, side, and drink
    
    Example:
        >>> category = Category.SANDWICH
        >>> print(category.value)
        'Sandwich'
    """
    HOTDOG = "Hotdog"
    SANDWICH = "Sandwich"
    EGGSANDWICH = "EggSandwich"
    SALAD = "Salad"
    SIDE = "Side"
    DRINK = "Drink"
    COMBO = "Combo"

