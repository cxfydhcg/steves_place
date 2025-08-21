"""Salad models and enumerations for Steve's Place.

This module defines salad-related classes and enumerations including
salad types, toppings, dressings, add-ons, and the main Salad class
with pricing logic.
"""

from enum import Enum
from typing import List, Optional


class SaladChoice(Enum):
    """
    Enumeration of available salad base options.
    
    Defines the different types of salad bases available,
    each with its own characteristic ingredients and style.
    
    Attributes:
        CHEF_HAM_TURKEY: Chef salad with ham and turkey
        CHEF_CHICKEN: Chef salad with chicken salad
        CHEF_TUNA: Chef salad with tuna salad
        GARDEN: Garden salad with vegetables only
    """
    CHEF_HAM_TURKEY = "Chef Salad - Ham & Turkey"
    CHEF_CHICKEN = "Chef Salad - Chicken Salad"
    CHEF_TUNA = "Chef Salad - Tuna Salad"
    GARDEN = "Garden Salad (veggies only)"


class SaladTopping(Enum):
    """
    Enumeration of available salad toppings.
    
    Lists all vegetable toppings and garnishes available for salads,
    from classic additions like lettuce to various cheeses and seasonings.
    
    Attributes:
        LETTUCE: Fresh lettuce
        BACON: Crispy bacon pieces
        TOMATO: Fresh tomato slices
        CUCUMBER: Cucumber slices
        ONIONS: Sliced onions
        OLIVES: Mixed olives
        EGGS: Hard boiled eggs
        GREEN_PEPPERS: Green bell pepper slices
        BANANA_PEPPERS: Banana pepper rings
        JALAPENOS: Jalapeno pepper slices
        SALT_PEPPER: Salt and pepper seasoning
        OREGANO: Oregano seasoning
        OIL_VINEGAR: Oil and vinegar dressing
        PICKLES: Pickle slices
        AMERICAN_CHEESE: American cheese
        PROVOLONE_CHEESE: Provolone cheese
        SWISS_CHEESE: Swiss cheese
    """
    LETTUCE = "Lettuce"
    BACON = "Bacon"
    TOMATO = "Tomato"
    CUCUMBER = "Cucumber"
    ONIONS = "Onions"
    OLIVES = "Olives"
    EGGS = "Eggs"
    GREEN_PEPPERS = "Green Peppers"
    BANANA_PEPPERS = "Banana Peppers"
    JALAPENOS = "Jalapenos Peppers"
    SALT_PEPPER = "Salt & Pepper"
    OREGANO = "Oregano"
    OIL_VINEGAR = "Oil & Vinegar"
    PICKLES = "Pickles"
    AMERICAN_CHEESE = "American Cheese"
    PROVOLONE_CHEESE = "Provolone Cheese"
    SWISS_CHEESE = "Swiss Cheese"


class SaladDressing(Enum):
    """
    Enumeration of available salad dressings.
    
    Lists all dressing options available for salads,
    from creamy to vinaigrette styles.
    
    Attributes:
        RANCH: Ranch dressing
        ITALIAN: Italian vinaigrette
        FRENCH: French dressing
        THOUSAND_ISLAND: Thousand Island dressing
        HONEY_MUSTARD: Honey mustard dressing
    """
    RANCH = "Ranch"
    ITALIAN = "Italian"
    FRENCH = "French"
    THOUSAND_ISLAND = "Thousand Island"
    HONEY_MUSTARD = "Honey Mustard"

class SaladAddOns(Enum):
    """
    Enumeration of premium add-ons for salads.
    
    Lists premium additions that incur extra charges,
    perfect for making salads more substantial meals.
    
    Attributes:
        CHEESE: Extra cheese
        EGGS: Extra eggs
        MEAT: Extra meat
        DRESSING: Extra dressing
    """
    CHEESE = "Cheese"
    EGGS = "Eggs"
    MEAT = "Meat"
    DRESSING = "Dressing"

SALAD_ADD_ONS_PRICE_MAP = {
    SaladAddOns.CHEESE: 0.75,
    SaladAddOns.EGGS: 1.00,
    SaladAddOns.MEAT: 2.00,
    SaladAddOns.DRESSING: 0.75,
}

# 💵 Price map
SALAD_PRICE_MAP = {
    SaladChoice.GARDEN: 7.50,
    SaladChoice.CHEF_HAM_TURKEY: 9.50,
    SaladChoice.CHEF_CHICKEN: 9.50,
    SaladChoice.CHEF_TUNA: 9.50,
}

class Salad:
    """
    Represents a salad order with customizable options and pricing.
    
    The Salad class handles all aspects of salad customization including
    base salad selection, toppings, dressings, and premium add-ons.
    It calculates pricing based on base price plus any premium add-ons.
    
    Attributes:
        quantity (int): Number of salads ordered
        choice (SaladChoice): Base salad type
        toppings (List[SaladTopping]): List of selected toppings
        dressing (Optional[SaladDressing]): Selected dressing
        add_ons (Optional[List[SaladAddOns]]): List of premium add-ons
        special_instructions (Optional[str]): Special preparation notes
        price (float): Total price for all salads
    
    Example:
        >>> salad = Salad(
        ...     quantity=1,
        ...     choice=SaladChoice.CHEF_CHICKEN,
        ...     toppings=[SaladTopping.LETTUCE, SaladTopping.TOMATO],
        ...     dressing=SaladDressing.RANCH,
        ...     add_ons=[SaladAddOns.CHEESE],
        ...     special_instructions="Extra dressing on the side"
        ... )
        >>> print(f"Price: ${salad.price:.2f}")
        Price: $10.25
    """
    def __init__(
        self,
        quantity: int,
        choice: SaladChoice,
        toppings: List[SaladTopping],
        dressing: Optional[SaladDressing],
        special_instructions: Optional[str],
        add_ons: Optional[List[SaladAddOns]],
    ):
        self.choice = choice
        self.toppings = list(set(toppings))
        self.dressing = dressing
        self.special_instructions = special_instructions
        self.add_ons = list(set(add_ons))
        self.quantity = quantity
        self._validate()
        self.price = self._calculate_price()

    def _validate(self):
        """
        Validate salad configuration.
        
        Performs validation checks to ensure the salad configuration
        is valid, including checking for invalid toppings and add-ons
        combinations, especially for Garden Salad restrictions.
        
        Raises:
            ValueError: if meat items are added to Garden Salad
        """

        if self.choice == SaladChoice.GARDEN:
            if SaladTopping.BACON in self.toppings:
                raise ValueError("Bacon is not allowed on Garden Salad")
            if SaladAddOns.MEAT in self.add_ons:
                raise ValueError("Meat is not allowed on Garden Salad")
            
        if SaladAddOns.DRESSING in self.add_ons and not self.dressing:
            raise ValueError("Dressing is required on Garden Salad")
        
        if SaladAddOns.EGGS in self.add_ons and SaladTopping.EGGS not in self.toppings:
            raise ValueError("Eggs are required in the toppings to add Eggs")

        if SaladAddOns.CHEESE in self.add_ons and not any(
            t in self.toppings for t in [
                SaladTopping.AMERICAN_CHEESE,
                SaladTopping.PROVOLONE_CHEESE,
                SaladTopping.SWISS_CHEESE,
            ]
        ):
            raise ValueError("Cheese is required in the toppings to add Cheese")



    def _calculate_price(self):
        """
        Calculate the total price for the salad order.
        
        Calculates price based on base salad price plus any premium
        add-ons, multiplied by quantity. Regular toppings and dressings
        are included in the base price.
        
        Returns:
            float: Total price for all salads in the order, rounded to 2 decimal places
        """
        price = SALAD_PRICE_MAP[self.choice]
        for add_on in self.add_ons:
            price += SALAD_ADD_ONS_PRICE_MAP[add_on]
        return round(price * self.quantity, 2)
    def __str__(self):
        """
        Return a formatted string representation of the salad order.
        
        Returns:
            str: Human-readable description including quantity, salad type,
                 toppings, dressing, add-ons, and any special instructions
        """
        result = (
            f"{self.quantity} X {self.choice.value} Salad\n"
            f"Toppings: {', '.join(t.value for t in self.toppings)}\n"
        )
        if self.dressing:
            result += f"Dressing: {self.dressing.value}\n"
        if self.special_instructions:
            result += f"Special Instructions: {self.special_instructions}\n"
        if self.add_ons:
            result += f"Add-ons: {', '.join(a.value for a in self.add_ons)}\n"
        return result
