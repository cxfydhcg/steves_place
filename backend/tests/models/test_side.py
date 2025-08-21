import pytest
from models.Side import Side, SideName, SideSize, Chips, SIDE_PRICE_MAP
from models.Schema import SideSchema
from pydantic import ValidationError

class TestSideValidCases:
    """Test valid Side cases for Side model - with price testing."""
    def test_price_field(self):
        """Test price field in Side model."""
        assert SIDE_PRICE_MAP == {
            SideName.CHIPS: 1.75,
            SideName.SLAW: {
                SideSize.REGULAR: 3.00,
                SideSize.LARGE: 5.75
            },
            SideName.POTATO_SALAD: {
                SideSize.REGULAR: 3.00,
                SideSize.LARGE: 5.75
            },
            SideName.MACARONI_SALAD: {
                SideSize.REGULAR: 3.00,
                SideSize.LARGE: 5.75
            },
            SideName.DEVILED_EGG: {
                SideSize.REGULAR: 3.00,
                SideSize.LARGE: 5.75
            },
            SideName.TUNA_SALAD: {
                SideSize.REGULAR: 4.00,
                SideSize.LARGE: 8.75
            },
            SideName.CHICKEN_SALAD: {
                SideSize.REGULAR: 4.00,
                SideSize.LARGE: 8.75
            },
            SideName.FRENCH_FRIES: {
                SideSize.REGULAR: 2.75,
                SideSize.LARGE: 3.50
            },
            SideName.CHEESE_FRIES: {
                SideSize.REGULAR: 3.25,
                SideSize.LARGE: 3.75
            },
            SideName.CHILLI_CHEESE_FRIES: {
                SideSize.REGULAR: 3.75,
                SideSize.LARGE: 4.25
            }
        }
    
    def test_side_valid_case_chips(self):
        """Test valid Side case for Chips."""
        quantity = 2
        side_schema = SideSchema(name=SideName.CHIPS, size=SideSize.REGULAR, quantity=quantity, chips_type=Chips.LAYS_BBQ)
        side = Side(**side_schema.model_dump())
        assert side.quantity == quantity
        assert side.name == SideName.CHIPS
        assert side.size == SideSize.REGULAR
        assert side.price == SIDE_PRICE_MAP[SideName.CHIPS] * quantity
        assert side.special_instructions == None

        side_schema = SideSchema(name=SideName.CHIPS, size=SideSize.LARGE, quantity=quantity, chips_type=Chips.LAYS_BBQ)
        side = Side(**side_schema.model_dump())
        assert side.quantity == quantity
        assert side.name == SideName.CHIPS
        assert side.size == SideSize.LARGE
        assert side.price == SIDE_PRICE_MAP[SideName.CHIPS] * quantity
        assert side.special_instructions == None

    def test_side_valid_case_non_chips(self):
        """Test valid Side case for non-Chips."""
        quantity = 2
        side_schema = SideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR, quantity=quantity)
        side = Side(**side_schema.model_dump())
        assert side.quantity == quantity
        assert side.name == SideName.FRENCH_FRIES
        assert side.size == SideSize.REGULAR
        assert side.price == SIDE_PRICE_MAP[SideName.FRENCH_FRIES][SideSize.REGULAR] * quantity
        assert side.special_instructions == None

        side_schema = SideSchema(name=SideName.FRENCH_FRIES, size=SideSize.LARGE, quantity=quantity)
        side = Side(**side_schema.model_dump())
        assert side.quantity == quantity
        assert side.name == SideName.FRENCH_FRIES
        assert side.size == SideSize.LARGE
        assert side.price == SIDE_PRICE_MAP[SideName.FRENCH_FRIES][SideSize.LARGE] * quantity
        assert side.special_instructions == None

    def test_side_valid_case_non_chips_with_special_instructions(self):
        """Test valid Side case for non-Chips with special instructions."""
        quantity = 2
        side_schema = SideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR, quantity=quantity, special_instructions="Add ketchup")
        side = Side(**side_schema.model_dump())
        assert side.quantity == quantity
        assert side.name == SideName.FRENCH_FRIES
        assert side.size == SideSize.REGULAR
        assert side.price == SIDE_PRICE_MAP[SideName.FRENCH_FRIES][SideSize.REGULAR] * quantity
        assert side.special_instructions == "Add ketchup"

class TestSideInvalidCases:
    """Test invalid Side cases for Side model."""
    def test_side_invalid_case_quantity(self):
        """Test invalid Side case for quantity."""
        with pytest.raises(ValidationError):
            SideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR, quantity=0)
    def test_side_invalid_case_name(self):
        """Test invalid Side case for name."""
        with pytest.raises(ValidationError):
            SideSchema(name="InvalidSide", size=SideSize.REGULAR, quantity=2)
    def test_side_invalid_case_size(self):
        """Test invalid Side case for size."""
        with pytest.raises(ValidationError):
            SideSchema(name=SideName.FRENCH_FRIES, size="InvalidSize", quantity=2)
    def test_side_invalid_case_special_instructions(self):
        """Test invalid Side case for special instructions."""
        with pytest.raises(ValidationError):
            SideSchema(name=SideName.FRENCH_FRIES, size=SideSize.REGULAR, quantity=2, special_instructions=123)
    
    def test_side_invalid_case_chips_type(self):
        """Test invalid Side case for chips type."""
        with pytest.raises(ValidationError):
            SideSchema(name=SideName.CHIPS, size=SideSize.REGULAR, quantity=2, chips_type="InvalidChips")
    def test_side_invalid_case_chips_size_regular(self):
        """Test invalid Side case for chips size regular."""
        with pytest.raises(ValueError):
            side_schema = SideSchema(name=SideName.CHIPS, size=SideSize.REGULAR, quantity=2)
            side = Side(**side_schema.model_dump())