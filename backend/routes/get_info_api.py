import json
import logging
from flask import request, Response, Blueprint
import os
from collections import OrderedDict
from datetime import datetime, time, timezone
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

# Import models for validation functions
from models.Category import Category
from models.Hotdog import HOT_DOG_PRICE_MAP, HotDogTopping
from models.Sandwich import SANDWICH_PRICE_MAP, SANDWICH_ADD_ONS_PRICE_MAP, SandwichSize, SandwichBread, SandwichCheese, SandwichToppings
from models.EggSandwich import EGG_SANDWICH_ADD_ONS_PRICE_MAP, Egg, EggSandwichBread, EggSandwichCheese, EggSandwichToppings, EggSandwichMeat
from models.Salad import SALAD_PRICE_MAP, SaladDressing, SaladTopping, SALAD_ADD_ONS_PRICE_MAP
from models.Drink import DRINK_PRICE_MAP, FountainDrink, BottleDrink, DrinkSize
from models.Side import SIDE_PRICE_MAP, SideName, Chips, SideSize
from models.Combo import COMBO_BASE_PRICE, DRINK_UPGRADE_COST
from models.OrderTable import OrderTable
from models.StoreCloseDateTable import StoreClosedDateTable

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(log_dir, 'get_info_api.log'))
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

routes = Blueprint('get_info_api', __name__, url_prefix='/api')



@routes.route('/get_category', methods=['GET'])
def get_category():
    """
    Get all available food categories.
    
    Returns a list of all food categories available in the menu system.
    
    Returns:
        JSON response containing array of category names
        
    Status Codes:
        200: Successfully returned categories
        
    Example Response:
        ["Hotdog", "Sandwich", "EggSandwich", "Salad", "Drink", "Side", "Combo"]
    """
    answer = [category.value for category in Category]
    return Response(json.dumps(answer), mimetype='application/json')

@routes.route('/get_menu', methods=['GET'])
def get_menu():
    """
    Get the complete menu with all items and their prices.
    
    Returns a comprehensive menu structure containing all food categories,
    items, and their corresponding prices. Prices are formatted as strings
    with two decimal places.
    
    Returns:
        JSON response containing complete menu structure with categories,
        item names, and prices
        
    Status Codes:
        200: Successfully returned complete menu
        
    Menu Structure:
        - Hotdog: Items with single prices
        - Sandwich: Items with Regular/Large size pricing
        - EggSandwich: Fixed price items
        - Salad: Items with single prices
        - Side: Items with size-based or fixed pricing
        - Drink: Fountain drinks with size pricing, bottled drinks with fixed pricing
        - Combo: Base price with drink upgrade options
    """
    menu = OrderedDict()
    menu["Hotdog"] = []
    menu["Sandwich"] = []
    menu["EggSandwich"] = []
    menu["Salad"] = []
    menu["Side"] = []
    menu["Drink"] = []
    menu["Combo"] = []
    for hotdog_name, hotdog_price in HOT_DOG_PRICE_MAP.items():
        menu["Hotdog"].append({"Name": hotdog_name.value, "Price": f"{hotdog_price:.2f}"})
    for sandwich_name, sandwich_price in SANDWICH_PRICE_MAP.items():
        menu["Sandwich"].append({"Name": sandwich_name.value, "Price": {
            SandwichSize.REGULAR.value: f"{sandwich_price[SandwichSize.REGULAR]:.2f}",
            SandwichSize.LARGE.value: f"{sandwich_price[SandwichSize.LARGE]:.2f}",
        }})
    menu["EggSandwich"] = [
        {"Name": "Egg Sandwich", "Price": f"3.50"}
    ]
    for salad_name, salad_price in SALAD_PRICE_MAP.items():
        menu["Salad"].append({"Name": salad_name.value, "Price": f"{salad_price:.2f}"})
    for side_name, side_price in SIDE_PRICE_MAP.items():
        if side_name == SideName.CHIPS:
            menu["Side"].append({"Name": side_name.value, "Price": f"{side_price:.2f}"})
        else:
            menu["Side"].append({"Name": side_name.value, "Price": {
            SideSize.REGULAR.value: f"{side_price[SideSize.REGULAR]:.2f}",
            SideSize.LARGE.value: f"{side_price[SideSize.LARGE]:.2f}",
        }})

    for drink_name in FountainDrink:
        menu["Drink"].append({"Name": drink_name.value, "Price": {
            DrinkSize.REGULAR.value: f"{DRINK_PRICE_MAP[DrinkSize.REGULAR]:.2f}",
            DrinkSize.LARGE.value: f"{DRINK_PRICE_MAP[DrinkSize.LARGE]:.2f}",
        }})
    for drink_name in BottleDrink:
        menu["Drink"].append({"Name": drink_name.value, "Price": f"{DRINK_PRICE_MAP[DrinkSize.BOTTLE]:.2f}"})
    menu["Combo"] = [
        {"Name": "Combo", "Price": {
            "Regular": f"{COMBO_BASE_PRICE:.2f}",
            "Upgrade to Large Drink": f"{COMBO_BASE_PRICE + DRINK_UPGRADE_COST:.2f}",
        }}
    ]

    return Response(json.dumps(menu), mimetype='application/json')

@routes.route('/get_hotdog', methods=['GET'])
def get_hotdog():
    """
    Get hotdog menu configuration including available toppings.
    
    Returns the available toppings that can be added to hotdog orders.
    This endpoint is used by the frontend to populate hotdog customization options.
    
    Returns:
        JSON response containing hotdog toppings array
        
    Status Codes:
        200: Successfully returned hotdog menu options
        
    Response Structure:
        {
            "Toppings": ["Mustard", "Ketchup", "Onions", ...]
        }
    """
    answer = OrderedDict()
    answer["Toppings"] = []
    for topping in HotDogTopping:
        answer["Toppings"].append(topping.value)

    return Response(json.dumps(answer), mimetype='application/json')

@routes.route('/get_sandwich', methods=['GET'])
def get_sandwich():
    """
    Get sandwich menu configuration including sizes, breads, toppings, and add-ons.
    
    Returns comprehensive sandwich customization options including available sizes,
    bread types, preparation methods, cheese options, toppings, and paid add-ons
    with their respective pricing.
    
    Returns:
        JSON response containing sandwich configuration options
        
    Status Codes:
        200: Successfully returned sandwich menu options
        
    Response Structure:
        {
            "Size": ["Regular", "Large"],
            "Bread": ["White", "Wheat", ...],
            "Bread Prep": ["Toasted", "Grilled", "Neither"],
            "Cheese": ["American", "Swiss", ...],
            "Toppings": ["Lettuce", "Tomato", ...],
            "Add Ons": [{"Add Ons": "name", "Add Ons Price": {"Regular": "price", "Large": "price"}}]
        }
    """
    answer = OrderedDict()
    answer["Size"] = []
    answer["Bread"] = []
    answer["Bread Prep"] = []
    answer["Cheese"] = []
    answer["Toppings"] = []
    for size in SandwichSize:
        answer["Size"].append(size.value)
    for bread in SandwichBread:
        answer["Bread"].append(bread.value)

    answer["Bread Prep"].append("Toasted")
    answer["Bread Prep"].append("Grilled")
    answer["Bread Prep"].append("Neither")

    for cheese in SandwichCheese:
        answer["Cheese"].append(cheese.value)
    for topping in SandwichToppings:
        answer["Toppings"].append(topping.value)
    

    answer["Add Ons"] = []
    for add_ons, add_ons_price in SANDWICH_ADD_ONS_PRICE_MAP.items():
        answer["Add Ons"].append({
            "Add Ons": add_ons.value,
            "Add Ons Price": {
                SandwichSize.REGULAR.value: f"{add_ons_price[SandwichSize.REGULAR]:.2f}",
                SandwichSize.LARGE.value: f"{add_ons_price[SandwichSize.LARGE]:.2f}"
            }
        })
    return Response(json.dumps(answer), mimetype='application/json')

@routes.route('/get_eggsandwich', methods=['GET'])
def get_egg_sandwich():
    """
    Get egg sandwich menu configuration including eggs, breads, meats, and add-ons.
    
    Returns comprehensive egg sandwich customization options including egg preparation,
    bread types, preparation methods, meat options, cheese, toppings, and paid add-ons
    with their respective pricing.
    
    Returns:
        JSON response containing egg sandwich configuration options
        
    Status Codes:
        200: Successfully returned egg sandwich menu options
        
    Response Structure:
        {
            "Egg": ["Scrambled", "Fried", ...],
            "Bread": ["White", "Wheat", ...],
            "Bread Prep": ["Toasted", "Grilled", "Neither"],
            "Meat": ["Bacon", "Sausage", ...],
            "Cheese": ["American", "Swiss", ...],
            "Toppings": ["Lettuce", "Tomato", ...],
            "Add Ons": [{"Add Ons": "name", "Add Ons Price": "price"}]
        }
    """
    answer = OrderedDict()
    answer["Egg"] = []
    answer["Bread"] = []
    answer["Bread Prep"] = []
    answer["Meat"] = []
    answer["Cheese"] = []
    answer["Toppings"] = []
    answer["Add Ons"] = []

    for egg in Egg:
        answer["Egg"].append(egg.value)

    for bread in EggSandwichBread:
        answer["Bread"].append(bread.value)
    answer["Bread Prep"].append("Toasted")
    answer["Bread Prep"].append("Grilled")
    answer["Bread Prep"].append("Neither")
    for meat in EggSandwichMeat:
        answer["Meat"].append(meat.value)
    for cheese in EggSandwichCheese:
        answer["Cheese"].append(cheese.value)
    for topping in EggSandwichToppings:
        answer["Toppings"].append(topping.value)

    
    for add_ons, add_ons_price in EGG_SANDWICH_ADD_ONS_PRICE_MAP.items():
        answer["Add Ons"].append({
            "Add Ons": add_ons.value,
            "Add Ons Price": f"{add_ons_price:.2f}"
        })

    return Response(json.dumps(answer), mimetype='application/json')

@routes.route('/get_salad', methods=['GET'])
def get_salad():
    """
    Get salad menu configuration including toppings, dressings, and add-ons.
    
    Returns salad customization options including available toppings,
    dressing options, and paid add-ons with their respective pricing.
    
    Returns:
        JSON response containing salad configuration options
        
    Status Codes:
        200: Successfully returned salad menu options
        
    Response Structure:
        {
            "Toppings": ["Lettuce", "Tomato", "Cucumber", ...],
            "Dressing": ["Ranch", "Italian", "Caesar", ...],
            "Add Ons": [{"Add Ons": "name", "Add Ons Price": "price"}]
        }
    """
    answer = OrderedDict()
    
    answer["Toppings"] = []
    for topping in SaladTopping:
        answer["Toppings"].append(topping.value)

    
    answer["Dressing"] = []
    for dressing in SaladDressing:
        answer["Dressing"].append(dressing.value)
    
    answer["Add Ons"] = []
    for add_ons, add_ons_price in SALAD_ADD_ONS_PRICE_MAP.items():
        answer["Add Ons"].append({
            "Add Ons": add_ons.value,
            "Add Ons Price": f"{add_ons_price:.2f}"
        })
    
    return Response(json.dumps(answer), mimetype='application/json')


    

@routes.route('/get_drink', methods=['GET'])
def get_drink():
    """
    Get drink menu configuration including available sizes.
    
    Returns the available drink sizes for fountain drinks. Bottle drinks
    have a fixed size and are not included in the size options.
    
    Returns:
        JSON response containing drink size options
        
    Status Codes:
        200: Successfully returned drink menu options
        
    Response Structure:
        {
            "Size": ["Regular", "Large"]
        }
        
    Note:
        Bottle drinks are excluded from size options as they have fixed sizing
    """
    answer = OrderedDict()
    answer["Size"] = []
    for size in DrinkSize:
        if size == DrinkSize.BOTTLE:
            continue
        answer["Size"].append(size.value)
    
    return Response(json.dumps(answer), mimetype='application/json')


@routes.route('/get_side', methods=['GET'])
def get_side():
    """
    Get side menu configuration including sizes and chip types.
    
    Returns the available sizes for side items and the different types
    of chips available for selection.
    
    Returns:
        JSON response containing side menu configuration options
        
    Status Codes:
        200: Successfully returned side menu options
        
    Response Structure:
        {
            "Size": ["Regular", "Large"],
            "Chips": ["Plain", "BBQ", "Sour Cream & Onion", ...]
        }
    """
    answer = OrderedDict()
    answer["Size"] = []
    answer["Size"].append("Regular")
    answer["Size"].append("Large")
    answer["Chips"] = []
    for chip in Chips:
        answer["Chips"].append(chip.value)
    return Response(json.dumps(answer), mimetype='application/json')

@routes.route('/get_combo', methods=['GET'])
def get_combo():
    """
    Get combo menu configuration including available sides and drinks.
    
    Returns the available side items and drink options that can be included
    in combo meals. Some premium sides are excluded from combo options.
    
    Returns:
        JSON response containing combo configuration options
        
    Status Codes:
        200: Successfully returned combo menu options
        
    Response Structure:
        {
            "Side": ["Fries", "Onion Rings", ...],
            "Drink": ["Coke", "Pepsi", "Sprite", ...],
            "Bottled Soda": ["Coke Bottle", "Pepsi Bottle", ...]
        }
        
    Note:
        Premium sides like Tuna Salad, Chicken Salad, Cheese Fries, and
        Chili Cheese Fries are excluded from combo options
    """
    answer = OrderedDict()
    answer["Side"] = []
    answer["Drink"] = []
    answer["Bottled Soda"] = []
    for side_name in SideName:
        if side_name == SideName.TUNA_SALAD or side_name == SideName.CHICKEN_SALAD or side_name == SideName.CHEESE_FRIES or side_name == SideName.CHILLI_CHEESE_FRIES:
            continue
        answer["Side"].append(side_name.value)
    
    # Add fountain drinks with size options
    for drink_name in FountainDrink:
        answer["Drink"].append(drink_name.value)

    for drink_name in BottleDrink:
        answer["Bottled Soda"].append(drink_name.value)
    
    return Response(json.dumps(answer), mimetype='application/json')



@routes.route('/get_today_orders', methods=['POST']) 
def get_today_orders():
    """
    Get today's orders filtered by Eastern Time zone.
    
    This endpoint retrieves all orders placed today based on Eastern Time zone.
    It requires store authentication to access order data. The endpoint converts
    Eastern Time to UTC for database queries and returns order details.
    
    Form Data:
        store_auth_sid (str): Store authentication token for access control
    
    Returns:
        JSON response containing array of today's orders with full order details
        
    Status Codes:
        200: Successfully returned today's orders
        400: Missing store authentication token
        401: Invalid store authentication token
        
    Response Structure:
        Array of order objects containing:
        - Order ID, customer info, items, payment details, timestamps
        
    Security:
        Requires valid store authentication token matching STORE_AUTH_SID environment variable
        
    Time Zone Handling:
        Uses Eastern Time zone for "today" calculation, converts to UTC for database queries
    """
    # Validate store_auth_sid
    store_auth_sid = request.form.get('store_auth_sid')
    if not store_auth_sid:
        logging.warning(f"Today's orders request missing store_auth_sid from IP: {request.remote_addr}")
        return Response(json.dumps({'error': 'Missing store_auth_sid'}), status=400, mimetype='application/json')
    if store_auth_sid != os.getenv('STORE_AUTH_SID'):
        logging.warning(f"Invalid store authentication attempt from IP: {request.remote_addr}, SID: {store_auth_sid}")
        return Response(json.dumps({'error': 'Unauthorized'}), status=401, mimetype='application/json')

    # Define Eastern time zone
    eastern = ZoneInfo("America/New_York")

    # Get now in Eastern time
    now_et = datetime.now(eastern)
    start_of_day_et = datetime.combine(now_et.date(), time.min, tzinfo=eastern)
    end_of_day_et = datetime.combine(now_et.date(), time.max, tzinfo=eastern)

    # Convert to UTC
    start_utc = start_of_day_et.astimezone(ZoneInfo("UTC"))
    end_utc = end_of_day_et.astimezone(ZoneInfo("UTC"))

    # Query orders in that UTC time range
    orders = OrderTable.query.filter(
        OrderTable.created_at >= start_utc,
        OrderTable.created_at <= end_utc
    ).all()

    order_list = [order.to_dict() for order in orders]
    return Response(json.dumps(order_list), mimetype='application/json')


@routes.route('/get_store_close_date', methods=['GET']) 
def get_store_close_date():
    """
    Get the store's close date for today.
    
    This endpoint retrieves the store's close date for the current day
    based on Eastern Time zone. 
    
    Returns:
        JSON response containing the store's close date for today
        
    Status Codes:
        200: Successfully returned today's close date
        
    Response Structure:
        {
            "close_dates": ["2023-12-31", "2024-01-01"]
        }
    """
    # Get today's date in Eastern Time and convert to UTC
    today_et = datetime.now(ZoneInfo("America/New_York"))
    today_utc = today_et.astimezone(timezone.utc)
    # Query the database for a closed date today and later
    closed_dates = StoreClosedDateTable.query.filter(StoreClosedDateTable.date >= today_utc.date()).all()

    print(closed_dates)
    if closed_dates:
        # If a closed date is found, return it
        return Response(json.dumps({'close_dates': [cd.date.strftime('%Y-%m-%d') for cd in closed_dates]}), status=200, mimetype='application/json')
    else:
        # If no closed date is found, return None
        return Response(json.dumps({'close_dates': []}), status=200, mimetype='application/json')

    
        