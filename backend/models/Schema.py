"""Pydantic schemas for API request/response validation in Steve's Place.

This module defines Pydantic BaseModel schemas for all food items,
providing data validation and serialization for API endpoints.
Each schema corresponds to a food item model and defines the expected
structure for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from .Side import SideName, SideSize, Chips
from .Drink import DrinkSize, FountainDrink, BottleDrink
from .Hotdog import HotDogMeat, HotDogTopping
from .Salad import SaladChoice, SaladTopping, SaladDressing, SaladAddOns
from .Sandwich import SandwichSize, SandwichBread, SandwichMeat, SandwichCheese, SandwichToppings, SandwichAddOns
from .EggSandwich import Egg, EggSandwichBread, EggSandwichMeat, EggSandwichCheese, EggSandwichToppings, EggSandwichAddOns

quantity_field: int = Field(ge=1, description="Quantity must be at least 1")

special_instructions_field: Optional[str] = Field(default=None, max_length=200, description="Special instructions for the order")


class HotdogSchema(BaseModel):
    """
    Pydantic schema for hotdog API requests and responses.
    
    Validates hotdog data structure including quantity, meat type,
    toppings, and special instructions. Used for API serialization
    and deserialization of hotdog orders.
    
    Attributes:
        quantity (int): Number of hotdogs ordered
        dog_type (HotDogMeat): Type of hotdog meat
        toppings (List[HotDogTopping]): List of selected toppings
        special_instructions (Optional[str]): Special preparation notes
    
    Example:
        >>> hotdog_data = {
        ...     "quantity": 2,
        ...     "dog_type": "BEEF",
        ...     "toppings": ["MUSTARD", "RELISH"],
        ...     "special_instructions": "Extra mustard"
        ... }
        >>> hotdog = HotdogSchema(**hotdog_data)
    """
    quantity: int = quantity_field
    dog_type: HotDogMeat
    toppings: Optional[List[HotDogTopping]] = None
    special_instructions: Optional[str] = special_instructions_field

class SaladSchema(BaseModel):
    """
    Pydantic schema for salad API requests and responses.
    
    Validates salad data structure including quantity, base salad choice,
    toppings, dressing, add-ons, and special instructions.
    
    Attributes:
        quantity (int): Number of salads ordered
        choice (SaladChoice): Base salad type
        toppings (List[SaladTopping]): List of selected toppings
        dressing (Optional[SaladDressing]): Selected dressing
        add_ons (Optional[List[SaladAddOns]]): List of premium add-ons
        special_instructions (Optional[str]): Special preparation notes
    """
    quantity: int = quantity_field
    choice: SaladChoice
    toppings: List[SaladTopping]
    dressing: Optional[SaladDressing] = None
    special_instructions: Optional[str] = special_instructions_field
    add_ons: Optional[List[SaladAddOns]] = None

class SandwichSchema(BaseModel):
    """
    Pydantic schema for sandwich API requests and responses.
    
    Validates sandwich data structure including quantity, size, bread,
    meat, preparation options, cheese, toppings, and add-ons.
    
    Attributes:
        quantity (int): Number of sandwiches ordered
        size (SandwichSize): Size of the sandwich
        bread (SandwichBread): Bread type
        meat (SandwichMeat): Meat selection
        toast (Optional[bool]): Whether to toast the sandwich
        grilled (Optional[bool]): Whether to grill the sandwich
        cheese (Optional[SandwichCheese]): Cheese selection
        toppings (Optional[List[SandwichToppings]]): List of toppings
        special_instructions (Optional[str]): Special preparation notes
        is_pick_two (Optional[bool]): Whether this is a pick two sandwich
        pick_two_meats (Optional[List[SandwichMeat]]): Meats for pick two
        add_ons (Optional[List[SandwichAddOns]]): List of premium add-ons
    """
    quantity: int = quantity_field
    size: SandwichSize
    bread: SandwichBread
    meat: SandwichMeat
    toast: Optional[bool] = None
    grilled: Optional[bool] = None
    cheese: Optional[SandwichCheese] = None
    toppings: Optional[List[SandwichToppings]] = None
    special_instructions: Optional[str] = special_instructions_field
    is_pick_two: Optional[bool] = None
    pick_two_meats: Optional[List[SandwichMeat]] = None
    add_ons: Optional[List[SandwichAddOns]] = None

class SideSchema(BaseModel):
    """
    Pydantic schema for side item API requests and responses.
    
    Validates side item data structure including quantity, name,
    size, chips type, and special instructions.
    
    Attributes:
        quantity (int): Number of side items ordered
        name (SideName): Name of the side item
        size (SideSize): Size of the side item
        chips_type (Optional[Chips]): Type of chips
        special_instructions (Optional[str]): Special preparation notes
    """
    quantity: int = quantity_field
    name: SideName
    size: SideSize = SideSize.REGULAR
    chips_type: Optional[Chips] = None
    special_instructions: Optional[str] = special_instructions_field

class DrinkSchema(BaseModel):
    """
    Pydantic schema for drink API requests and responses.
    
    Validates drink data structure including quantity, size,
    drink name (fountain or bottle), and special instructions.
    
    Attributes:
        quantity (int): Number of drinks ordered
        size (DrinkSize): Size of the drink
        name (FountainDrink | BottleDrink): Drink selection
        special_instructions (Optional[str]): Special preparation notes
    """
    quantity: int = quantity_field
    size: DrinkSize
    name: FountainDrink | BottleDrink
    special_instructions: Optional[str] = special_instructions_field

class ComboSideSchema(BaseModel):
    """
    Pydantic schema for combo side item API requests and responses.
    
    Validates side item data structure for combo meals.
    
    Attributes:
        quantity (int): is by default 1
        name (SideName): Name of the side item
        size (SideSize): is by default regular
        chips_type (Optional[Chips]): Type of chips
        special_instructions (str): is by default to None
    """
    quantity: Literal[1] = Field(default=1, description="Quantity should be at combo level")
    name: SideName
    size: SideSize = SideSize.REGULAR
    chips_type: Optional[Chips] = None
    special_instructions: Literal[None] = Field(default=None, description="Description should be at combo level")





class ComboDrinkSchema(BaseModel):
    """
    Pydantic schema for combo drink API requests and responses.
    
    Validates drink data structure for combo meals.
    
    Attributes:
        quantity (int): is by default 1
        name (FountainDrink | BottleDrink): Drink selection
        size (DrinkSize): Size of the drink
        special_instructions (str): is by default to None

    """
    quantity: Literal[1] = Field(default=1, description="Quantity should be at combo level")

    name: FountainDrink | BottleDrink
    size: DrinkSize
    special_instructions: Literal[None] = Field(default=None, description="Description should be at combo level")



class ComboSchema(BaseModel):
    """
    Pydantic schema for combo meal API requests and responses.
    
    Validates combo meal data structure including quantity,
    side item, drink, and special instructions.
    
    Attributes:
        quantity (int): Number of combo meals ordered
        side (ComboSideSchema): Side item component
        drink (ComboDrinkSchema): Drink component
        special_instructions (Optional[str]): Special preparation notes
    """
    quantity: int = quantity_field
    side: ComboSideSchema
    drink: ComboDrinkSchema
    special_instructions: Optional[str] = special_instructions_field

class EggSandwichSchema(BaseModel):
    """
    Pydantic schema for egg sandwich API requests and responses.
    
    Validates egg sandwich data structure including quantity, bread,
    egg preparation, toasting/grilling options, meat, cheese, toppings,
    and add-ons.
    
    Attributes:
        quantity (int): Number of egg sandwiches ordered
        bread (EggSandwichBread): Bread type
        egg (Egg): Egg preparation style
        toasted (Optional[bool]): Whether to toast the bread
        grilled (Optional[bool]): Whether to grill the sandwich
        meat (Optional[EggSandwichMeat]): Meat selection
        cheese (Optional[EggSandwichCheese]): Cheese selection
        toppings (Optional[List[EggSandwichToppings]]): List of toppings
        special_instructions (Optional[str]): Special preparation notes
        add_ons (Optional[List[EggSandwichAddOns]]): List of premium add-ons
    """
    quantity: int = quantity_field
    bread: EggSandwichBread
    egg: Egg
    toasted: Optional[bool] = None
    grilled: Optional[bool] = None
    meat: Optional[EggSandwichMeat] = None
    cheese: Optional[EggSandwichCheese] = None
    toppings: Optional[List[EggSandwichToppings]] = None
    special_instructions: Optional[str] = special_instructions_field
    add_ons: Optional[List[EggSandwichAddOns]] = None
