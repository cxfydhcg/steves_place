import pytest
from models.Schema import EggSandwichSchema
from models.EggSandwich import EggSandwich, EGG_SANDWICH_ADD_ONS_PRICE_MAP, EggSandwichAddOns, EggSandwichBread, EggSandwichMeat, EggSandwichCheese, EggSandwichToppings, Egg
from pydantic import ValidationError

class TestEggSandwichValidCases:
    EGG_SANDWICH_WITH_MEAT_PRICE = 5.25
    EGG_SANDWICH_WITHOUT_MEAT = 3.5

    """Test cases for EggSandwich model - valid cases with price testing."""
    def test_price_field(self):
        assert EGG_SANDWICH_ADD_ONS_PRICE_MAP == {
            EggSandwichAddOns.MEAT: 1.50,
            EggSandwichAddOns.HASHBROWN: 0.75,
            EggSandwichAddOns.HASHBROWN_ONSIDE: 1.50,
            EggSandwichAddOns.EGG: 0.75,
            EggSandwichAddOns.CHEESE: 0.75,
        }
        assert EGG_SANDWICH_ADD_ONS_PRICE_MAP == {
            EggSandwichAddOns.MEAT: 1.50,
            EggSandwichAddOns.HASHBROWN: 0.75,
            EggSandwichAddOns.HASHBROWN_ONSIDE: 1.50,
            EggSandwichAddOns.EGG: 0.75,
            EggSandwichAddOns.CHEESE: 0.75,
        }
    
    def test_eggsandwich_valid_case(self):
        """Test that the price field is calculated correctly."""
        quantity = 2
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            toasted=True,
            grilled=True,
            meat=EggSandwichMeat.BACON,
            toppings=[EggSandwichToppings.SALT, EggSandwichToppings.PEPPER],
            special_instructions="Add extra salt",
            add_ons=[EggSandwichAddOns.MEAT, EggSandwichAddOns.HASHBROWN]
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        # Price should be (base price + add on price) * quantity
        add_on_prices = [EGG_SANDWICH_ADD_ONS_PRICE_MAP[add_on] for add_on in egg_sandwich.add_ons]
        assert egg_sandwich.price == (self.EGG_SANDWICH_WITH_MEAT_PRICE + sum(add_on_prices)) * quantity

    def test_eggsandwich_without_meat(self):
        """Test that the price field is calculated correctly."""
        quantity = 2
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            toasted=True,
            grilled=True,
            cheese=EggSandwichCheese.AMERICAN,
            toppings=[EggSandwichToppings.SALT, EggSandwichToppings.PEPPER],
            special_instructions="Add extra salt",
            add_ons=[EggSandwichAddOns.HASHBROWN]
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        # Price should be (base price + add on price) * quantity
        add_on_prices = [EGG_SANDWICH_ADD_ONS_PRICE_MAP[add_on] for add_on in egg_sandwich.add_ons]
        assert egg_sandwich.price == (self.EGG_SANDWICH_WITHOUT_MEAT + sum(add_on_prices)) * quantity
    
    def test_eggsandwich_without_add_ons(self):
        """Test that the price field is calculated correctly."""
        quantity = 2
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            toasted=True,
            grilled=True,
            cheese=EggSandwichCheese.AMERICAN,
            toppings=[EggSandwichToppings.SALT, EggSandwichToppings.PEPPER],
            special_instructions="Add extra salt",
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        # Price should be (base price + add on price) * quantity
        assert egg_sandwich.price == self.EGG_SANDWICH_WITHOUT_MEAT * quantity

    def test_eggsandwich_without_toppings(self):
        """Test that the price field is calculated correctly."""
        quantity = 2
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            cheese=EggSandwichCheese.AMERICAN,
            special_instructions="Add extra salt",
            add_ons=[EggSandwichAddOns.HASHBROWN]
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        # Price should be (base price + add on price) * quantity
        add_on_prices = [EGG_SANDWICH_ADD_ONS_PRICE_MAP[add_on] for add_on in egg_sandwich.add_ons]
        assert egg_sandwich.price == (self.EGG_SANDWICH_WITHOUT_MEAT + sum(add_on_prices)) * quantity

        # Test without add ons
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            toasted=True,
            cheese=EggSandwichCheese.AMERICAN,
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        # Price should be (base price + add on price) * quantity
        assert egg_sandwich.price == self.EGG_SANDWICH_WITHOUT_MEAT * quantity
    def test_eggsandwich_duplicate_toppings(self):
        quantity = 2
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            toasted=True,
            grilled=True,
            cheese=EggSandwichCheese.AMERICAN,
            special_instructions="Add extra salt",
            toppings=[EggSandwichToppings.SALT, EggSandwichToppings.PEPPER, EggSandwichToppings.SALT]
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        assert len(egg_sandwich.toppings) == 2
    
    def test_eggsandwich_duplicate_add_ons(self):
        quantity = 2
        egg_sandwich_schema = EggSandwichSchema(
            quantity=quantity,
            bread=EggSandwichBread.WHEAT,
            egg=Egg.FRIED,
            toasted=True,
            grilled=True,
            cheese=EggSandwichCheese.AMERICAN,
            meat=EggSandwichMeat.BACON,
            special_instructions="Add extra salt",
            add_ons=[EggSandwichAddOns.MEAT, EggSandwichAddOns.HASHBROWN, EggSandwichAddOns.MEAT]
        )
        egg_sandwich = EggSandwich(**egg_sandwich_schema.model_dump())
        assert len(egg_sandwich.add_ons) == 2

class TestEggSandwichInvalidCases:
    def test_eggsandwich_invalid_quantity(self):
        """Test that the quantity field is validated."""
        with pytest.raises(ValidationError):
            EggSandwichSchema(
                quantity=0,
                bread=EggSandwichBread.WHEAT,
                egg=Egg.FRIED,
                toasted=True,
                cheese=EggSandwichCheese.AMERICAN,
                special_instructions="Add extra salt",
            )

    def test_eggsandwich_invalid_bread(self):
        """Test that the bread field is validated."""
        with pytest.raises(ValidationError):
            EggSandwichSchema(
                quantity=1,
                bread="Invalid Bread",
                egg=Egg.FRIED,
                toasted=True,
                grilled=True,
            )
          
    def test_eggsandwich_no_egg_and_no_meat(self):
        """Test that the egg and meat fields are validated."""
        with pytest.raises(ValueError):
            egg_sandwich_schema = EggSandwichSchema(
                quantity=1,
                bread=EggSandwichBread.WHEAT,
                egg=Egg.NO_EGG,
                toasted=True,
                grilled=True,
                cheese=EggSandwichCheese.AMERICAN,
            )
            EggSandwich(**egg_sandwich_schema.model_dump())

    def test_eggsandwich_no_egg_with_egg_add_on(self):
        """Test that the add on field is validated - eggs."""
        with pytest.raises(ValueError):
            egg_sandwich_schema = EggSandwichSchema(
                quantity=1,
                bread=EggSandwichBread.WHEAT,
                egg=Egg.NO_EGG,
                toasted=True,
                grilled=True,
                meat=EggSandwichMeat.BACON,
                cheese=EggSandwichCheese.AMERICAN,
                add_ons=[EggSandwichAddOns.EGG]
            )
            EggSandwich(**egg_sandwich_schema.model_dump())

    def test_eggsandwich_no_meat_with_meat_add_on(self):
        """Test that the add on field is validated - meat."""
        with pytest.raises(ValueError):
            egg_sandwich_schema = EggSandwichSchema(
                quantity=1,
                bread=EggSandwichBread.WHEAT,
                egg=Egg.FRIED,
                toasted=True,
                grilled=True,
                cheese=EggSandwichCheese.AMERICAN,
                add_ons=[EggSandwichAddOns.MEAT]
            )
            EggSandwich(**egg_sandwich_schema.model_dump())

    def test_eggsandwich_no_cheese_with_cheese_add_on(self):
        """Test that the add on field is validated - cheese."""
        with pytest.raises(ValueError):
            egg_sandwich_schema = EggSandwichSchema(
                quantity=1,
                bread=EggSandwichBread.WHEAT,
                egg=Egg.FRIED,
                toasted=True,
                grilled=True,
                meat=EggSandwichMeat.BACON,
                add_ons=[EggSandwichAddOns.CHEESE]
            )
            EggSandwich(**egg_sandwich_schema.model_dump())

            
    

    

