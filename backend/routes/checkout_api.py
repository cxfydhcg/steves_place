import json
import logging
from flask import Blueprint, request, jsonify
from models.OrderTable import OrderTable, db
from utils.checkout_api_helper import generate_sms_code, validate_order, verify_sms_code, serialize_food_item, pay_with_card, cancel_payment_intent, confirm_payment_intent
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(os.path.join(log_dir, 'checkout_api.log'))
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

routes = Blueprint('checkout_api', __name__, url_prefix='/api/checkout')

    
@routes.route('/send_sms_verification', methods=['POST'])
def send_sms_verification():
    # return jsonify({'success': True, 'message': 'Test: Verification code received successfully'}), 200
    """
    Handle SMS verification request for cash payments.
    
    This endpoint initiates the SMS verification process for customers who want to pay with cash.
    It validates the order data, generates an SMS verification code, and sends it to the customer's phone.
    
    Form Data:
        customer_name (str): Customer's name (max 100 characters)
        phone_number (str): 10-digit phone number for SMS verification
        order_items (str): JSON string containing array of order items
        order_price (str): Total order price as string
    
    Returns:
        JSON response with success status and message, or error details
        
    Status Codes:
        200: SMS verification code sent successfully
        500: Failed to generate verification code or server error
    
    Raises:
        ValueError: If order validation fails
        Exception: For any other server errors
    """
    logger.info(f"SMS verification request received from IP: {request.remote_addr}")
    try:
        # Parse form data
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        order_items = json.loads(request.form.get('order_items'))
        order_price = float(request.form.get('order_price'))
        pickup_at = request.form.get('pickup_at')
        
        logger.info(f"SMS verification request - Customer: {customer_name}, Phone: {phone_number}, Order Price: ${order_price}")
        
        try:
            order, pickup_time = validate_order(customer_name, phone_number, order_items, order_price, pickup_at, card_payment=False)
        except ValueError as e:
            logger.error(f"Order validation failed for {customer_name}: {str(e)}")
            return jsonify({'error': f'Order validation failed: {str(e)}'}), 400
    
        # Generate verification code and temporary order ID
        if not generate_sms_code(phone_number):
            logger.error(f"Failed to generate SMS code for phone: {phone_number}")
            return jsonify({'error': 'Failed to generate verification code'}), 500
        else:
            logger.info(f"SMS verification code sent successfully to {phone_number}")
            return jsonify({
                'success': True,
                'message': 'Verification code sent successfully',
            }), 200

    except Exception as e:
        logger.error(f"SMS verification failed for {phone_number}: {str(e)}")
        return jsonify({'error': f'Failed to receive verification: {str(e)}'}), 500

@routes.route('/verify_sms', methods=['POST'])
def verify_sms():
    """
    Verify SMS code and confirm cash order placement.
    
    This endpoint verifies the SMS code sent to the customer and creates the order
    in the database upon successful verification. The order is marked as 'pending'
    with payment method 'cash'.
    
    Form Data:
        customer_name (str): Customer's name (max 100 characters)
        phone_number (str): 10-digit phone number used for SMS verification
        order_items (str): JSON string containing array of order items
        order_price (str): Total order price as string
        sms_code (str): SMS verification code received by customer
    
    Returns:
        JSON response with success status and estimated preparation time, or error details
        
    Status Codes:
        200: Order placed successfully
        500: SMS verification failed, database error, or server error
    
    Raises:
        ValueError: If order validation or SMS verification fails
        Exception: For database errors or other server errors
    """
    logger.info(f"SMS verification attempt from IP: {request.remote_addr}")
    try:
        # Parse form data
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        order_items = json.loads(request.form.get('order_items'))
        order_price = float(request.form.get('order_price'))
        pickup_at = request.form.get('pickup_at')
        sms_code = request.form.get('sms_code')
        
        logger.info(f"SMS verification - Customer: {customer_name}, Phone: {phone_number}, Code: {sms_code}")
        try:
            order, pickup_time = validate_order(customer_name, phone_number, order_items, order_price, pickup_at, card_payment=False)
        except ValueError as e:
            logger.error(f"Order validation failed for {customer_name}: {str(e)}")
            return jsonify({'error': f'Order validation failed: {str(e)}'}), 400

        if not verify_sms_code(phone_number, sms_code):
            logger.error(f"Failed to verify SMS code for {phone_number}")
            return jsonify({'error': 'Failed to verify SMS code'}), 400

        logger.info(f"SMS code verified successfully for {phone_number}")
        
        try:
            # After verified, create order in database
            order_db = OrderTable(
                customer_name=customer_name,
                phone_number=phone_number,
                order_items=[serialize_food_item(item) for item in order.items],  # Serialize items
                total_amount=order.total_price(),
                payment_method='cash',
                payment_status='pending',
                sms_verification_code=sms_code,
                pickup_at=pickup_time,
            )
            db.session.add(order_db)
            db.session.commit()
            logger.info(f"Cash order created successfully - Order ID: {order_db.id}, Customer: {customer_name}, Amount: ${order.total_price()}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create cash order for {customer_name}: {str(e)}")
            return jsonify({'error': f'Failed to create order: {str(e)}'}), 500

        return jsonify({
            'success': True,
            'message': 'Order placed! Estimated time: Sandwich/EggSandwich: ~7-10 mins, Other items: ~3-7 mins (depends on kitchen workload)',
        }), 200

    except Exception as e:
        logger.error(f"SMS verification failed for {phone_number}: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@routes.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    """
    Confirm card payment and create order after successful payment processing.
    
    This endpoint processes card payments using Stripe, creates a payment intent,
    and upon successful payment confirmation, creates the order in the database.
    The order includes processing fees for card payments.
    
    Form Data:
        customer_name (str): Customer's name (max 100 characters)
        phone_number (str): 10-digit phone number for order contact
        order_items (str): JSON string containing array of order items
        order_price (str): Total order price as string (including fees)
        payment_method_id (str): Stripe payment method ID for card processing
    
    Returns:
        JSON response with success status and estimated preparation time, or error details
        
    Status Codes:
        200: Payment confirmed and order placed successfully
        400: Payment confirmation failed
        500: Database error or server error
    
    Raises:
        ValueError: If order validation fails
        Exception: For payment processing, database errors, or other server errors
        
    Note:
        If database error occurs after payment, the payment intent is automatically cancelled
    """
    logger.info(f"Card payment confirmation request from IP: {request.remote_addr}")
    try:
        # Parse form data
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        order_items = json.loads(request.form.get('order_items'))
        order_price = float(request.form.get('order_price'))
        pickup_at = request.form.get('pickup_at')

        payment_method_id = request.form.get('payment_method_id')
        
        logger.info(f"Card payment - Customer: {customer_name}, Phone: {phone_number}, Amount: ${order_price}")
        try:
            order, pickup_time = validate_order(customer_name, phone_number, order_items, order_price, pickup_at, card_payment=True)
        except ValueError as e:
            logger.error(f"Order validation failed for {customer_name}: {str(e)}")
            return jsonify({'error': f'Order validation failed: {str(e)}'}), 400

        # Pay with card
        payment_response = pay_with_card(payment_method_id, order.total_price_with_fee())
        logger.info(f"Payment response for {customer_name}: {payment_response.get('status', 'unknown')}")
        
        if payment_response['status'] == 'requires_confirmation':
            try:
                # Payment successful - create order
                order_db = OrderTable(
                    customer_name=customer_name,
                    phone_number=phone_number,
                    order_items=[serialize_food_item(item) for item in order.items],  # Serialize items
                    total_amount=order.total_price_with_fee(),
                    payment_method='card',
                    payment_status='succeeded',
                    payment_intent_id=payment_response['id'],
                    pickup_at=pickup_time,
                )
                db.session.add(order_db)
                db.session.commit()  # Commit the transaction
                
                logger.info(f"Card order created successfully - Order ID: {order_db.id}, Customer: {customer_name}, Amount: ${order.total_price_with_fee()}, Payment Intent: {payment_response['id']}")

                confirm_payment_intent(payment_response['id'], {
                    'order_id': str(order_db.id),
                    'customer_name': customer_name,
                    'phone_number': phone_number,
                })
                logger.info(f"Payment intent confirmed for Order ID: {order_db.id}")
                
                return jsonify({
                    'success': True,
                    'message': 'Payment confirmed! Estimated time: Sandwich/EggSandwich: ~7-10 mins, Other items: ~3-7 mins (depends on kitchen workload)',
                }), 200
                
            except Exception as e:
                # Handle database errors, this should never happen
                db.session.rollback()
                # Cancel the payment intent
                cancel_payment_intent(payment_response['id'])
                logger.error(f"Database error for {customer_name}, payment intent cancelled: {str(e)}")
                return jsonify({'error': f'Database error: {str(e)}'}), 500
                
        else:
            logger.warning(f"Payment confirmation failed for {customer_name}: {payment_response.get('status', 'unknown')}")
            return jsonify({
                'error': 'Payment confirmation failed',
                'status': payment_response.get('status', 'unknown')
            }), 400
            
    except Exception as e:
        logger.error(f"Card payment server error for {customer_name}: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


