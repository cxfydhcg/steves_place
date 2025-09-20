import pytest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from unittest.mock import patch
import os
import json
from models.OrderTable import OrderTable

class TestCheckoutAPI:
    mock_customer_name = 'Xufeng Ce'
    mock_phone_number = '9293008888'

    # Mock the order items data
    mock_order_items = [
        {
            'type': 'Sandwich',
            'quantity': 1,
            'size': 'Regular',
            'meat': 'BLT',
            'bread': 'White',
            'cheese': 'American',
            'toppings': ['Tomato', 'Lettuce'],
            'add_ons': ['Cheese', 'Bacon']
        },
        {
            'type': 'Drink',
            'quantity': 1,
            'name': 'Coke',
            'size': 'Regular'
        },
        {
            'type': 'Combo',
            'quantity': 1,
            'side': {
                'name': 'French Fries',
            },
            'drink': {
                'name': 'Coke',
                'size': 'Regular'
            },
            'special_instructions': 'More ice'
        },
    ]
    # Set the mock pickup time to now, in iso format
    mock_pickup_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    """Tests for the /api/checkout endpoint."""
    @patch("routes.checkout_api.generate_sms_code", return_value=True)
    @patch("utils.checkout_api_helper.validate_pickup_time", return_value=datetime(2025, 8, 25, 15, 0, tzinfo=ZoneInfo("UTC")))
    def test_send_sms_verification(self, mock_generate_sms_code, mock_validate_pickup_time, client, app, db_session):
        """Test send sms verification code. and verified data input"""
        # Create a test order
        response = client.post('/api/checkout/send_sms_verification', data={
            'customer_name': self.mock_customer_name,
            'phone_number': self.mock_phone_number,
            'order_items': json.dumps(self.mock_order_items),
            'pickup_at': self.mock_pickup_at,
            'order_price': 4.25 + 2 + 6.75 + 2 + 0.75,
        })
        assert response.status_code == 200

    @patch("routes.checkout_api.verify_sms_code", return_value=True)
    def test_verify_sms_code(self, mock_verify_sms_code, client, app, db_session):
        mock_validate_pickup_time = datetime(2025, 8, 25, 9, 0, tzinfo=ZoneInfo("US/Eastern"))
        # Turn into iso format
        mock_validate_pickup_time = mock_validate_pickup_time.astimezone(ZoneInfo("UTC")).isoformat()
        """Test verify sms code."""
        with app.app_context():
            response = client.post('/api/checkout/verify_sms', data={
                'customer_name': self.mock_customer_name,
                'phone_number': self.mock_phone_number,
                'order_items': json.dumps(self.mock_order_items),
                'pickup_at': mock_validate_pickup_time,
                'order_price': 4.25 + 2 + 6.75 + 2 + 0.75,
                'sms_code': "123456",
            })
            assert response.status_code == 200
            # Check if the order is created in the database
            order = OrderTable.query.filter_by(phone_number=self.mock_phone_number).first()
            assert order is not None
            print(order)
            assert order.total_amount == 4.25 + 2 + 6.75 + 2 + 0.75
            # SQLite return native time,
            assert order.pickup_at.replace(tzinfo=ZoneInfo("UTC")) == datetime(2025, 8, 25, 9, 0, tzinfo=ZoneInfo("US/Eastern")).astimezone(ZoneInfo("UTC"))
            # assert order.order_items == json.dumps(self.mock_order_items)

    @patch("routes.checkout_api.pay_with_card", return_value={"status": "requires_confirmation", "id": "pi_1234567890"})
    @patch("utils.checkout_api_helper.validate_pickup_time", return_value=datetime(2025, 8, 25, 15, 0, tzinfo=ZoneInfo("UTC")))
    def test_confirm_payment(self, mock_pay_with_card, mock_validate_pickup_time, client, app, db_session):
        """Test confirm payment."""
        with app.app_context():
            response = client.post('/api/checkout/confirm_payment', data={
                'customer_name': self.mock_customer_name,
                'phone_number': self.mock_phone_number,
                'order_items': json.dumps(self.mock_order_items),
                'pickup_at': self.mock_pickup_at,
                'order_price': (4.25 + 2 + 6.75 + 2 + 0.75) * 1.04,
                'payment_method_id': "pm_1234567890"
            })
            assert response.status_code == 200
            # Check if the order is created in the database
            order = OrderTable.query.filter_by(phone_number=self.mock_phone_number).first()
            assert order is not None
            # print(order)
            assert order.total_amount == (4.25 + 2 + 6.75 + 2 + 0.75) * 1.04

            # assert order.order_items == json.dumps(self.mock_order_items)

    def test_confirm_payment_succeeded_invalid_date(self, client, app, db_session):
        mock_invalidate_pickup_time = datetime(2025, 8, 25, 6, 0, tzinfo=ZoneInfo("US/Eastern"))
        # Turn into iso format
        mock_invalidate_pickup_time = mock_invalidate_pickup_time.isoformat()

        response = client.post('/api/checkout/confirm_payment', data={
            'customer_name': self.mock_customer_name,
            'phone_number': self.mock_phone_number,
            'order_items': json.dumps(self.mock_order_items),
            'pickup_at': mock_invalidate_pickup_time,
            'order_price': (4.25 + 2 + 6.75 + 2 + 0.75) * 1.04,
            'payment_method_id': "pm_1234567890"
        })
        assert response.status_code == 400
