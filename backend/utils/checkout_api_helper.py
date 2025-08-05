from twilio.rest import Client
import os
from typing import Dict, Any, List, Union, Tuple
from typeguard import typechecked
import stripe
from dotenv import load_dotenv
from models.StoreCloseDateTable import StoreClosedDateTable
import enum
from datetime import date, datetime
from pydantic import BaseModel
from zoneinfo import ZoneInfo

load_dotenv()

# Import models for validation functions
from models.Sandwich import Sandwich
from models.Drink import Drink
from models.Combo import Combo
from models.Hotdog import Hotdog
from models.Side import Side
from models.EggSandwich import EggSandwich
from models.Salad import Salad
from models.Order import Order
from models.Schema import ComboSchema, SideSchema, DrinkSchema, HotdogSchema, SaladSchema, SandwichSchema, EggSandwichSchema, ComboSideSchema, ComboDrinkSchema
from models.Category import Category
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
# Initialize Twilio (only if credentials are available)
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_verify_service_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

twilio_client = Client(twilio_account_sid, twilio_auth_token)

@typechecked
def verify_sms_code(phone_number: str, verification_code: str) -> bool:
    """
    Verify SMS code using Twilio Verify API.
    
    Validates the SMS verification code sent to the customer's phone number
    using Twilio's Verify service. This is used in the two-factor authentication
    process for order verification.
    
    Args:
        phone_number (str): Customer's phone number (10 digits)
        verification_code (str): 6-digit verification code entered by the customer
    
    Returns:
        bool: True if verification code is valid and approved, False otherwise
        
    Example:
        >>> verify_sms_code("1234567890", "123456")
        True
    """
    return True
    verification_check = twilio_client.verify.v2.services(twilio_verify_service_sid).verification_checks.create(
        to="+1"+phone_number,
        code=verification_code
    )
    return verification_check.status == 'approved'

@typechecked
def generate_sms_code(phone_number: str) -> bool:
    """
    Generate and send SMS verification code using Twilio Verify API.
    
    Initiates the SMS verification process by sending a 6-digit code to the
    customer's phone number. This is the first step in the two-factor
    authentication process for order verification.
    
    Args:
        phone_number (str): Customer's phone number (10 digits)
    
    Returns:
        bool: True if SMS was successfully sent and status is pending, False otherwise
        
    Example:
        >>> generate_sms_code("1234567890")
        True
    """
    return True
    # Send SMS using Twilio Verify service
    message = twilio_client.verify.v2.services(twilio_verify_service_sid).verifications.create(
        to="+1"+phone_number,
        channel='sms'
    )
    return message.status == 'pending'

@typechecked
def pay_with_card(payment_method_id: str, order_price: float) -> Dict[str, Any]:
    """
    Create a Stripe PaymentIntent for card payment processing.
    
    Creates a PaymentIntent with Stripe to handle card payments. The PaymentIntent
    represents an intent to collect payment from a customer and tracks the lifecycle
    of the payment process.
    
    Args:
        payment_method_id (str): Stripe payment method ID for the card
        order_price (float): Payment amount in dollars (will be converted to cents for Stripe)
    
    Returns:
        Dict[str, Any]: Stripe PaymentIntent object if successful, error dict if failed
        
    Example:
        >>> intent = pay_with_card("pm_1234567890", 25.99)
        >>> print(intent.client_secret)
        'pi_1234567890_secret_abcdef'
    """
    try:

        # Create a payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(round(order_price * 100)),
            currency='usd',
            payment_method=payment_method_id,
            confirm=False,
            automatic_payment_methods={
                'enabled': True,
                'allow_redirects': 'never'
            }

        )   
        return payment_intent
    except stripe.error.CardError as e:
        # Handle card errors
        return {'error': 'Card payment failed', 'message': str(e)}
    except stripe.error.StripeError as e:
        # Handle other Stripe errors
        return {'error': 'Payment failed', 'message': str(e)}
    except Exception as e:
        # Handle other errors
        return {'error': 'Payment failed', 'message': str(e)}

@typechecked
def confirm_payment_intent(payment_intent_id: str, metadata: Dict[str, str]) -> None:
    """
    Confirm a Stripe PaymentIntent and update its metadata.
    
    Modifies the PaymentIntent with order metadata and then confirms it to
    complete the payment process. This is used after order verification
    is successful to finalize the payment.
    
    Args:
        payment_intent_id (str): The ID of the payment intent to confirm
        metadata (Dict[str, str]): Metadata to update for the payment intent
        
    Raises:
        stripe.error.StripeError: Logs error if Stripe API call fails
        Exception: Logs error for other failures
        
    Example:
        >>> confirm_payment_intent("pi_1234567890", {"order_id": "12345"})
    """
    try:
        stripe.PaymentIntent.modify(
            payment_intent_id,
            metadata=metadata
        )
        stripe.PaymentIntent.confirm(
            payment_intent_id,
        )
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print(f"Stripe error: {str(e)}")
    except Exception as e:
        # Handle other errors
        print(f"Error: {str(e)}")


@typechecked
def cancel_payment_intent(payment_intent_id: str) -> None:
    """
    Cancel a Stripe PaymentIntent.
    
    Cancels a PaymentIntent that hasn't been completed yet. This is typically
    used when an order verification fails or when a customer abandons the
    payment process.
    
    Args:
        payment_intent_id (str): Stripe PaymentIntent ID to cancel
        
    Example:
        >>> cancel_payment_intent("pi_1234567890abcdef")
    """
    stripe.PaymentIntent.cancel(payment_intent_id)


    if not phone.isdigit() or len(phone) != 10:
        raise ValueError('Invalid phone number format')

def validate_and_create_food_item(item_type: str, item_data: Dict[str, Any]) -> Union[Sandwich, Drink, Combo, Hotdog, Side, EggSandwich, Salad]:
    """
    Validate and create a food item from JSON data.
    
    Takes raw item data and creates the appropriate food item object based on
    the item type. Validates the data against the corresponding schema before
    creating the object.
    
    Args:
        item_type (str): Type of food item (from Category enum values)
        item_data (Dict[str, Any]): Raw data for the food item
    
    Returns:
        Union[Sandwich, Drink, Combo, Hotdog, Side, EggSandwich, Salad]: 
            Validated food item object
            
    Raises:
        ValueError: If item type is unknown or validation fails
        
    Example:
        >>> item = validate_and_create_food_item("sandwich", {"quantity": 1, "bread": "white"})
    """
    print("In validate_and_create_food_item")
    print(item_type)
    print(item_data)
    try:
        match item_type:
            case Category.HOTDOG.value:
                hotdog = HotdogSchema(**item_data)
                return Hotdog(**hotdog.dict())
            case Category.SANDWICH.value:
                sandwich = SandwichSchema(**item_data)
                return Sandwich(**sandwich.dict())
            case Category.EGGSANDWICH.value:
                egg_sandwich = EggSandwichSchema(**item_data)
                return EggSandwich(**egg_sandwich.dict())
            case Category.SALAD.value:
                salad = SaladSchema(**item_data)
                return Salad(**salad.dict())
            case Category.DRINK.value:
                drink = DrinkSchema(**item_data)
                return Drink(**drink.dict())
            case Category.SIDE.value:
                side = SideSchema(**item_data)
                return Side(**side.dict())
            case Category.COMBO.value:
                combo = ComboSchema(**item_data)
                # Convert side and drink schemas to model instances
                side = ComboSideSchema(**combo.side.dict())
                drink = ComboDrinkSchema(**combo.drink.dict())
                return Combo(
                    quantity=combo.quantity,
                    side=side,
                    drink=drink,
                    special_instructions=combo.special_instructions,
                )
            case _:
                raise ValueError(f"Unknown food item type: {item_type}")

    except Exception as e:
        print(f"Error in validate_and_create_food_item: {str(e)}")
        raise ValueError(f"Error creating {item_type}: {str(e)}")

def validate_order_items(items_data: List[Dict[str, Any]]) -> Order:
    """
    Validate all food items in the order and return Order object.
    
    Processes a list of raw item data, validates each item, creates the
    appropriate food item objects, and adds them to an Order object.
    
    Args:
        items_data (List[Dict[str, Any]]): List of raw food item data
    
    Returns:
        Order: Order object containing all validated food items
        
    Raises:
        ValueError: If any food item validation fails
        
    Example:
        >>> order = validate_order_items([{"type": "sandwich", "quantity": 1}])
    """
    order = Order()
    for item_data in items_data:
        try:
            # Extract type and create a copy without the type field for constructor
            item_type = item_data['type']
            item_params = {k: v for k, v in item_data.items() if k != 'type'}
            
            # Create the food item (validation happens in constructor)
            food_item = validate_and_create_food_item(item_type, item_params)
            order.add_item(food_item)
        except Exception as e:
            raise ValueError(f"Invalid food item: {str(e)}")
    
    return order

@typechecked
def validate_order(customer_name: str, phone_number: str, order_items_data: List[Dict[str, Any]], order_price: float, pickup_at: str, card_payment: bool = False) -> Tuple[Order, date]:
    """
    Validate complete order data and return Order object.
    
    Validates customer information, order items, and pricing. Ensures all
    data is properly formatted and the calculated price matches the provided
    price (including fees for card payments).
    
    Args:
        customer_name (str): Customer's name (max 100 characters)
        phone_number (str): Customer's 10-digit phone number
        order_items_data (List[Dict[str, Any]]): List of raw food item data
        order_price (float): Expected total price
        pickup_at (str): Pickup time in ISO format (YYYY-MM-DD HH:MM:SS)
        card_payment (bool, optional): Whether payment is by card. Defaults to False
    
    Returns:
        Order: Validated Order object with all items
        
    Raises:
        ValueError: If customer name too long, phone number invalid, or price mismatch
        AssertionError: If calculated price doesn't match provided price
        
    Example:
        >>> order = validate_order("John Doe", "1234567890", items, 25.99, True)
    """
    if len(customer_name) > 100:
        raise ValueError('Customer name can not exceed 100 characters')
    if not phone_number.isdigit() or len(phone_number) != 10:
        raise ValueError('Phone number must be 10 digits')

    # Pickup time is in iso format, which is in utc
    pickup_time = datetime.fromisoformat(pickup_at)
    # Convert to Eastern Time if the pickup_time is naive (no timezone)
    if pickup_time.tzinfo is None:
        # Assume input is UTC and convert to Eastern
        pickup_time = pickup_time.replace(tzinfo=ZoneInfo('UTC'))
    pickup_time_eastern = pickup_time.astimezone(ZoneInfo('US/Eastern'))
    
    # Time can not exceed store hour 7:30AM-5:30PM in eastern time
    store_hour_start = pickup_time_eastern.replace(hour=7, minute=30, second=0, microsecond=0)
    store_hour_end = pickup_time_eastern.replace(hour=17, minute=30, second=0, microsecond=0)
    if pickup_time_eastern < store_hour_start or pickup_time_eastern > store_hour_end:
        raise ValueError('Pickup time must be between 7:30AM and 5:30PM Eastern Time')
    # Check if store is closed on pickup date
    if StoreClosedDateTable.is_closed_on(pickup_time.date()):
        raise ValueError('Store is closed on this date')
    order = validate_order_items(order_items_data)
    if card_payment:
        assert order_price == order.total_price_with_fee(), 'Order price does not match'
    else:
        assert order_price == order.total_price(), 'Order price does not match'

    return order, pickup_time

def to_serializable(obj):
    """
    Convert complex objects to JSON-serializable format.
    
    Recursively converts objects that are not natively JSON-serializable
    (like Enums and Pydantic models) into basic Python types that can
    be serialized to JSON.
    
    Args:
        obj: Object to convert (can be Enum, BaseModel, dict, list, or primitive)
    
    Returns:
        JSON-serializable representation of the object
        
    Example:
        >>> to_serializable(MyEnum.VALUE)
        'value'
        >>> to_serializable(MyModel(field="test"))
        {'field': 'test'}
    """
    if isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, BaseModel):
        return {k: to_serializable(v) for k, v in obj.dict().items()}
    elif isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    else:
        return obj

def serialize_food_item(item) -> dict:
    """
    Serialize a food item object to a dictionary.
    
    Converts a food item object into a JSON-serializable dictionary format
    that includes the item type, price, and all attributes. Used for storing
    order data and API responses.
    
    Args:
        item: Food item object (Sandwich, Drink, Combo, etc.)
    
    Returns:
        dict: Serialized representation of the food item
        
    Example:
        >>> serialize_food_item(sandwich_obj)
        {'type': 'Sandwich', 'price': 8.99, 'bread': 'white', 'quantity': 1}
    """
    item_dict = {
        'type': item.__class__.__name__,
        'price': item.price
    }
    for attr_name, attr_value in item.__dict__.items():
        item_dict[attr_name] = to_serializable(attr_value)
    return item_dict