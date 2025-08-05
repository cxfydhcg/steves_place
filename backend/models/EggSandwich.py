"""Egg sandwich models and enumerations for Steve's Place.

This module defines egg sandwich-related classes and enumerations including
egg preparation styles, bread options, meats, cheeses, toppings, add-ons,
and the main EggSandwich class with pricing logic.
"""

from enum import Enum
from typing import List, Optional

class Egg(Enum):
    """
    Enumeration of egg preparation styles.
    
    Defines the different ways eggs can be prepared for egg sandwiches,
    including fried, scrambled, or no egg options.
    
    Attributes:
        FRIED: Fried egg
        SCRAMBLED: Scrambled egg
        NO_EGG: No egg option
    """
    FRIED = "Fried Egg"
    SCRAMBLED = "Scrambled Egg"
    NO_EGG = "No Egg"
    


class EggSandwichBread(Enum):
    """
    Enumeration of available bread options for egg sandwiches.
    
    Lists all bread types available for egg sandwiches, from traditional
    sliced breads to specialty options like croissants and kaiser rolls.
    
    Attributes:
        WHITE: White bread
        WHEAT: Wheat bread
        RYE: Rye bread
        KAISER_ROLL: Kaiser roll
        CROISSANT: Croissant with upcharge
    """
    WHITE = "White"
    WHEAT = "Wheat"
    RYE = "Rye"
    KAISER_ROLL = "Kaiser Roll"
    CROISSANT = "Croissant +$0.75"  # +$0.75


class EggSandwichMeat(Enum):
    """
    Enumeration of available meat options for egg sandwiches.
    
    Lists all meat options that can be added to egg sandwiches,
    including breakfast meats and specialty options.
    
    Attributes:
        PORK_ROLL: Pork roll
        HAM: Ham slices
        BACON: Bacon strips
        SAUSAGE: Breakfast sausage
        TURKEY_SAUSAGE: Turkey sausage
        COUNTRY_HAM: Country ham
        TURKEY_BACON: Turkey bacon
    """
    PORK_ROLL = "Pork Roll"
    HAM = "Ham"
    BACON = "Bacon"
    SAUSAGE = "Sausage"
    TURKEY_SAUSAGE = "Turkey Sausage"
    COUNTRY_HAM = "Country Ham"
    TURKEY_BACON = "Turkey Bacon"


class EggSandwichCheese(Enum):
    """
    Enumeration of available cheese options for egg sandwiches.
    
    Lists all cheese varieties available for egg sandwiches,
    from mild to sharp flavors.
    
    Attributes:
        AMERICAN: American cheese
        SWISS: Swiss cheese
        PROVOLONE: Provolone cheese
        PEPPER_JACK: Pepper jack cheese
    """
    AMERICAN = "American"
    SWISS = "Swiss"
    PROVOLONE = "Provolone"
    PEPPER_JACK = "Pepper Jack"

class EggSandwichToppings(Enum):
    """
    Enumeration of available toppings for egg sandwiches.
    
    Lists all condiment and seasoning options available for
    egg sandwiches.
    
    Attributes:
        MAYO: Mayonnaise
        SALT: Salt seasoning
        PEPPER: Pepper seasoning
        KETCHUP: Ketchup condiment
    """
    MAYO = "Mayo"
    SALT = "Salt"
    PEPPER = "Pepper"
    KETCHUP = "Ketchup"

class EggSandwichAddOns(Enum):
    """
    Enumeration of premium add-ons for egg sandwiches.
    
    Lists premium additions that incur extra charges,
    such as hashbrowns and extra portions of meat, egg, or cheese.
    
    Attributes:
        HASHBROWN: Hashbrown on sandwich (1 piece)
        HASHBROWN_ONSIDE: Hashbrown on side (2 pieces)
        MEAT: Additional meat portion
        EGG: Additional egg
        CHEESE: Additional cheese
    """
    HASHBROWN = "Hashbrown on it (1 Piece)"
    HASHBROWN_ONSIDE = "Hashbrown on Side (2 Piece)"
    MEAT = "Meat"
    EGG = "Egg"
    CHEESE = "Cheese"



EGG_SANDWICH_ADD_ONS_PRICE_MAP = {
    EggSandwichAddOns.MEAT: 1.50,
    EggSandwichAddOns.HASHBROWN: 0.75,
    EggSandwichAddOns.HASHBROWN_ONSIDE: 1.50,
    EggSandwichAddOns.EGG: 0.75,
    EggSandwichAddOns.CHEESE: 0.75,
}




CROISSANT_UPCHARGE = 0.75


class EggSandwich:
    """
    Represents an egg sandwich order with customizable options and pricing.
    
    The EggSandwich class handles all aspects of egg sandwich customization
    including egg preparation, bread selection, meats, cheeses, toppings,
    and premium add-ons. It calculates pricing based on base price plus
    any premium add-ons and croissant upcharge.
    
    Attributes:
        quantity (int): Number of sandwiches ordered
        bread (EggSandwichBread): Bread type
        egg (Egg): Egg preparation style
        toasted (Optional[bool]): Whether bread should be toasted
        grilled (Optional[bool]): Whether sandwich should be grilled
        meat (Optional[EggSandwichMeat]): Meat selection
        cheese (Optional[EggSandwichCheese]): Cheese selection
        toppings (Optional[List[EggSandwichToppings]]): List of toppings
        special_instructions (Optional[str]): Special preparation notes
        add_ons (Optional[List[EggSandwichAddOns]]): List of premium add-ons
        price (float): Total price for all sandwiches
    
    Example:
        >>> sandwich = EggSandwich(
        ...     quantity=1,
        ...     bread=EggSandwichBread.WHITE,
        ...     egg=Egg.SCRAMBLED,
        ...     toasted=True,
        ...     grilled=False,
        ...     meat=EggSandwichMeat.BACON,
        ...     cheese=EggSandwichCheese.AMERICAN,
        ...     toppings=[EggSandwichToppings.SALT],
        ...     special_instructions=None,
        ...     add_ons=[EggSandwichAddOns.HASHBROWN]
        ... )
        >>> print(f"Price: ${sandwich.price:.2f}")
    """
    def __init__(
        self,
        quantity: int,
        bread: EggSandwichBread,
        egg: Egg,
        toasted: Optional[bool],
        grilled: Optional[bool],
        meat: Optional[EggSandwichMeat],
        cheese: Optional[EggSandwichCheese],
        toppings: Optional[List[EggSandwichToppings]],
        special_instructions: Optional[str],
        add_ons: Optional[List[EggSandwichAddOns]],
    ):
        self.egg = egg
        self.bread = bread
        self.toasted = toasted
        self.grilled = grilled
        self.meat = meat
        self.cheese = cheese
        self.toppings = toppings
        self.special_instructions = special_instructions
        self.add_ons = add_ons
        self.quantity = quantity
        self._validate()
        self.price = self._calculate_price()

    def _validate(self):
        """
        Validate egg sandwich configuration.
        
        Ensures that the sandwich has either egg or meat specified,
        and validates that toppings and add-ons lists don't exceed
        the available enum options.
        
        Raises:
            ValueError: If egg and meat are both missing, or if toppings
                       or add-ons lists are invalid
        """

        if not self.egg and not self.meat:
            raise ValueError("Egg or meat must be specified")
        
        if self.toppings and len(self.toppings) > len(EggSandwichToppings):
            raise ValueError("Toppings must be a list of instances of EggSandwichToppings enum")

        if self.add_ons and len(self.add_ons) > len(EggSandwichAddOns):
            raise ValueError("Add-ons must be a list of instances of EggSandwichAddOns enum")

    def _calculate_price(self) -> float:
        """
        Calculate the total price for the egg sandwich order.
        
        Calculates price based on base sandwich price (different for
        meat vs no-meat sandwiches), croissant upcharge if applicable,
        and any premium add-ons, multiplied by quantity.
        
        Returns:
            float: Total price for all sandwiches in the order, rounded to 2 decimal places
        """
        price = 0.0
        if not self.meat:
            price += 3.50
        else:
            price += 5.25

        if self.bread == EggSandwichBread.CROISSANT:
            price += CROISSANT_UPCHARGE
        
        if self.add_ons:
            for add_on in self.add_ons:
                price += EGG_SANDWICH_ADD_ONS_PRICE_MAP[add_on]
        return round(price * self.quantity, 2)

    def __str__(self):
        """
        Return a formatted string representation of the egg sandwich order.
        
        Returns:
            str: Human-readable description including quantity, bread type,
                 toasted/grilled options, egg style, meat, cheese, toppings,
                 add-ons, and any special instructions
        """
        result = (
            f"{self.quantity} X {self.bread.value} Egg Sandwich\n"
        )
        if self.toasted:
            result += "Toasted: Yes\n"
        if self.grilled:
            result += "Grilled: Yes\n"
        if self.egg:
            result += f"Egg: {self.egg.value}\n"
        if self.meat:
            result += f"Meat: {self.meat.value}\n"
        if self.cheese:
            result += f"Cheese: {self.cheese.value}\n"
        if self.toppings:
            result += f"Toppings: {', '.join(t.value for t in self.toppings)}\n"
        if self.add_ons:
            result += f"Add-ons: {', '.join(a.value for a in self.add_ons)}\n"
        if self.special_instructions:
            result += f"Special Instructions: {self.special_instructions}\n"

