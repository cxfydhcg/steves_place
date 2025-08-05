# Steve's Place Frontend

Modern React TypeScript frontend for Steve's Place restaurant ordering system with responsive design, payment integration, and real-time order management.

## 🏗️ Project Structure

```
frontend/
├── public/                # Static assets
│   ├── index.html        # HTML template
│   ├── favicon.ico       # Site favicon
│   └── manifest.json     # PWA manifest
├── src/
│   ├── App.tsx           # Main application component
│   ├── index.tsx         # Application entry point
│   ├── App.css           # Global styles
│   ├── index.css         # Base styles and Tailwind imports
│   ├── api/              # API service functions
│   ├── components/       # Reusable UI components
│   ├── context/          # React context providers
│   ├── lib/              # Utility libraries
│   ├── pages/            # Page components
│   ├── utils/            # Helper functions
│   └── react-app-env.d.ts # TypeScript declarations
├── dockerfile            # Multi-stage Docker build
├── nginx.conf            # Nginx configuration for production
├── package.json          # Dependencies and scripts
├── tailwind.config.js    # Tailwind CSS configuration
├── postcss.config.js     # PostCSS configuration
└── tsconfig.json         # TypeScript configuration
```

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Development Server**
   ```bash
   npm start
   ```

   The application will be available at `http://localhost:3000`

### Docker Development

```bash
# Build and run with Docker Compose (from project root)
docker-compose up --build frontend
```

## 📦 Dependencies

### Core Framework
- **React 19.1.0** - UI library
- **TypeScript 4.9.5** - Type-safe JavaScript
- **React DOM 19.1.0** - DOM rendering
- **React Scripts 5.0.1** - Build tooling

### Routing & Navigation
- **React Router DOM 7.7.0** - Client-side routing

### UI Components & Styling
- **Tailwind CSS 3.3.0** - Utility-first CSS framework
- **Tailwind Merge 3.3.1** - Conditional class merging
- **Tailwindcss Animate 1.0.7** - Animation utilities
- **Class Variance Authority 0.7.1** - Component variant management
- **clsx 2.1.1** - Conditional className utility

### UI Component Library
- **Radix UI React Dialog 1.1.14** - Accessible modal dialogs
- **Radix UI React Slot 1.2.3** - Composable component slots
- **Lucide React 0.525.0** - Beautiful icons
- **React Icons 5.5.0** - Popular icon library

### Payment Processing
- **Stripe React Stripe.js 3.8.0** - Stripe payment components
- **Stripe.js 7.6.1** - Stripe JavaScript SDK

### Development & Testing
- **Testing Library React 16.3.0** - React testing utilities
- **Testing Library Jest DOM 6.6.3** - Jest DOM matchers
- **Testing Library User Event 13.5.0** - User interaction testing
- **Web Vitals 2.1.4** - Performance metrics

### Build Tools
- **PostCSS 8.5.6** - CSS processing
- **Autoprefixer 10.4.21** - CSS vendor prefixing

## 🎨 UI Components

### Component Architecture

The frontend uses a component-based architecture with:

- **Atomic Design**: Components organized by complexity
- **Compound Components**: Complex UI patterns
- **Render Props**: Flexible component composition
- **Custom Hooks**: Reusable stateful logic

### Key Components

#### Layout Components
- Header with navigation
- Footer with restaurant information
- Responsive grid layouts
- Mobile-first design

#### Menu Components
- Category navigation
- Item cards with customization
- Price display with size variants
- Add to cart functionality

#### Cart Components
- Cart sidebar/modal
- Item quantity controls
- Price calculations
- Checkout button

#### Checkout Components
- Customer information form
- Payment method selection
- Stripe payment elements
- SMS verification for cash orders
- Order confirmation

#### Form Components
- Input fields with validation
- Select dropdowns
- Checkbox groups
- Radio button groups
- Form submission handling

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:5000/api

# Stripe Configuration
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# Development Configuration
CHOKIDAR_USEPOLLING=true
WATCHPACK_POLLING=true
```

### Tailwind CSS Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom color palette
      },
      fontFamily: {
        // Custom fonts
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
  ],
}
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
```

## 🔌 API Integration

### API Service Layer

The frontend uses a service layer to interact with the backend API:

```typescript
// Example API service
class ApiService {
  private baseUrl = process.env.REACT_APP_API_URL;

  async getMenu() {
    const response = await fetch(`${this.baseUrl}/get_menu`);
    return response.json();
  }

  async placeOrder(orderData: OrderData) {
    const response = await fetch(`${this.baseUrl}/checkout/confirm_payment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderData),
    });
    return response.json();
  }
}
```

### State Management

The application uses React Context for global state management:

- **Cart Context**: Shopping cart state and operations
- **Menu Context**: Menu data and loading states
- **Order Context**: Order processing and status
- **User Context**: Customer information

## 💳 Payment Integration

### Stripe Integration

The frontend integrates with Stripe for secure payment processing:

```typescript
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY!);

// Payment component example
const PaymentForm = () => {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!stripe || !elements) return;
    
    const cardElement = elements.getElement(CardElement);
    // Payment processing logic
  };
};
```

### Payment Methods

1. **Card Payments**: Stripe Elements integration
2. **Cash Orders**: SMS verification workflow
3. **Payment Status**: Real-time status updates

## 📱 Responsive Design

### Mobile-First Approach

The application is built with a mobile-first responsive design:

- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Touch-Friendly**: Large tap targets and gestures
- **Performance**: Optimized for mobile networks
- **Accessibility**: WCAG 2.1 AA compliance

### Key Responsive Features

- Collapsible navigation menu
- Responsive grid layouts
- Touch-optimized cart interactions
- Mobile-friendly forms
- Optimized image loading

## 🧪 Testing

### Testing Strategy

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Test Types

1. **Unit Tests**: Component logic and utilities
2. **Integration Tests**: Component interactions
3. **E2E Tests**: User workflows (future enhancement)

### Example Test

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { CartProvider } from '../context/CartContext';
import AddToCartButton from '../components/AddToCartButton';

test('adds item to cart when clicked', () => {
  render(
    <CartProvider>
      <AddToCartButton item={mockItem} />
    </CartProvider>
  );
  
  const button = screen.getByText('Add to Cart');
  fireEvent.click(button);
  
  expect(screen.getByText('Added to Cart')).toBeInTheDocument();
});
```

## 🚀 Build & Deployment

### Development Build

```bash
npm start
```

### Production Build

```bash
npm run build
```

Creates optimized production build in the `build/` directory.

### Docker Deployment

#### Development
```bash
docker build --target development -t steves-frontend:dev .
```

#### Production
```bash
docker build --target production -t steves-frontend:prod .
```

The production build uses Nginx to serve static files efficiently.

### Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: Image and CSS optimization
- **Caching**: Browser caching strategies
- **Bundle Analysis**: Webpack bundle analyzer

## 🔍 Development Tools

### Available Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject from Create React App (irreversible)
npm run eject
```

### Code Quality

- **ESLint**: Code linting and style enforcement
- **Prettier**: Code formatting (recommended)
- **TypeScript**: Static type checking
- **Husky**: Git hooks for quality gates (future enhancement)

### Browser Support

- **Production**: >0.2%, not dead, not op_mini all
- **Development**: Last 1 version of Chrome, Firefox, Safari

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check `REACT_APP_API_URL` environment variable
   - Verify backend server is running
   - Check CORS configuration

2. **Stripe Payment Issues**
   - Verify `REACT_APP_STRIPE_PUBLISHABLE_KEY`
   - Check Stripe dashboard for errors
   - Ensure HTTPS in production

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript errors
   - Verify environment variables

4. **Styling Issues**
   - Check Tailwind CSS configuration
   - Verify PostCSS setup
   - Clear browser cache

### Debug Mode

Enable React Developer Tools for debugging:

```bash
# Install React DevTools browser extension
# Enable in development mode
NODE_ENV=development npm start
```

## 📈 Future Enhancements

- [ ] Progressive Web App (PWA) features
- [ ] Real-time order tracking
- [ ] Push notifications
- [ ] Offline functionality
- [ ] Advanced animations
- [ ] Accessibility improvements
- [ ] Performance monitoring
- [ ] A/B testing framework
- [ ] Multi-language support
- [ ] Dark mode theme

## 🎯 Performance Metrics

### Core Web Vitals

- **Largest Contentful Paint (LCP)**: < 2.5s
- **First Input Delay (FID)**: < 100ms
- **Cumulative Layout Shift (CLS)**: < 0.1

### Bundle Size Targets

- **Initial Bundle**: < 250KB gzipped
- **Total JavaScript**: < 500KB gzipped
- **Images**: WebP format with lazy loading

---

**For more information, see the main project README or contact the development team.**