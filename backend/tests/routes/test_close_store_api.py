import pytest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os
import json
from models.StoreCloseDateTable import StoreClosedDateTable
STORE_AUTH_SID = os.environ['STORE_AUTH_SID']

class TestCloseStoreAPI:
    """Tests for the /api/close_store/add_close_date endpoint."""

    def test_add_valid_close_date(self, client, app, db_session):
        """Test adding a valid close date."""
        with app.app_context():
            # 1 day in the future
            future_date = (datetime.now(timezone.utc) + timedelta(days=10)).astimezone(ZoneInfo("America/New_York"))
            future_str = future_date.strftime("%m/%d/%Y")
            response = client.post(
                "/api/close_store/add_close_date",
                data={"store_auth_sid": STORE_AUTH_SID, "date": future_str}
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["message"] == "Close date added successfully"

            # Convert to utc time when query
            date_obj = datetime.strptime(future_str, "%m/%d/%Y").replace(tzinfo=ZoneInfo("America/New_York")).astimezone(timezone.utc)
            
            stored = StoreClosedDateTable.query.filter_by(date=date_obj.date()).first()
            assert stored is not None
            assert stored.date == date_obj.date()

            assert StoreClosedDateTable.is_closed_on(date_obj.date())

            # Sunday data obj
            sunday_date = datetime.strptime("08/24/2025", "%m/%d/%Y").replace(tzinfo=ZoneInfo("America/New_York")).astimezone(timezone.utc)
            assert StoreClosedDateTable.is_closed_on(sunday_date.date())
    def test_missing_store_auth_sid(self, client):
        """Test request with missing store_auth_sid."""
        future_date = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
        response = client.post("/api/close_store/add_close_date", data={"date": future_date})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["error"] == "Missing store_auth_sid"

    def test_invalid_store_auth_sid(self, client):
        """Test request with wrong store_auth_sid."""
        future_date = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
        response = client.post(
            "/api/close_store/add_close_date",
            data={"store_auth_sid": "WRONG_SID", "date": future_date}
        )
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Unauthorized"

    def test_date_in_past(self, client):
        """Test request with a past date."""
        past_date = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")
        response = client.post(
            "/api/close_store/add_close_date",
            data={"store_auth_sid": STORE_AUTH_SID, "date": past_date}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["error"] == "Date can not be in the past"

    def test_invalid_date_format(self, client):
        """Test request with invalid date format."""
        response = client.post(
            "/api/close_store/add_close_date",
            data={"store_auth_sid": STORE_AUTH_SID, "date": "2025-01-01"}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["error"] == "Invalid date format"
