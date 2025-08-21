from random import choice
import pytest
from models.Salad import (
    Salad, SaladChoice, SaladTopping, SaladDressing, SaladAddOns,
    SALAD_PRICE_MAP, SALAD_ADD_ONS_PRICE_MAP
)
from models.Schema import SaladSchema
from pydantic import ValidationError

class TestSaladValidCases:
    """Test cases for Salad model - valid cases with price testing."""
    def test_price_field(self):
        """Test that the price field is correctly calculated."""
        assert SALAD_PRICE_MAP == {
            SaladChoice.GARDEN: 7.50,
            SaladChoice.CHEF_HAM_TURKEY: 9.50,
            SaladChoice.CHEF_CHICKEN: 9.50,
            SaladChoice.CHEF_TUNA: 9.50,
        }

        assert SALAD_ADD_ONS_PRICE_MAP == {
            SaladAddOns.CHEESE: 0.75,
            SaladAddOns.EGGS: 1.00,
            SaladAddOns.MEAT: 2.00,
            SaladAddOns.DRESSING: 0.75,
        }

    def test_salad_valid_case(self):
        """Test that the salad model is valid with valid data."""
        quantity = 2
        salad_schema = SaladSchema(
            quantity=quantity,
            choice=SaladChoice.GARDEN,
            toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
            dressing=SaladDressing.FRENCH,
        )
        salad = Salad(**salad_schema.model_dump())
        assert salad.quantity == quantity
        assert salad.choice == SaladChoice.GARDEN
        assert SaladTopping.CUCUMBER in salad.toppings
        assert SaladTopping.ONIONS in salad.toppings
        assert salad.price == SALAD_PRICE_MAP[SaladChoice.GARDEN] * quantity
        assert salad.dressing == SaladDressing.FRENCH
        assert salad.add_ons == []

    
    def test_duplicate_toppings(self):
        """Test that the salad model is valid with duplicate toppings."""
        quantity = 2
        salad_schema = SaladSchema(
            quantity=quantity,
            choice=SaladChoice.GARDEN,
            toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS, SaladTopping.CUCUMBER],
            dressing=SaladDressing.FRENCH,
        )
        salad = Salad(**salad_schema.model_dump())
        assert salad.quantity == quantity
        assert salad.choice == SaladChoice.GARDEN
        assert SaladTopping.CUCUMBER in salad.toppings
        assert SaladTopping.ONIONS in salad.toppings
        assert len(salad.toppings) == 2
        assert salad.price == SALAD_PRICE_MAP[SaladChoice.GARDEN] * quantity
        assert salad.dressing == SaladDressing.FRENCH
        assert salad.add_ons == []
    
    def test_salad_add_ons(self):
        """Test that the salad model is valid with add-ons."""
        quantity = 2
        salad_schema = SaladSchema(
            quantity=quantity,
            choice=SaladChoice.CHEF_CHICKEN,
            toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS, SaladTopping.BACON],
            dressing=SaladDressing.FRENCH,
            add_ons=[SaladAddOns.DRESSING],
        )
        salad = Salad(**salad_schema.model_dump())
        assert salad.quantity == quantity
        assert SaladTopping.CUCUMBER in salad.toppings
        assert SaladTopping.ONIONS in salad.toppings
        assert SaladTopping.BACON in salad.toppings
        assert salad.price == (SALAD_PRICE_MAP[SaladChoice.CHEF_CHICKEN] + SALAD_ADD_ONS_PRICE_MAP[SaladAddOns.DRESSING]) * quantity

class TestSaladInvalidCases:
    """Test cases for Salad model - invalid cases."""
    def test_invalid_salad_quantity(self):
        """Test that the salad model is invalid with an invalid quantity."""
        with pytest.raises(ValidationError):
            SaladSchema(
                quantity=0,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing=SaladDressing.FRENCH,
            )
        
        with pytest.raises(ValidationError):
            SaladSchema(
                quantity=-1,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing=SaladDressing.FRENCH,
            )

    def test_invalid_salad_type(self):
        """Test that the salad model is invalid with an invalid salad type."""
        with pytest.raises(ValidationError):
            SaladSchema(
                quantity=2,
                choice="invalid_salad",
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing=SaladDressing.FRENCH,
                add_ons=[SaladAddOns.DRESSING],
            )
    
    def test_invalid_topping(self):
        """Test that the salad model is invalid with an invalid topping."""
        with pytest.raises(ValidationError):
            SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=["invalid_topping"],
                dressing=SaladDressing.FRENCH,
                add_ons=[SaladAddOns.DRESSING],
            )
    
    def test_invalid_dressing(self):
        """Test that the salad model is invalid with an invalid dressing."""
        with pytest.raises(ValidationError):
            SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing="invalid_dressing",
                add_ons=[SaladAddOns.DRESSING],
            )
    
    def test_invalid_add_on(self):
        """Test that the salad model is invalid with an invalid add-on."""
        with pytest.raises(ValidationError):
            SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing=SaladDressing.FRENCH,
                add_ons=["invalid_add_on"],
            )
    def test_invalid_garden_with_bacon(self):
        """Test that the salad model is invalid with garden salad and bacon."""
        with pytest.raises(ValueError):
            salad_schema = SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS, SaladTopping.BACON],
                dressing=SaladDressing.FRENCH,
            )
            salad = Salad(**salad_schema.model_dump())
        with pytest.raises(ValueError):
            salad_schema = SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing=SaladDressing.FRENCH,
                add_ons=[SaladAddOns.MEAT],
            )
            salad = Salad(**salad_schema.model_dump())
    def test_invalid_salad_add_ons(self):
        """Test that the salad model is invalid with add-ons."""
        with pytest.raises(ValueError):
            salad_schema = SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                dressing=SaladDressing.FRENCH,
                add_ons=[SaladAddOns.CHEESE],
            )
            salad = Salad(**salad_schema.model_dump())
    
        # Test that the salad model is valid with add-ons
        with pytest.raises(ValueError):
            salad_schema = SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                add_ons=[SaladAddOns.DRESSING],
            )
            salad = Salad(**salad_schema.model_dump())
        
        # Test that the salad model is valid with add-ons
        with pytest.raises(ValueError):
            salad_schema = SaladSchema(
                quantity=2,
                choice=SaladChoice.GARDEN,
                toppings=[SaladTopping.CUCUMBER, SaladTopping.ONIONS],
                add_ons=[SaladAddOns.EGGS],
            )
            salad = Salad(**salad_schema.model_dump())
    





