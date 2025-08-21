import pytest
from models.Schema import HotdogSchema
from models.Hotdog import Hotdog, HotDogMeat, HotDogTopping, HOT_DOG_PRICE_MAP
from pydantic import ValidationError

class TestHotDogValidCases:
    """Test cases for HotDog model - valid cases with price testing."""
    def test_price_field(self):
        """Test that the price field is correctly calculated."""
        assert HOT_DOG_PRICE_MAP == {
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
    
    def test_hotdot_valid_case(self):
        """Test that the hotdog model is valid with valid data."""
        quantity = 2
        hotdog_schema = HotdogSchema(
            quantity=quantity,
            dog_type=HotDogMeat.RED,
            toppings=[HotDogTopping.CHEESE, HotDogTopping.ONIONS],
        )
        hotdog = Hotdog(**hotdog_schema.model_dump())
        assert hotdog.quantity == quantity
        assert hotdog.price == HOT_DOG_PRICE_MAP[HotDogMeat.RED] * quantity

    def test_duplicate_toppings(self):
        """Test that the hotdog model is valid with duplicate toppings."""
        quantity = 2
        hotdog_schema = HotdogSchema(
            quantity=quantity,
            dog_type=HotDogMeat.RED,
            toppings=[HotDogTopping.CHEESE, HotDogTopping.ONIONS, HotDogTopping.CHEESE],
        )
        hotdog = Hotdog(**hotdog_schema.model_dump())
        assert hotdog.quantity == quantity
        assert len(hotdog.toppings) == 2
        assert hotdog.price == HOT_DOG_PRICE_MAP[HotDogMeat.RED] * quantity

class TestHotDogInvalidCases:
    """Test cases for HotDog model - invalid cases."""
    def test_hotdog_invalid_case_quantity(self):
        """Test that the hotdog model is invalid with invalid quantity."""
        with pytest.raises(ValidationError):
            HotdogSchema(quantity=0, dog_type=HotDogMeat.RED, toppings=[HotDogTopping.CHEESE, HotDogTopping.ONIONS])
    def test_hotdog_invalid_case_dog_type(self):
        """Test that the hotdog model is invalid with invalid dog type."""
        with pytest.raises(ValidationError):
            HotdogSchema(quantity=1, dog_type="invalid", toppings=[HotDogTopping.CHEESE, HotDogTopping.ONIONS])
    def test_hotdog_invalid_case_toppings(self):
        """Test that the hotdog model is invalid with invalid toppings."""
        with pytest.raises(ValidationError):
            HotdogSchema(quantity=1, dog_type=HotDogMeat.RED, toppings=["invalid", HotDogTopping.ONIONS])
    def test_hotdog_invalid_case_special_instructions(self):
        """Test that the hotdog model is invalid with invalid special instructions."""
        with pytest.raises(ValidationError):
            HotdogSchema(quantity=1, dog_type=HotDogMeat.RED, toppings=[HotDogTopping.CHEESE, HotDogTopping.ONIONS], special_instructions=123)