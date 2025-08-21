import pytest
from models.Order import Order
from models.Sandwich import Sandwich, SandwichSize, SandwichBread, SandwichMeat, SandwichCheese, SandwichToppings, SANDWICH_PRICE_MAP
from models.Drink import Drink, DrinkSize, FountainDrink, DRINK_PRICE_MAP
from models.Combo import Combo
from models.Hotdog import HotDogMeat, Hotdog, HOT_DOG_PRICE_MAP
from models.Side import Side, SideName, SideSize, Chips, SIDE_PRICE_MAP
from models.EggSandwich import EggSandwich, EggSandwichBread, EggSandwichMeat, EggSandwichCheese, EggSandwichToppings
from models.Schema import ComboSchema, ComboDrinkSchema,ComboSideSchema, DrinkSchema, SandwichSchema, HotdogSchema, SideSchema

class TestOrder:
    def test_create_order(self):
         # Create order
        order = Order()
        test_quantity = 2
        test_total_price = 0
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
        order.add_item(combo)
        with pytest.raises(AttributeError):
            combo.price = 0
        test_total_price += 4.25 * test_quantity
        assert order.total_price() == round(test_total_price, 2)
        assert order.total_price_with_fee() == round(test_total_price * 1.04, 2)
        # Create valid sandwich
        sandwich_schema = SandwichSchema(
            quantity=test_quantity,
            bread=SandwichBread.WHEAT,
            meat=SandwichMeat.BLT,
            size=SandwichSize.REGULAR,
            toppings=[SandwichToppings.LETTUCE, SandwichToppings.ONIONS]
        )
        sandwich = Sandwich(**sandwich_schema.model_dump())
        order.add_item(sandwich)
        test_total_price += SANDWICH_PRICE_MAP[sandwich.meat][sandwich.size] * test_quantity
        assert order.total_price() == round(test_total_price, 2)
        assert order.total_price_with_fee() == round(test_total_price * 1.04, 2)
        # Create valid hotdog
        hotdog_schema = HotdogSchema(
            quantity=test_quantity,
            dog_type=HotDogMeat.BEEF,
        )
        hotdog = Hotdog(**hotdog_schema.model_dump())
        order.add_item(hotdog)
        test_total_price += HOT_DOG_PRICE_MAP[hotdog.dog_type] * test_quantity
        assert order.total_price() == round(test_total_price, 2)
        assert order.total_price_with_fee() == round(test_total_price * 1.04, 2)
        # Create valid side
        side_schema = SideSchema(
            quantity=test_quantity,
            name=SideName.FRENCH_FRIES,
            size=SideSize.REGULAR
        )
        side = Side(**side_schema.model_dump())
        order.add_item(side)
        test_total_price += SIDE_PRICE_MAP[side.name][side.size] * test_quantity
        assert order.total_price() == round(test_total_price, 2)
        assert order.total_price_with_fee() == round(test_total_price * 1.04, 2)
    
    
