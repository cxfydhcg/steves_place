import pytest
from datetime import date
from models.StoreCloseDateTable import StoreClosedDateTable

class TestStoreClosedDateTable:

    def test_storecloseddate_basic_initialization(self, app, db_session):
        """Test that a StoreClosedDateTable can be created and stored in the DB."""
        test_date = date(2024, 12, 25)
        
        # Create a closed date
        closed_date = StoreClosedDateTable(date=test_date)
        db_session.add(closed_date)
        db_session.commit()
        
        # Fetch from the DB
        stored = StoreClosedDateTable.query.filter_by(date=test_date).first()
        
        assert stored is not None
        assert stored.date == test_date
        assert stored.is_recurring is False

    def test_duplicate_date_raises_exception(self, app, db_session):
        """Test that creating a duplicate closed date raises an exception."""
        test_date = date(2024, 12, 25)
        
        # First record
        first = StoreClosedDateTable(date=test_date)
        db_session.add(first)
        db_session.commit()
        
        # Creating duplicate should raise
        with pytest.raises(Exception) as excinfo:
            duplicate = StoreClosedDateTable(date=test_date)
        
    def test_is_closed_on(self, app, db_session):
        """Test the is_closed_on class method."""
        sunday_date = date(2024, 12, 29)  # Sunday
        
        # No record yet: should return True for Sunday
        assert StoreClosedDateTable.is_closed_on(sunday_date) is True

        # Add a closed date
        closed_date = StoreClosedDateTable(date=date(2024, 12, 25))
        db_session.add(closed_date)
        db_session.commit()
        
        assert StoreClosedDateTable.is_closed_on(date(2024, 12, 25)) is True

        # Recurring closure
        recurring = StoreClosedDateTable(date=date(2024, 1, 1), is_recurring=True)
        db_session.add(recurring)
        db_session.commit()
        
        assert StoreClosedDateTable.is_closed_on(date(2024, 2, 1)) is True  # recurring
