# import pytest
# import json
# from datetime import datetime, timezone
# from unittest.mock import Mock, patch
# from backend.models.OrderTable import OrderTable


# class TestOrderTableCreation:
#     """Test OrderTable creation and initialization."""
    
#     def test_ordertable_basic_initialization(self):
#         """Test basic OrderTable initialization."""
#         order_items = [{"item": "hotdog", "price": 4.50, "quantity": 1}]
        
#         order = OrderTable(
#             customer_name="John Doe",
#             phone_number="5551234567",
#             order_items=order_items,
#             total_amount=4.50,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         assert order.customer_name == "John Doe"
#         assert order.phone_number == "5551234567"
#         assert order.order_items == json.dumps(order_items)
#         assert order.total_amount == 4.50
#         assert order.payment_method == "cash"
#         assert order.payment_status == "pending"
#         assert order.payment_intent_id is None
#         assert order.sms_verification_code is None
    
#     def test_ordertable_with_all_fields(self):
#         """Test OrderTable initialization with all fields."""
#         order_items = [
#             {"item": "hotdog", "price": 4.50, "quantity": 1},
#             {"item": "drink", "price": 3.00, "quantity": 1}
#         ]
#         pickup_time = datetime.now(timezone.utc)
        
#         order = OrderTable(
#             customer_name="Jane Smith",
#             phone_number="5559876543",
#             order_items=order_items,
#             total_amount=7.50,
#             payment_method="card",
#             payment_status="succeeded",
#             payment_intent_id="pi_1234567890",
#             sms_verification_code="123456",
#             pickup_at=pickup_time
#         )
        
#         assert order.customer_name == "Jane Smith"
#         assert order.phone_number == "5559876543"
#         assert order.order_items == json.dumps(order_items)
#         assert order.total_amount == 7.50
#         assert order.payment_method == "card"
#         assert order.payment_status == "succeeded"
#         assert order.payment_intent_id == "pi_1234567890"
#         assert order.sms_verification_code == "123456"
#         assert order.pickup_at == pickup_time
    
#     def test_ordertable_with_string_order_items(self):
#         """Test OrderTable initialization with string order_items."""
#         order_items_json = '[{"item": "hotdog", "price": 4.50, "quantity": 1}]'
        
#         order = OrderTable(
#             customer_name="Bob Johnson",
#             phone_number="5551112222",
#             order_items=order_items_json,
#             total_amount=4.50,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         assert order.order_items == order_items_json
    
#     def test_ordertable_payment_methods(self):
#         """Test OrderTable with different payment methods."""
#         order_items = [{"item": "hotdog", "price": 4.50, "quantity": 1}]
        
#         # Test cash payment
#         cash_order = OrderTable(
#             customer_name="Cash Customer",
#             phone_number="5551111111",
#             order_items=order_items,
#             total_amount=4.50,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         assert cash_order.payment_method == "cash"
        
#         # Test card payment
#         card_order = OrderTable(
#             customer_name="Card Customer",
#             phone_number="5552222222",
#             order_items=order_items,
#             total_amount=4.50,
#             payment_method="card",
#             payment_status="succeeded"
#         )
        
#         assert card_order.payment_method == "card"
    
#     def test_ordertable_payment_statuses(self):
#         """Test OrderTable with different payment statuses."""
#         order_items = [{"item": "hotdog", "price": 4.50, "quantity": 1}]
        
#         statuses = ["pending", "succeeded", "failed"]
        
#         for status in statuses:
#             order = OrderTable(
#                 customer_name=f"Customer {status}",
#                 phone_number="5551234567",
#                 order_items=order_items,
#                 total_amount=4.50,
#                 payment_method="card",
#                 payment_status=status
#             )
            
#             assert order.payment_status == status


# class TestOrderTableToDictMethod:
#     """Test OrderTable to_dict method."""
    
#     def test_to_dict_basic(self):
#         """Test basic to_dict conversion."""
#         order_items = [{"item": "hotdog", "price": 4.50, "quantity": 1}]
        
#         order = OrderTable(
#             customer_name="John Doe",
#             phone_number="5551234567",
#             order_items=order_items,
#             total_amount=4.50,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         # Mock the id since it's set by the database
#         order.id = 1
#         order.created_at = datetime(2023, 12, 1, 14, 30, 0, tzinfo=timezone.utc)
#         order.pickup_at = datetime(2023, 12, 1, 15, 0, 0, tzinfo=timezone.utc)
        
#         result = order.to_dict()
        
#         expected = {
#             'id': 1,
#             'customer_name': 'John Doe',
#             'phone_number': '5551234567',
#             'order_items': order_items,
#             'total_amount': 4.50,
#             'payment_method': 'cash',
#             'payment_status': 'pending',
#             'payment_intent_id': None,
#             'created_at': '2023-12-01T14:30:00+00:00',
#             'pickup_at': '2023-12-01T15:00:00+00:00'
#         }
        
#         assert result == expected
    
#     def test_to_dict_with_all_fields(self):
#         """Test to_dict conversion with all fields populated."""
#         order_items = [
#             {"item": "hotdog", "price": 4.50, "quantity": 1},
#             {"item": "drink", "price": 3.00, "quantity": 1}
#         ]
        
#         order = OrderTable(
#             customer_name="Jane Smith",
#             phone_number="5559876543",
#             order_items=order_items,
#             total_amount=7.50,
#             payment_method="card",
#             payment_status="succeeded",
#             payment_intent_id="pi_1234567890",
#             sms_verification_code="123456"
#         )
        
#         # Mock database fields
#         order.id = 2
#         order.created_at = datetime(2023, 12, 1, 14, 30, 0, tzinfo=timezone.utc)
#         order.pickup_at = datetime(2023, 12, 1, 15, 0, 0, tzinfo=timezone.utc)
        
#         result = order.to_dict()
        
#         assert result['id'] == 2
#         assert result['customer_name'] == 'Jane Smith'
#         assert result['phone_number'] == '5559876543'
#         assert result['order_items'] == order_items
#         assert result['total_amount'] == 7.50
#         assert result['payment_method'] == 'card'
#         assert result['payment_status'] == 'succeeded'
#         assert result['payment_intent_id'] == 'pi_1234567890'
#         assert result['created_at'] == '2023-12-01T14:30:00+00:00'
#         assert result['pickup_at'] == '2023-12-01T15:00:00+00:00'
    
#     def test_to_dict_with_string_order_items(self):
#         """Test to_dict conversion when order_items is stored as string."""
#         order_items_list = [{"item": "hotdog", "price": 4.50, "quantity": 1}]
#         order_items_json = json.dumps(order_items_list)
        
#         order = OrderTable(
#             customer_name="Bob Johnson",
#             phone_number="5551112222",
#             order_items=order_items_json,
#             total_amount=4.50,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         # Mock database fields
#         order.id = 3
#         order.created_at = datetime(2023, 12, 1, 14, 30, 0, tzinfo=timezone.utc)
#         order.pickup_at = datetime(2023, 12, 1, 15, 0, 0, tzinfo=timezone.utc)
        
#         result = order.to_dict()
        
#         # Should parse the JSON string back to list
#         assert result['order_items'] == order_items_list
    
#     def test_to_dict_with_none_timestamps(self):
#         """Test to_dict conversion with None timestamps."""
#         order_items = [{"item": "hotdog", "price": 4.50, "quantity": 1}]
        
#         order = OrderTable(
#             customer_name="Test Customer",
#             phone_number="5551234567",
#             order_items=order_items,
#             total_amount=4.50,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         # Mock database fields with None timestamps
#         order.id = 4
#         order.created_at = None
#         order.pickup_at = None
        
#         result = order.to_dict()
        
#         assert result['created_at'] is None
#         assert result['pickup_at'] is None


# class TestOrderTableValidation:
#     """Test OrderTable validation and edge cases."""
    
#     def test_ordertable_empty_order_items(self):
#         """Test OrderTable with empty order items."""
#         order = OrderTable(
#             customer_name="Empty Order",
#             phone_number="5551234567",
#             order_items=[],
#             total_amount=0.0,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         assert order.order_items == json.dumps([])
#         assert order.total_amount == 0.0
    
#     def test_ordertable_complex_order_items(self):
#         """Test OrderTable with complex order items structure."""
#         complex_order_items = [
#             {
#                 "item": "combo",
#                 "price": 12.99,
#                 "quantity": 1,
#                 "details": {
#                     "side": "fries",
#                     "drink": "coke",
#                     "special_instructions": "No pickles"
#                 }
#             },
#             {
#                 "item": "sandwich",
#                 "price": 8.50,
#                 "quantity": 2,
#                 "toppings": ["lettuce", "tomato", "mayo"]
#             }
#         ]
        
#         order = OrderTable(
#             customer_name="Complex Order",
#             phone_number="5551234567",
#             order_items=complex_order_items,
#             total_amount=29.99,
#             payment_method="card",
#             payment_status="succeeded"
#         )
        
#         assert order.order_items == json.dumps(complex_order_items)
        
#         # Test to_dict conversion
#         order.id = 5
#         order.created_at = datetime(2023, 12, 1, 14, 30, 0, tzinfo=timezone.utc)
#         order.pickup_at = datetime(2023, 12, 1, 15, 0, 0, tzinfo=timezone.utc)
        
#         result = order.to_dict()
#         assert result['order_items'] == complex_order_items
    
#     def test_ordertable_long_customer_name(self):
#         """Test OrderTable with long customer name."""
#         long_name = "A" * 100  # Maximum length according to schema
        
#         order = OrderTable(
#             customer_name=long_name,
#             phone_number="5551234567",
#             order_items=[{"item": "test", "price": 1.0}],
#             total_amount=1.0,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         assert order.customer_name == long_name
    
#     def test_ordertable_phone_number_format(self):
#         """Test OrderTable with different phone number formats."""
#         phone_numbers = ["5551234567", "1234567890", "0000000000"]
        
#         for phone in phone_numbers:
#             order = OrderTable(
#                 customer_name="Test Customer",
#                 phone_number=phone,
#                 order_items=[{"item": "test", "price": 1.0}],
#                 total_amount=1.0,
#                 payment_method="cash",
#                 payment_status="pending"
#             )
            
#             assert order.phone_number == phone
    
#     def test_ordertable_large_total_amount(self):
#         """Test OrderTable with large total amount."""
#         large_amount = 999999.99
        
#         order = OrderTable(
#             customer_name="Big Spender",
#             phone_number="5551234567",
#             order_items=[{"item": "expensive_item", "price": large_amount}],
#             total_amount=large_amount,
#             payment_method="card",
#             payment_status="succeeded"
#         )
        
#         assert order.total_amount == large_amount
    
#     def test_ordertable_zero_total_amount(self):
#         """Test OrderTable with zero total amount."""
#         order = OrderTable(
#             customer_name="Free Order",
#             phone_number="5551234567",
#             order_items=[{"item": "free_item", "price": 0.0}],
#             total_amount=0.0,
#             payment_method="cash",
#             payment_status="succeeded"
#         )
        
#         assert order.total_amount == 0.0
    
#     def test_ordertable_long_payment_intent_id(self):
#         """Test OrderTable with long payment intent ID."""
#         long_payment_id = "pi_" + "1" * 97  # Maximum length according to schema
        
#         order = OrderTable(
#             customer_name="Card Customer",
#             phone_number="5551234567",
#             order_items=[{"item": "test", "price": 1.0}],
#             total_amount=1.0,
#             payment_method="card",
#             payment_status="succeeded",
#             payment_intent_id=long_payment_id
#         )
        
#         assert order.payment_intent_id == long_payment_id
    
#     def test_ordertable_sms_verification_code_formats(self):
#         """Test OrderTable with different SMS verification code formats."""
#         codes = ["123456", "000000", "999999", "1234567890"]
        
#         for code in codes:
#             order = OrderTable(
#                 customer_name="SMS Customer",
#                 phone_number="5551234567",
#                 order_items=[{"item": "test", "price": 1.0}],
#                 total_amount=1.0,
#                 payment_method="cash",
#                 payment_status="pending",
#                 sms_verification_code=code
#             )
            
#             assert order.sms_verification_code == code


# class TestOrderTableDatabaseIntegration:
#     """Test OrderTable database-related functionality."""
    
#     def test_ordertable_tablename(self):
#         """Test that OrderTable has correct table name."""
#         assert OrderTable.__tablename__ == 'orders'
    
#     def test_ordertable_column_attributes(self):
#         """Test that OrderTable has all expected column attributes."""
#         # Test that all expected attributes exist
#         expected_attributes = [
#             'id', 'customer_name', 'phone_number', 'order_items',
#             'total_amount', 'payment_method', 'payment_status',
#             'sms_verification_code', 'payment_intent_id',
#             'created_at', 'pickup_at'
#         ]
        
#         for attr in expected_attributes:
#             assert hasattr(OrderTable, attr)
    
#     def test_ordertable_default_values(self):
#         """Test OrderTable default values."""
#         order = OrderTable(
#             customer_name="Default Test",
#             phone_number="5551234567",
#             order_items=[{"item": "test", "price": 1.0}],
#             total_amount=1.0,
#             payment_method="cash",
#             payment_status="pending"
#         )
        
#         # Test default values
#         assert order.payment_status == "pending"  # Should have default
#         assert order.sms_verification_code is None
#         assert order.payment_intent_id is None