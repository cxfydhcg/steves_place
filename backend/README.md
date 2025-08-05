# Steve's Place Backend API

Flask-based REST API for Steve's Place restaurant ordering system with payment processing (Stripe), SMS verification (Twilio), and menu management.

## 🏗️ Architecture

```
backend/
├── app.py                 # Flask application entry point
├── db.py                  # Database configuration
├── requirements.txt       # Python dependencies
├── dockerfile            # Multi-stage Docker build
├── .env                  # Environment variables
├── .dockerignore         # Docker ignore file
├── data/                 # Static data files
├── models/               # SQLAlchemy data models
│   ├── Category.py       # Menu categories
│   ├── Combo.py          # Combo meal definitions
│   ├── Drink.py          # Drink options and pricing
│   ├── EggSandwich.py    # Egg sandwich configurations
│   ├── Hotdog.py         # Hotdog options and toppings
│   ├── Order.py          # Order data structures
│   ├── OrderTable.py     # Database order model
│   ├── Salad.py          # Salad options and add-ons
│   ├── Sandwich.py       # Sandwich configurations
│   ├── Schema.py         # Data validation schemas
│   ├── Side.py           # Side dish options
│   └── StoreCloseDateTable.py # Store closure dates model
├── routes/               # API route handlers
│   ├── get_info_api.py   # Menu information & store management endpoints
│   ├── checkout_api.py   # Order processing endpoints
│   └── close_store_api.py # Store closure management endpoints
├── utils/                # Utility functions
│   └── checkout_api_helper.py # Payment and SMS helpers
├── instance/             # SQLite database storage
│   └── db.sqlite         # SQLite database file
└── logs/                 # Application logs
    ├── get_info_api.log  # Menu API logs
    ├── checkout_api.log  # Checkout API logs
    └── close_store_api.log # Store management logs
```

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**

   ```bash
   # Create .env file in the backend directory
   # Edit .env with your API keys
   ```

   [See All Environment Variables](#environment-variables)

3. **Run the Application**

   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Docker Development

```bash
# Build and run with Docker Compose (from project root)
docker-compose up --build backend
```

## 📋 Dependencies

### Core Framework

- **Flask 2.3.3** - Web framework
- **Flask-SQLAlchemy 3.0.5** - ORM for database operations
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Werkzeug 2.3.7** - WSGI utilities

### Database & Validation

- **SQLAlchemy 2.0.21** - Database toolkit
- **Pydantic 2.11.7** - Data validation and parsing
- **typeguard 4.4.4** - Runtime type checking

### External Services

- **Stripe 6.7.0** - Payment processing
- **Twilio 8.10.0** - SMS verification
- **requests 2.31.0** - HTTP client

### Utilities

- **python-dotenv 1.0.0** - Environment variable management
- **Jinja2 3.1.2** - Template engine
- **click 8.1.7** - Command line interface

## 🔌 API Endpoints

### Menu Information Endpoints

#### Get Categories

```http
GET /api/get_category
```

Returns all available menu categories.

**Response:**

```json
["Hotdog", "Sandwich", "EggSandwich", "Salad", "Side", "Drink", "Combo"]
```

#### Get Complete Menu

```http
GET /api/get_menu
```

Returns complete menu with items and pricing.

**Response:**

```json
{
  "Hotdog": [{ "Name": "Regular Hot Dog", "Price": "4.50" }],
  "Sandwich": [
    {
      "Name": "Turkey Sandwich",
      "Price": {
        "Regular": "6.50",
        "Large": "8.50"
      }
    }
  ]
}
```

#### Get Item Customization Options

```http
GET /api/get_hotdog
GET /api/get_sandwich
GET /api/get_eggsandwich
GET /api/get_salad
GET /api/get_drink
GET /api/get_combo
```

Each endpoint returns customization options for the respective item type.

### Order Processing Endpoints

#### Send SMS Verification (Cash Orders)

```http
POST /api/checkout/send_sms_verification
```

**Request Body:**

```json
{
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "order": {
    "items": [...],
    "total": 15.50
  }
}
```

**Response:**

```json
{
  "success": true,
  "message": "Verification code sent successfully"
}
```

#### Verify SMS and Place Order

```http
POST /api/checkout/verify_sms
```

**Request Body:**

```json
{
  "sms_code": "123456",
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "order": {...}
}
```

#### Process Card Payment

```http
POST /api/checkout/confirm_payment
```

**Request Body:**

```json
{
  "payment_method_id": "pm_1234567890",
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "order": {...}
}
```

#### Get Order Details

```http
GET /api/checkout/order/{order_id}
```

**Response:**

```json
{
  "success": true,
  "order": {
    "id": 1,
    "customer_name": "John Doe",
    "phone_number": "+1234567890",
    "order_items": [...],
    "total_amount": 15.50,
    "payment_method": "card",
    "payment_status": "succeeded",
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

### Store Management Endpoints

#### Get Today's Orders

```http
POST /get_today_orders
```

**Request Body:**

```json
{
  "store_auth_sid": "your_store_auth_token"
}
```

**Response:**

```json
[
  {
    "id": 1,
    "customer_name": "John Doe",
    "phone_number": "+1234567890",
    "order_items": [...],
    "total_amount": 15.50,
    "payment_method": "card",
    "payment_status": "succeeded",
    "created_at": "2024-01-01T12:00:00Z",
    "pickup_at": "2024-01-01T13:00:00Z"
  }
]
```

**Description:** Retrieves all orders placed today based on Eastern Time zone. Requires store authentication for access control.

#### Get Store Close Dates

```http
GET /get_store_close_date
```

**Response:**

```json
{
  "close_dates": ["2023-12-31", "2024-01-01"]
}
```

**Description:** Returns all store closure dates from today onwards in Eastern Time zone.

#### Add Store Close Date

```http
POST /add_close_date
```

**Request Body:**

```json
{
  "store_auth_sid": "your_store_auth_token",
  "date": "12/31/2023"
}
```

**Response:**

```json
{
  "message": "Close date added successfully"
}
```

**Description:** Adds a new store closure date. Date format should be MM/DD/YYYY in Eastern Time. Requires store authentication and prevents adding past dates.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Application Configuration
PORT=5000
FLASK_ENV=development

# Database Configuration (optional)
DATABASE_URL=sqlite:///db.sqlite
```

### Docker Configuration

The Dockerfile includes three stages:

1. **Build Stage**: Installs Python dependencies with build tools
2. **Development Stage**: Development environment with hot reload
3. **Production Stage**: Optimized production environment

```dockerfile
# Development
docker build --target development -t steves-backend:dev .

# Production
docker build --target production -t steves-backend:prod .
```

## 🧪 Testing

### Manual API Testing

Use curl or Postman to test endpoints:

```bash
# Test menu endpoint
curl http://localhost:5000/api/get_menu

# Test category endpoint
curl http://localhost:5000/api/get_category
```

### Health Check

```bash
curl http://localhost:5000/
# Response: "This is steve's api"
```

## 📊 Logging

Logs are written to:

- Console output (development)
- `/logs/checkout_api.log` (file logging)
- `/logs/close_store_api.log` (file logging)
- `/logs/get_info_api.log` (file logging)

Log levels:

- `INFO`: General application flow
- `ERROR`: Error conditions
- `DEBUG`: Detailed diagnostic information

## 🔒 Security Features

- **CORS Protection**: Configured for frontend domain
- **Input Validation**: Pydantic schemas for request validation
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **Payment Security**: Stripe handles sensitive payment data
- **SMS Verification**: Twilio integration for order verification

## 🚀 Deployment

### Production Deployment

1. **Set Production Environment Variables**
2. **Build Production Docker Image**
   ```bash
   docker build --target production -t steves-backend:latest .
   ```
3. **Run with Production Configuration**
   ```bash
   docker run -p 5000:5000 --env-file .env steves-backend:latest
   ```

### Performance Considerations

- **Database**: Consider PostgreSQL for production
- **Caching**: Implement Redis for menu caching
- **Load Balancing**: Use multiple instances behind a load balancer
- **Monitoring**: Add application performance monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Errors**

   - Check SQLite file permissions
   - Verify database path in configuration

2. **Stripe Payment Failures**

   - Verify API keys are correct
   - Check Stripe dashboard for error details

3. **SMS Verification Issues**

   - Confirm Twilio credentials
   - Check phone number format (+1234567890)

4. **CORS Errors**
   - Verify frontend URL in CORS configuration
   - Check request headers and methods

### Debug Mode

Enable debug mode for detailed error messages:

```python
app.run(debug=True)
```

---

**For more information, see the main project README or contact the development team.**
