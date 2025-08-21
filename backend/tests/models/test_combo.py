import pytest
from models.Combo import Combo, COMBO_BASE_PRICE, DRINK_UPGRADE_COST
from models.Side import SideSize, SideName, Chips
from models.Drink import BottleDrink, DrinkSize, FountainDrink
from models.Schema import ComboSchema, ComboSideSchema, ComboDrinkSchema
from pydantic import ValidationError

class TestComboValidCases:
    """Test cases for Combo model - valid and invalid cases with price testing."""
    def test_price_field(self):
        """Test price field in Combo model."""
        assert COMBO_BASE_PRICE == 4.25
        assert DRINK_UPGRADE_COST == 0.50
    def test_combo_valid_case_regular_drink(self):
        """Test valid combo with regular drink and price calculation."""
        test_quantity = 1
        # Create valid side (regular size, allowed type)
        side_schema = ComboSideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR)
        
        # Create regular drink
        drink_schema = ComboDrinkSchema(size=DrinkSize.REGULAR, name=FountainDrink.COKE)
        
        # Create combo
        combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_schema, special_instructions="Extra napkins")
        
        # Turn combo to model
        combo = Combo(
            quantity=combo_schema.quantity,
            side=combo_schema.side,
            drink=combo_schema.drink,
            special_instructions=combo_schema.special_instructions
        )
        test_quantity = 1
        # Verify combo properties
        assert combo.quantity == test_quantity
        assert combo.side.name == SideName.FRENCH_FRIES
        assert combo.side.size == SideSize.REGULAR
        assert combo.drink.size == DrinkSize.REGULAR
        assert combo.drink.name == FountainDrink.COKE
        assert combo.special_instructions == "Extra napkins"
        
        # Verify price (base price for regular drink)
        assert combo.price == COMBO_BASE_PRICE * test_quantity
        
        test_quantity = 2

        combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_schema)
        
        # Turn combo to model
        combo = Combo(
            quantity=combo_schema.quantity,
            side=combo_schema.side,
            drink=combo_schema.drink,
            special_instructions=combo_schema.special_instructions
        )

        # Verify combo properties
        assert combo.quantity == test_quantity
        assert combo.side.quantity == 1
        assert combo.drink.quantity == 1
        assert combo.side.name == SideName.FRENCH_FRIES
        assert combo.side.size == SideSize.REGULAR
        assert combo.drink.size == DrinkSize.REGULAR
        assert combo.drink.name == FountainDrink.COKE
        assert combo.special_instructions == None
        
        # Verify price (base price for regular drink)
        assert combo.price == COMBO_BASE_PRICE * test_quantity

    def test_combo_valid_case_large_drink(self):
        """Test valid combo with large drink and price calculation."""
        test_quantity = 2
        # Create valid side
        side_schema = ComboSideSchema(name=SideName.CHIPS, chips_type=Chips.LAYS_PLAIN)
        
        # Create large drink (should add upgrade cost)
        drink_schema = ComboDrinkSchema(size=DrinkSize.LARGE, name=FountainDrink.SPRITE)
        
        # Create combo
        combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_schema)
        
        # Turn combo to model
        combo = Combo(
            quantity=combo_schema.quantity,
            side=combo_schema.side,
            drink=combo_schema.drink,
            special_instructions=combo_schema.special_instructions
        )

        # Verify combo properties
        assert combo.quantity == test_quantity
        assert combo.side.name == SideName.CHIPS
        assert combo.side.size == SideSize.REGULAR
        assert combo.drink.size == DrinkSize.LARGE
        assert combo.drink.name == FountainDrink.SPRITE
        assert combo.special_instructions == None
        assert combo.price == (COMBO_BASE_PRICE + DRINK_UPGRADE_COST) * test_quantity
        
    def test_combo_valid_case_bottle_drink(self):
        """Test valid combo with bottled drink and price calculation."""
        test_quantity = 1
        # Create valid side
        side_schema = ComboSideSchema(quantity=test_quantity, name=SideName.SLAW, size=SideSize.REGULAR)
        
        # Create bottled drink (should add upgrade cost)
        drink_schema = ComboDrinkSchema(quantity=test_quantity, size=DrinkSize.BOTTLE, name=BottleDrink.BOTTLED_SODA)
        
        # Create combo
        combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_schema, special_instructions="Extra napkins")
        
        # Turn combo to model
        combo = Combo(
            quantity=combo_schema.quantity,
            side=combo_schema.side,
            drink=combo_schema.drink,
            special_instructions=combo_schema.special_instructions
        )
        
        # Verify combo properties
        assert combo.quantity == test_quantity
        assert combo.side.name == SideName.SLAW
        assert combo.side.size == SideSize.REGULAR
        assert combo.drink.size == DrinkSize.BOTTLE
        assert combo.drink.name == BottleDrink.BOTTLED_SODA
        assert combo.special_instructions == "Extra napkins"
        
        # Verify price (base price + upgrade cost)
        assert combo.price == (COMBO_BASE_PRICE + DRINK_UPGRADE_COST) * test_quantity
    

class TestComboInvalidCases:
    """Test invalid Combo creation scenarios."""
    
    def test_invalid_quantity_zero(self):
        """Test invalid quantity of zero."""
        test_quantity = 0
        side_schema = ComboSideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR)
        drink_shema = ComboDrinkSchema(size=DrinkSize.REGULAR, name=FountainDrink.COKE)
        
        with pytest.raises(ValidationError):
            ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema)
    
    def test_invalid_quantity_negative(self):
        """Test invalid negative quantity."""
        test_quantity = -1
        side_schema = ComboSideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR)
        drink_shema = ComboDrinkSchema(size=DrinkSize.REGULAR, name=FountainDrink.COKE)
        
        with pytest.raises(ValidationError):
            ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema)
    

    def test_invalid_side_type(self):
        """Test invalid side type."""
        test_quantity = 1
        drink_shema = ComboDrinkSchema(size=DrinkSize.REGULAR, name=FountainDrink.COKE)

        side_schema = ComboSideSchema(name=SideName.TUNA_SALAD, size=SideSize.REGULAR)
        with pytest.raises(ValueError):
            combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema)
            Combo(
                quantity=combo_schema.quantity,
                side=combo_schema.side,
                drink=combo_schema.drink,
                special_instructions=combo_schema.special_instructions,
            )
        
        side_schema = ComboSideSchema(name=SideName.CHEESE_FRIES, size=SideSize.REGULAR)
        with pytest.raises(ValueError):
            combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema)
            Combo(
                quantity=combo_schema.quantity,
                side=combo_schema.side,
                drink=combo_schema.drink,
                special_instructions=combo_schema.special_instructions,
            )

        side_schema = ComboSideSchema(name=SideName.CHILLI_CHEESE_FRIES, size=SideSize.REGULAR)
        with pytest.raises(ValueError):
            combo_schema = ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema)
            Combo(
                quantity=combo_schema.quantity,
                side=combo_schema.side,
                drink=combo_schema.drink,
                special_instructions=combo_schema.special_instructions,
            )
    
    def test_invalid_side_quality(self):
        """Test invalid side quality."""
        test_quantity = 2
        with pytest.raises(ValidationError):
            side_schema = ComboSideSchema(quantity=test_quantity, name=SideName.FRENCH_FRIES, size=SideSize.REGULAR)
        test_quantity = -1
        with pytest.raises(ValidationError):
            drink_shema = ComboDrinkSchema(quantity=test_quantity, size=DrinkSize.REGULAR, name=FountainDrink.COKE)

        test_quantity = 1
        special_instructions_field = "Extra napkins"
        with pytest.raises(ValidationError):
            side_schema = ComboSideSchema(quantity=test_quantity, name=SideName.FRENCH_FRIES, size=SideSize.REGULAR, special_instructions="Extra napkins")
        with pytest.raises(ValidationError):
            drink_shema = ComboDrinkSchema(quantity=test_quantity, size=DrinkSize.REGULAR, name=FountainDrink.COKE, special_instructions="Extra napkins")

    def test_invalid_special_instructions_type(self):
        """Test invalid special instructions type."""
        test_quantity = 1
        side_schema = ComboSideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR)
        drink_shema = ComboDrinkSchema(size=DrinkSize.REGULAR, name=FountainDrink.COKE)
        special_instructions = 123
       
        with pytest.raises(ValidationError):
            ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema, special_instructions=special_instructions)
    
    def test_invalid_special_instructions_too_long(self):
        """Test special instructions exceeding maximum length."""
        test_quantity = 1
        side_schema = ComboSideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR)
        drink_shema = ComboDrinkSchema(size=DrinkSize.REGULAR, name=FountainDrink.COKE)
        long_instructions = "a" * 501
        
        with pytest.raises(ValidationError):
            ComboSchema(quantity=test_quantity, side=side_schema, drink=drink_shema, special_instructions=long_instructions)


