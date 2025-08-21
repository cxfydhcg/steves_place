import pytest
from models.Sandwich import (
    Sandwich, SandwichSize, SandwichBread, SandwichMeat, SandwichCheese,
    SandwichToppings, SandwichAddOns, SANDWICH_PRICE_MAP, SANDWICH_ADD_ONS_PRICE_MAP,
    STANDARD_SANDWICH_PRICE_REGULAR, STANDARD_SANDWICH_PRICE_LARGE
)
from models.Schema import SandwichSchema
from pydantic import ValidationError


class TestSandwichValidCases:
    """Test cases for Sandwich model - valid cases with price testing."""
    def test_price_field(self):
        """Test that the price field is correctly calculated."""
        assert SANDWICH_PRICE_MAP == {
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

        assert SANDWICH_ADD_ONS_PRICE_MAP == {
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
    def test_sandwich_valid_case(self):
        """Test that the sandwich model is valid with valid data."""
        quantity = 2
        sandwich_schema = SandwichSchema(
            quantity=quantity,
            size=SandwichSize.REGULAR,
            bread=SandwichBread.WHITE,
            meat=SandwichMeat.CHICKEN_SALAD,
            toast=True,
            grilled=True,
            cheese=SandwichCheese.AMERICAN,
            toppings=[SandwichToppings.MAYO, SandwichToppings.ONIONS],
            special_instructions="Add extra cheese",
            add_ons=[SandwichAddOns.BACON, SandwichAddOns.MEAT],
        )
        sandwich = Sandwich(**sandwich_schema.model_dump())
        assert sandwich.quantity == quantity
        assert SandwichToppings.MAYO in sandwich.toppings
        assert SandwichToppings.ONIONS in sandwich.toppings
        assert SandwichAddOns.BACON in sandwich.add_ons
        assert SandwichAddOns.MEAT in sandwich.add_ons
        add_on_price = sum(SANDWICH_ADD_ONS_PRICE_MAP[item][sandwich.size] for item in sandwich.add_ons)
        assert sandwich.price == (SANDWICH_PRICE_MAP[SandwichMeat.CHICKEN_SALAD][SandwichSize.REGULAR] + add_on_price) * quantity

        

    def test_sandwich_valid_case_large(self):
        """Test that the sandwich model is valid with valid data."""
        quantity = 2
        sandwich_schema = SandwichSchema(
            quantity=quantity,
            size=SandwichSize.LARGE,
            bread=SandwichBread.WHITE,
            meat=SandwichMeat.CHICKEN_SALAD,
            toast=True,
            grilled=True,
            cheese=SandwichCheese.AMERICAN,
            toppings=[SandwichToppings.MAYO, SandwichToppings.ONIONS, SandwichToppings.MAYO],
            special_instructions="Add extra cheese",
            add_ons=[SandwichAddOns.BACON, SandwichAddOns.MEAT],
        )
        sandwich = Sandwich(**sandwich_schema.model_dump())
        assert sandwich.quantity == quantity
        assert SandwichToppings.MAYO in sandwich.toppings
        assert SandwichToppings.ONIONS in sandwich.toppings
        assert len(sandwich.toppings) == 2
        assert SandwichAddOns.BACON in sandwich.add_ons
        assert SandwichAddOns.MEAT in sandwich.add_ons
        add_on_price = sum(SANDWICH_ADD_ONS_PRICE_MAP[item][sandwich.size] for item in sandwich.add_ons)
        assert sandwich.price == (SANDWICH_PRICE_MAP[SandwichMeat.CHICKEN_SALAD][SandwichSize.LARGE] + add_on_price) * quantity
    def test_sandwich_valid_case_no_extra(self):
        """Test that the sandwich model is valid with no toppings."""
        quantity = 2
        sandwich_schema = SandwichSchema(
            quantity=quantity,
            size=SandwichSize.REGULAR,
            bread=SandwichBread.WHITE,
            meat=SandwichMeat.CHICKEN_SALAD,
        )
        sandwich = Sandwich(**sandwich_schema.model_dump())

        add_on_price = sum(SANDWICH_ADD_ONS_PRICE_MAP[item][sandwich.size] for item in sandwich.add_ons)
        assert sandwich.price == (SANDWICH_PRICE_MAP[SandwichMeat.CHICKEN_SALAD][SandwichSize.REGULAR] + add_on_price) * quantity


class TestSandwichInvalidCases:
    """Test cases for Sandwich model - invalid cases."""
    def test_invalid_sandwich_quantity(self):
        """Test that the sandwich model is invalid with an invalid quantity."""
        with pytest.raises(ValidationError):
            SandwichSchema(
                quantity=0,
                size=SandwichSize.REGULAR,
                bread=SandwichBread.WHITE,
                meat=SandwichMeat.CHICKEN_SALAD,
                cheese=SandwichCheese.AMERICAN,
                toppings=[SandwichToppings.MAYO, SandwichToppings.ONIONS],
                special_instructions="Add extra cheese",
                add_ons=[SandwichAddOns.BACON, SandwichAddOns.MEAT],
            )
    

    def test_invalid_sandwich_add_ons(self):
        """Test that the sandwich model is invalid with an invalid add-on."""
        with pytest.raises(ValueError):
            sandwich_schema = SandwichSchema(
                quantity=2,
                size=SandwichSize.REGULAR,
                bread=SandwichBread.WHITE,
                meat=SandwichMeat.CHICKEN_SALAD,
                toppings=[SandwichToppings.MAYO, SandwichToppings.ONIONS],
                add_ons=[SandwichAddOns.CHEESE],
            )
            sandwich = Sandwich(**sandwich_schema.model_dump())
