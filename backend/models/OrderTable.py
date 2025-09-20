"""Database model for order persistence in Steve's Place.

This module defines the OrderTable class which represents the database
schema for storing customer orders with SQLAlchemy ORM.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json
from db import db

class OrderTable(db.Model):
    """
    SQLAlchemy model representing an order in the database.
    
    This class defines the database schema for storing customer orders,
    including customer information, order details, pricing, and timestamps.
    It provides methods for converting database records to dictionary format.
    
    Attributes:
        id (int): Primary key, auto-incrementing order ID
        customer_name (str): Name of the customer placing the order
        phone_number (str): Customer's phone number for contact
        order_items (str): JSON string containing serialized order items
        total_amount (float): Total price of the order
        payment_method (str): Payment method ('cash' or 'card')
        payment_status (str): Payment status ('pending', 'succeeded', 'failed')
        sms_verification_code (str, optional): SMS verification code
        payment_intent_id (str, optional): Stripe payment intent identifier
        created_at (datetime): Timestamp when the order was created
        pickup_at (datetime): Timestamp for order pickup
    
    Example:
        >>> order = OrderTable(
        ...     customer_name="John Doe",
        ...     phone_number="5551234567",
        ...     order_items=[{"item": "burger", "price": 10.99}],
        ...     total_amount=10.99,
        ...     payment_method="card",
        ...     payment_status="pending"
        ... )
        >>> db.session.add(order)
        >>> db.session.commit()
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    order_items = db.Column(db.Text, nullable=False)  # JSON string of serialized items
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # 'cash' or 'card'
    payment_status = db.Column(db.String(20), default='pending')  # 'pending', 'succeeded', 'failed'
    
    # SMS verification fields
    sms_verification_code = db.Column(db.String(10), nullable=True)
    
    # Payment transaction fields
    payment_intent_id = db.Column(db.String(100), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    pickup_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, customer_name, phone_number, order_items, total_amount, payment_method, payment_status, payment_intent_id=None, sms_verification_code=None, pickup_at=None):
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.order_items = json.dumps(order_items) if isinstance(order_items, list) else order_items
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        
        self.payment_intent_id = payment_intent_id
        self.sms_verification_code = sms_verification_code
        self.pickup_at = pickup_at


    def __repr__(self):
        return f"<Order {self.id} {self.customer_name} {self.phone_number} {self.order_items} {self.total_amount} {self.payment_method} {self.payment_status} {self.payment_intent_id} {self.sms_verification_code} {self.created_at} {self.pickup_at}>"
    
    
    def to_dict(self):
        """
        Convert the OrderTable instance to a dictionary representation.
        
        Transforms the SQLAlchemy model instance into a dictionary format
        suitable for JSON serialization and API responses. Handles datetime
        conversion to ISO format string and JSON parsing of order items.
        
        Returns:
            dict: Dictionary containing all order fields with appropriate
                  data type conversions for serialization
        
        Example:
            >>> order_dict = order.to_dict()
            >>> print(order_dict['created_at'])
            '2023-12-01T14:30:00'
        """
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number,
            'order_items': json.loads(self.order_items) if isinstance(self.order_items, str) else self.order_items,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'payment_intent_id': self.payment_intent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'pickup_at': self.pickup_at.isoformat() if self.pickup_at else None,
        }
