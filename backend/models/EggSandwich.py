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
        self._egg = egg
        self._bread = bread
        self._toasted = toasted
        self._grilled = grilled
        self._meat = meat
        self._cheese = cheese
        self._toppings = list(set(toppings))
        self._special_instructions = special_instructions
        self._add_ons = list(set(add_ons))
        self._quantity = quantity
        self._validate()
        self._price = self._calculate_price()

    def _validate(self):
        """
        Validate egg sandwich configuration.
        
        Ensures that the sandwich has valid combinations of ingredients by checking:
        - At least egg or meat must be specified
        - Number of toppings cannot exceed available options
        - Number of add-ons cannot exceed available options  
        - Cannot add extra egg/cheese/meat as add-ons if base ingredient not selected
        
        Raises:
            ValueError: If validation fails for any of the following:
                - Both egg and meat are missing
                - Toppings list exceeds available enum options
                - Add-ons list exceeds available enum options
                - Extra egg selected without base egg
                - Extra cheese selected without base cheese
                - Extra meat selected without base meat
        """
    
        if self.egg == Egg.NO_EGG and not self.meat:
            raise ValueError("Egg or meat must be specified")

        if self.egg == Egg.NO_EGG and EggSandwichAddOns.EGG in self.add_ons:
            raise ValueError("Can not have egg in add-ons if no egg is specified")

        
        if not self.cheese and EggSandwichAddOns.CHEESE in self.add_ons:
            raise ValueError("Can not have cheese in add-ons if no cheese is specified")
        
        if not self.meat and EggSandwichAddOns.MEAT in self.add_ons:
            raise ValueError("Can not have meat in add-ons if no meat is specified")



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
    @property
    def quantity(self):
        return self._quantity
    @property
    def bread(self):
        return self._bread
    @property
    def egg(self):
        return self._egg
    @property
    def toasted(self):
        return self._toasted
    @property
    def grilled(self):
        return self._grilled
    @property
    def meat(self):
        return self._meat
    @property
    def cheese(self):
        return self._cheese
    @property
    def toppings(self):
        return self._toppings
    @property
    def special_instructions(self):
        return self._special_instructions
    @property
    def add_ons(self):
        return self._add_ons
    @property
    def price(self):
        return self._price

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

