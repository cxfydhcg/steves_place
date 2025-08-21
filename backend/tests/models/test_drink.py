import pytest
from models.Drink import Drink, DrinkSize, FountainDrink, BottleDrink, DRINK_PRICES_MAP
from models.Schema import DrinkSchema
from pydantic import ValidationError

class TestDrinkValidCases:
    """Test cases for Drink model - valid cases with price testing."""
    def test_price_field(self):
        """Test price field in Drink model."""
        assert DRINK_PRICES_MAP == {
            DrinkSize.REGULAR: 2.00,
            DrinkSize.LARGE: 2.50,
            DrinkSize.BOTTLE: 2.50
        }
    
    def test_drink_valid_case_regular(self):
        """Test valid case for regular drink."""
        quantity = 1
        drink_schema = DrinkSchema(quantity=quantity, size=DrinkSize.REGULAR, name=FountainDrink.COKE)
        drink = Drink(**drink_schema.model_dump())
        assert drink.quantity == quantity
        assert drink.size == DrinkSize.REGULAR
        assert drink.name == FountainDrink.COKE
        assert drink.price == DRINK_PRICES_MAP[DrinkSize.REGULAR] * quantity
        assert drink.special_instructions == None

        quantity = 2
        drink_schema = DrinkSchema(quantity=quantity, size=DrinkSize.REGULAR, name=FountainDrink.COKE, special_instructions="Extra syrup")
        drink = Drink(**drink_schema.model_dump())
        assert drink.quantity == quantity
        assert drink.size == DrinkSize.REGULAR
        assert drink.name == FountainDrink.COKE
        assert drink.price == DRINK_PRICES_MAP[DrinkSize.REGULAR] * quantity
        assert drink.special_instructions == "Extra syrup"

    def test_drink_valid_case_large(self):
        """Test valid case for large drink."""
        quantity = 1
        drink_schema = DrinkSchema(quantity=quantity, size=DrinkSize.LARGE, name=FountainDrink.COKE)
        drink = Drink(**drink_schema.model_dump())
        assert drink.quantity == quantity
        assert drink.size == DrinkSize.LARGE
        assert drink.name == FountainDrink.COKE
        assert drink.price == DRINK_PRICES_MAP[DrinkSize.LARGE] * quantity
        assert drink.special_instructions == None

        quantity = 2
        drink_schema = DrinkSchema(quantity=quantity, size=DrinkSize.LARGE, name=FountainDrink.COKE, special_instructions="Extra syrup")
        drink = Drink(**drink_schema.model_dump())
        assert drink.quantity == quantity
        assert drink.size == DrinkSize.LARGE
        assert drink.name == FountainDrink.COKE
        assert drink.price == DRINK_PRICES_MAP[DrinkSize.LARGE] * quantity
        assert drink.special_instructions == "Extra syrup"

    def test_drink_valid_case_bottle(self):
        """Test valid case for bottle drink."""
        quantity = 1
        drink_schema = DrinkSchema(quantity=quantity, size=DrinkSize.BOTTLE, name=BottleDrink.BOTTLED_SODA)
        drink = Drink(**drink_schema.model_dump())
        assert drink.quantity == quantity
        assert drink.size == DrinkSize.BOTTLE
        assert drink.name == BottleDrink.BOTTLED_SODA
        assert drink.price == DRINK_PRICES_MAP[DrinkSize.BOTTLE] * quantity
        assert drink.special_instructions == None

        quantity = 2
        drink_schema = DrinkSchema(quantity=quantity, size=DrinkSize.BOTTLE, name=BottleDrink.BOTTLED_SODA, special_instructions="Extra syrup")
        drink = Drink(**drink_schema.model_dump())
        assert drink.quantity == quantity
        assert drink.size == DrinkSize.BOTTLE
        assert drink.name == BottleDrink.BOTTLED_SODA
        assert drink.price == DRINK_PRICES_MAP[DrinkSize.BOTTLE] * quantity
        assert drink.special_instructions == "Extra syrup"


class TestDrinkInvalidCases:
    """Test cases for Drink model - invalid cases."""

    def test_drink_invalid_quantity(self):
        """Test invalid case for quantity."""
        with pytest.raises(ValidationError):
            DrinkSchema(quantity=0, size=DrinkSize.REGULAR, name=FountainDrink.COKE)

    def test_drink_invalid_case_size(self):
        """Test invalid case for size."""
        with pytest.raises(ValidationError):
            DrinkSchema(quantity=1, size="INVALID", name=FountainDrink.COKE)
            
    def test_drink_invalid_case_name(self):
        """Test invalid case for name."""
        with pytest.raises(ValidationError):
            DrinkSchema(quantity=1, size=DrinkSize.REGULAR, name="INVALID")

    def test_drink_invalid_case_special_instructions(self):
        """Test invalid case for special instructions."""
        with pytest.raises(ValidationError):
            DrinkSchema(quantity=1, size=DrinkSize.REGULAR, name=FountainDrink.COKE, special_instructions=123)

    def test_drink_invalid_case_bottle_name(self):
        """Test invalid case for bottle name."""
        with pytest.raises(ValidationError):
            DrinkSchema(quantity=1, size=DrinkSize.BOTTLE, name="INVALID", special_instructions="Extra syrup")

    def test_drink_invalid_case_bottle_size_fountain_drink(self):
        """Test invalid case for bottle size with fountain drink."""
        with pytest.raises(ValueError):
            drink_schema = DrinkSchema(quantity=1, size=DrinkSize.BOTTLE, name=FountainDrink.COKE, special_instructions="Extra syrup")
            Drink(**drink_schema.model_dump())

    def test_drink_invalid_case_fountain_size_bottle_drink(self):
        """Test invalid case for fountain size with bottle drink."""
        with pytest.raises(ValueError):
            drink_schema = DrinkSchema(quantity=1, size=DrinkSize.REGULAR, name=BottleDrink.BOTTLED_SODA, special_instructions="Extra syrup")
            Drink(**drink_schema.model_dump())

        
