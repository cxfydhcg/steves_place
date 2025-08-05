import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { HomePage, StorePage, CheckoutPage } from "./pages";
import { CartProvider } from "./context/CartContext";
import "./App.css";

// Initialize Stripe
const stripePromise = loadStripe(
  process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || "pk_test_placeholder"
);

function App() {
  return (
    <CartProvider>
      <Elements stripe={stripePromise}>
        <Router>
          <div className="min-h-screen bg-background">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/store" element={<StorePage />} />
              <Route path="/checkout" element={<CheckoutPage />} />
            </Routes>
          </div>
        </Router>
      </Elements>
    </CartProvider>
  );
}

export default App;
