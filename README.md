# Steve's Place - Restaurant Ordering System

A full-stack restaurant ordering application built with React (TypeScript) frontend and Flask (Python) backend, featuring online ordering, payment processing, and SMS verification.

## 🏗️ Project Structure

```
steves_place/
├── frontend/          # React TypeScript frontend
├── backend/           # Flask Python API backend
├── docker-compose.yml # Docker orchestration
└── README.md         # This file
```

## 🚀 Features

- **Menu Management**: Dynamic menu with categories (Hotdogs, Sandwiches, Egg Sandwiches, Salads, Sides, Drinks, Combos)
- **Order Customization**: Detailed customization options for each menu item
- **Payment Processing**: Stripe integration for card payments
- **SMS Verification**: Twilio integration for cash order verification
- **Responsive Design**: Modern UI built with React, TypeScript, and Tailwind CSS
- **Real-time Updates**: Order status tracking and notifications
- **Docker Support**: Containerized deployment with multi-stage builds

## 🛠️ Tech Stack

### Frontend

- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **Radix UI** for accessible components
- **React Router** for navigation
- **Stripe React** for payment processing
- **Lucide React** for icons

### Backend

- **Flask 2.3** web framework
- **SQLAlchemy** ORM with SQLite database
- **Stripe API** for payment processing
- **Twilio API** for SMS verification
- **Flask-CORS** for cross-origin requests
- **Pydantic** for data validation

### DevOps

- **Docker** with multi-stage builds
- **Docker Compose** for orchestration
- **Nginx** for production frontend serving

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.12+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd steves_place
   ```

2. **Start the application**

   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Local Development

1. **Backend Setup**

   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

## 📱 API Endpoints

### Menu Information

- `GET /api/get_category` - Get all menu categories
- `GET /api/get_menu` - Get complete menu with prices
- `GET /api/get_hotdog` - Get hotdog customization options
- `GET /api/get_sandwich` - Get sandwich customization options
- `GET /api/get_eggsandwich` - Get egg sandwich options
- `GET /api/get_salad` - Get salad customization options
- `GET /api/get_drink` - Get drink options
- `GET /api/get_combo` - Get combo meal options
- `GET /api/get_side` - Get side dish options

### Order Processing

- `POST /api/checkout/send_sms_verification` - Send SMS verification for cash orders
- `POST /api/checkout/verify_sms` - Verify SMS code and place cash order
- `POST /api/checkout/confirm_payment` - Process card payment and place order

### Store Management

- `POST /get_today_orders` - Get all orders placed today (requires authentication)
- `GET /get_store_close_date` - Get store closure dates from today onwards
- `POST /add_close_date` - Add new store closure date (requires authentication)

## 🔧 Configuration

### Environment Variables

**Backend (.env)**

```env
STRIPE_SECRET_KEY=your_stripe_secret_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
PORT=5000
```

**Frontend (.env)**

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
```

## 🐳 Docker Configuration

The project uses multi-stage Docker builds:

- **Development**: Hot reload enabled for both frontend and backend
- **Production**: Optimized builds with Nginx for frontend serving
- **Build**: Separate build stage for Python dependencies

## 🤝 Contributing (If find any bug)

1. Open an issue in the GitHub repository.
2. Provide a detailed description of the bug, including steps to reproduce it.
3. If possible, include screenshots or logs that demonstrate the issue.

## 🆘 Support

For support, email to xufengce209@gmail.com

---

**This is a beta version of the Steve's Place ordering system. Please note that it is not yet fully functional and may contain bugs. We are working to improve and expand the features in future releases.**

---

**Built with ❤️ for my family's business Steve's Place Restaurant**
