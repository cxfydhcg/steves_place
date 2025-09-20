"""Sandwich models and enumerations for Steve's Place.

This module defines sandwich-related classes and enumerations including
sizes, bread options, meats, cheeses, toppings, add-ons, and the main
Sandwich class with complex pricing logic.
"""

from enum import Enum
from typing import List, Optional


class SandwichSize(Enum):
    """
    Enumeration of available sandwich sizes.
    
    Defines the different sizes available for sandwiches, each with
    different pricing structures and portion sizes.
    
    Attributes:
        REGULAR: Standard sandwich size
        LARGE: Large sandwich with premium pricing
    """
    REGULAR = "Regular"
    LARGE = "Large"


class SandwichBread(Enum):
    """
    Enumeration of available bread options for sandwiches.
    
    Lists all bread types available for sandwiches, from traditional
    sliced breads to specialty rolls.
    
    Attributes:
        WHITE: White bread
        WHEAT: Wheat bread
        RYE: Rye bread
        KAISER_ROLL: Kaiser roll
    """
    WHITE = "White"
    WHEAT = "Wheat"
    RYE = "Rye"
    KAISER_ROLL = "Kaiser Roll"


class SandwichMeat(Enum):
    """
    Enumeration of available meat options for sandwiches.
    
    Lists all meat and protein options available for sandwiches,
    including deli meats, salads, and specialty preparations.
    
    Attributes:
        CHICKEN_SALAD: Chicken salad mixture
        TUNA_SALAD: Tuna salad mixture
        FRIED_BOLOGNA: Fried bologna
        EGG_SALAD: Egg salad mixture
        PIMENTO_CHEESE: Pimento cheese spread
        GRILLED_CHEESE: Grilled cheese sandwich
        BLT: Bacon, lettuce, and tomato
        TURKEY: Sliced turkey
        ROAST_BEEF: Sliced roast beef
        CORNED_BEEF_REUBEN: Corned beef reuben
        HAM: Sliced ham
        BUFFALO_CHICKEN_BREAST: Buffalo chicken breast
        HOT_PASTRAMI: Hot pastrami
        HOT_CORNER_BEEF: Hot corned beef
        HALF_TURKEY_HALF_HAM: Half Turkey Half Ham
        HALF_HOT_PASTRAMI_HALF_CORNED_BEEF: Half Hot Pastrami Half Corned Beef
    """
    CHICKEN_SALAD = "Chicken Salad"
    TUNA_SALAD = "Tuna Salad"
    FRIED_BOLOGNA = "Fried Bologna"
    EGG_SALAD = "Egg Salad"
    PIMENTO_CHEESE = "Pimento Cheese"
    GRILLED_CHEESE = "Grilled Cheese"
    BLT = "BLT"
    TURKEY = "Turkey"
    ROAST_BEEF = "Roast Beef"
    CORNED_BEEF_REUBEN = "Corned Beef Reuben"
    HAM = "Ham"
    BUFFALO_CHICKEN_BREAST = "Buffalo Chicken Breast"
    HOT_PASTRAMI = "Hot Pastrami"
    HOT_CORNED_BEEF = "Hot Corned Beef"
    HALF_TURKEY_HALF_HAM = "Half Turkey Half Ham"
    HALF_HOT_PASTRAMI_HALF_CORNED_BEEF = "Half Hot Pastrami Half Corned Beef"


class SandwichCheese(Enum):
    """
    Enumeration of available cheese options for sandwiches.
    
    Lists all cheese varieties available for sandwiches,
    from mild to sharp flavors.
    
    Attributes:
        AMERICAN: American
        PROVOLONE: Provolone
        SWISS: Swiss
        PEPPER_JACK: Pepper Jack
    """
    AMERICAN = "American"
    PROVOLONE = "Provolone"
    SWISS = "Swiss"
    PEPPER_JACK = "Pepper Jack"


class SandwichToppings(Enum):
    """
    Enumeration of available toppings for sandwiches.
    
    Lists all vegetable toppings, condiments, and garnishes available
    for sandwiches, from basic lettuce and tomato to specialty items.
    
    Attributes:
        MAYO: Mayo
        TOMATO: Tomato
        LETTUCE: Lettuce
        ONIONS: Onions
        PICKLES: Pickles
        SALT: Salt
        PEPPER: Pepper
        OREGANO: Oregano
        THOUSAND_ISLAND: Thousand Island
        GRILLED_ONIONS: Grilled Onions
        GRILLED_PEPPERS: Grilled Peppers
        SPICY_MUSTARD: Spicy Mustard
        MUSTARD: Mustard
        BANANA_PEPPERS: Banana Peppers
        JALAPENO_PEPPERS: Jalapeno Peppers
        OLIVES: Olives
        OIL: Oil
        VINEGAR: Vinegar
        KRAUT: Kraut
    """
    MAYO = "Mayo"
    TOMATO = "Tomato"
    LETTUCE = "Lettuce"
    ONIONS = "Onions"
    PICKLES = "Pickles"
    SALT = "Salt"
    PEPPER = "Pepper"
    OREGANO = "Oregano"
    THOUSAND_ISLAND = "Thousand Island"
    GRILLED_ONIONS = "Grilled Onions"
    GRILLED_PEPPERS = "Grilled Peppers"

    SPICY_MUSTARD = "Spicy Mustard"
    MUSTARD = "Mustard"
    BANANA_PEPPERS = "Banana Peppers"
    JALAPENO_PEPPERS = "Jalapeno Peppers"
    OLIVES = "Olives"
    OIL = "Oil"
    VINEGAR = "Vinegar"
    KRAUT = "Kraut"

class SandwichAddOns(Enum):
    """
    Enumeration of premium add-ons for sandwiches.
    
    Lists premium additions that incur extra charges,
    such as bacon and extra portions.
    
    Attributes:
        BACON: Crispy bacon strips
        MEAT: Additional meat portion
        CHEESE: Additional cheese portion
    """
    BACON = "Bacon"
    MEAT = "Meat"
    CHEESE = "Cheese"


STANDARD_SANDWICH_PRICE_REGULAR = 7.00
STANDARD_SANDWICH_PRICE_LARGE = 8.50

SANDWICH_PRICE_MAP = {
    # Special sandwiches
    SandwichMeat.EGG_SALAD: {SandwichSize.REGULAR: 5.50, SandwichSize.LARGE: 6.75},
    SandwichMeat.PIMENTO_CHEESE: {SandwichSize.REGULAR: 5.25, SandwichSize.LARGE: 6.50},
    SandwichMeat.GRILLED_CHEESE: {SandwichSize.REGULAR: 4.00, SandwichSize.LARGE: 5.00},
    SandwichMeat.BLT: {SandwichSize.REGULAR: 6.75, SandwichSize.LARGE: 8.25},

    # Standard sandwiches (same price)
    SandwichMeat.CHICKEN_SALAD: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.TUNA_SALAD: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.FRIED_BOLOGNA: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.TURKEY: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.ROAST_BEEF: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.CORNED_BEEF_REUBEN: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.HAM: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.BUFFALO_CHICKEN_BREAST: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.HOT_PASTRAMI: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.HOT_CORNED_BEEF: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.HALF_TURKEY_HALF_HAM: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
    SandwichMeat.HALF_HOT_PASTRAMI_HALF_CORNED_BEEF: {SandwichSize.REGULAR: STANDARD_SANDWICH_PRICE_REGULAR, SandwichSize.LARGE: STANDARD_SANDWICH_PRICE_LARGE},
}



SANDWICH_ADD_ONS_PRICE_MAP = {
    SandwichAddOns.BACON: {
        SandwichSize.REGULAR: 2.00,
        SandwichSize.LARGE: 2.50
    },

    SandwichAddOns.MEAT: {
        SandwichSize.REGULAR: 2.00,
        SandwichSize.LARGE: 2.50
    },
    SandwichAddOns.CHEESE: {
        SandwichSize.REGULAR: 0.75,
        SandwichSize.LARGE: 0.75
    },
}

class Sandwich:
    """
    Represents a sandwich order with customizable options and complex pricing.
    
    The Sandwich class handles all aspects of sandwich customization including
    size selection, bread choice, meat, cheese, toppings, and premium add-ons.
    
    Attributes:
        quantity (int): Number of sandwiches ordered
        size (SandwichSize): Size of the sandwich (regular or large)
        bread (SandwichBread): Bread type
        meat (SandwichMeat): Meat selection
        toast (bool): Whether to toast the sandwich
        grilled (bool): Whether to grill the sandwich
        cheese (Optional[SandwichCheese]): Cheese selection
        toppings (Optional[List[SandwichToppings]]): List of vegetable toppings and condiments
        special_instructions (Optional[str]): Special preparation notes
        add_ons (Optional[List[SandwichAddOns]]): List of premium add-ons
        price (float): Total price for all sandwiches
    
    Example:
        >>> sandwich = Sandwich(
        ...     quantity=1,
        ...     size=SandwichSize.REGULAR,
        ...     bread=SandwichBread.WHEAT,
        ...     meat=SandwichMeat.TURKEY,
        ...     toast=True,
        ...     grilled=False,
        ...     cheese=SandwichCheese.SWISS,
        ...     toppings=[SandwichToppings.LETTUCE, SandwichToppings.TOMATO],
        ...     special_instructions="Light mayo",
        ...     add_ons=[SandwichAddOns.BACON]
        ... )
        >>> print(f"Price: ${sandwich.price:.2f}")
        Price: $9.50
    """
    def __init__(
        self,
        quantity: int,
        size: SandwichSize,
        bread: SandwichBread,
        meat: SandwichMeat,
        toast: bool,
        grilled: bool,
        cheese: Optional[SandwichCheese],
        toppings: Optional[List[SandwichToppings]],
        special_instructions: Optional[str],
        add_ons: Optional[List[SandwichAddOns]],
    ):

        self._size = size
        self._bread = bread
        self._toast = toast
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
        Validate sandwich configuration.

        Validates that the sandwich configuration is valid, including
        checking that cheese is specified when adding cheese add-on.



        Raises:
            ValueError: If no cheese is specified when adding cheese add-on.
        """


        if SandwichAddOns.CHEESE in self.add_ons and self.cheese is None:
            raise ValueError("Cheese is required when adding cheese add-on.")


    def _calculate_price(self) -> float:
        """
        Calculate the total price for the sandwich order.
        
        Calculates price based on sandwich size and meat type, with special
        handling for "Pick Two" half-sandwiches. Adds premium add-on costs
        and multiplies by quantity. Regular toppings are included in base price.
        
        Returns:
            float: Total price for all sandwiches in the order, rounded to 2 decimal places
        """

        base_price = SANDWICH_PRICE_MAP[self.meat][self.size]

        if self.add_ons:
            for add_on in self.add_ons:
                base_price += SANDWICH_ADD_ONS_PRICE_MAP[add_on][self.size]

        return round(base_price * self.quantity, 2)
    # Read-only properties
    @property
    def quantity(self):
        return self._quantity
    @property
    def size(self):
        return self._size
    @property
    def bread(self):
        return self._bread
    @property
    def meat(self):
        return self._meat
    @property
    def toast(self):
        return self._toast
    @property
    def grilled(self):
        return self._grilled
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
        Return a formatted string representation of the sandwich order.
        
        Returns:
            str: Human-readable description including quantity, size, meat, bread,
                 preparation options, cheese, toppings, add-ons, and any special instructions
        """
        meat_info = f"Meat: {self.meat.value}"
        result = (
            f"{self.quantity} X {self.size.value} {meat_info} Sandwich\n"
            f"  Bread: {self.bread.value}\n"
        )
        if self.toast:
            result += f"  Toast: Yes\n"
        if self.grilled:
            result += f"  Grilled: Yes\n"
        if self.cheese:
            result += f"  Cheese: {self.cheese.value}\n"
        if self.toppings:
            result += f"  Toppings: {', '.join(t.value for t in self.toppings)}\n"
        if self.add_ons:
            result += f"  Add Ons: {', '.join(a.value for a in self.add_ons)}\n"
        if self.special_instructions:
            result += f"  Special Instructions: {self.special_instructions}\n"
        return result