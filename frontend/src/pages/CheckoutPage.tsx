import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import {
  sendSMSVerification,
  verifySMSCode,
  processCardPayment,
  CustomerInfo,
} from "../api/checkoutAPI";
import { Button } from "../components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { FaArrowLeft, FaCheckCircle, FaShoppingCart } from "react-icons/fa";
import StripePaymentForm from "../components/StripePaymentForm";
import Notification from "../components/ui/notification";
import { useCart } from "../context/CartContext";
// Icon components
const ArrowLeftIcon = FaArrowLeft as React.ComponentType<
  React.SVGProps<SVGSVGElement>
>;
const CheckCircleIcon = FaCheckCircle as React.ComponentType<
  React.SVGProps<SVGSVGElement>
>;
const ShoppingCartIcon = FaShoppingCart as React.ComponentType<
  React.SVGProps<SVGSVGElement>
>;

// Using CartItem directly since it now includes special_instructions

const CheckoutPage: React.FC = () => {
  const { cart, clearCart } = useCart();
  const navigate = useNavigate();

  // Store cart items in local state to prevent flash when cart is cleared
  const [localCartItems, setLocalCartItems] = useState(() =>
    cart.map((item: any, index: number) => ({
      ...item,
      id: item.id || `item-${index}-${Date.now()}`,
    }))
  );

  // Use local cart items for display
  const cartItems = localCartItems;
  const [orderComplete, setOrderComplete] = useState(false);

  // Update local cart items when cart changes (but not when order is complete)
  useEffect(() => {
    if (!orderComplete && cart.length > 0) {
      setLocalCartItems(
        cart.map((item: any, index: number) => ({
          ...item,
          id: item.id || `item-${index}-${Date.now()}`,
        }))
      );
    }
  }, [cart, orderComplete]);

  console.log("Cart items:", cartItems);

  const [customerInfo, setCustomerInfo] = useState<CustomerInfo>({
    name: "",
    phone: "",
  });
  const [pickupTime, setPickupTime] = useState<string>("asap");
  const [showCustomTimeModal, setShowCustomTimeModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState<string>("");
  const [selectedHour, setSelectedHour] = useState<string>("");
  const [selectedMinute, setSelectedMinute] = useState<string>("");
  const [paymentMethod, setPaymentMethod] = useState("card");
  const [isProcessing, setIsProcessing] = useState(false);

  const [smsVerificationStep, setSmsVerificationStep] = useState<
    "none" | "sending" | "verifying"
  >("none");
  const [verificationCode, setVerificationCode] = useState("");
  const [smsMessage, setSmsMessage] = useState("");
  const [paymentError, setPaymentError] = useState<string | null>(null);
  const [notification, setNotification] = useState<{
    type: "success" | "error";
    title: string;
    message: string;
    isVisible: boolean;
  }>({ type: "success", title: "", message: "", isVisible: false });

  // Redirect to store if no cart data (but not if order is complete or processing)
  if (!orderComplete && !isProcessing && (!cart || cart.length === 0)) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardContent className="p-8 text-center">
            <ShoppingCartIcon className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <CardTitle className="text-2xl font-bold mb-4">
              Your cart is empty
            </CardTitle>
            <p className="text-muted-foreground mb-6">
              Add some items to your cart before proceeding to checkout.
            </p>
            <Button onClick={() => navigate("/store")} className="w-full">
              Go to Store
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Calculate base subtotal from cart items
  const baseSubtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.data.quantity,
    0
  );

  // For display purposes: show cash as "discounted" but actually the base price
  // Card payment shows 4% upcharge from base price
  const subtotal = baseSubtotal;
  const cashDiscount = paymentMethod === "cash" ? baseSubtotal * 0.04 : 0; // Show as discount but price stays same
  const cardFee = baseSubtotal * 0.04; // 4% upcharge for card
  const total =
    paymentMethod === "cash" ? baseSubtotal : baseSubtotal + cardFee;

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setCustomerInfo((prev) => ({ ...prev, [name]: value }));
  };

  // Generate available dates for the next 7 business days (excluding Sundays)
  const generateAvailableDates = () => {
    const dates = [];
    const now = new Date();
    let day = 0;

    // Keep adding days until we have 7 business days (excluding Sundays)
    while (dates.length < 7) {
      const date = new Date(now);
      date.setDate(now.getDate() + day);

      // Skip Sundays (0 = Sunday)
      if (date.getDay() !== 0) {
        dates.push({
          value: date.toISOString().split("T")[0],
          label: date.toLocaleDateString("en-US", {
            weekday: "long",
            month: "short",
            day: "numeric",
          }),
          date: date,
        });
      }

      day++;
    }

    return dates;
  };

  // Validate if selected time is within business hours and not in the past
  const isValidTime = (hour: number, minute: number, date: Date) => {
    // Business hours: 6:30 AM - 5:30 PM
    if (hour < 6 || hour > 17) return false;
    if (hour === 6 && minute < 30) return false;
    if (hour === 17 && minute > 30) return false;

    // Check if it's not in the past
    const selectedDateTime = new Date(date);
    selectedDateTime.setHours(hour, minute, 0, 0);
    const now = new Date();

    return selectedDateTime > now;
  };

  // Handle custom time confirmation
  const handleCustomTimeConfirm = () => {
    setShowCustomTimeModal(false);
    if (!selectedDate || !selectedHour || !selectedMinute) {
      showNotification(
        "error",
        "Invalid Time",
        "Please select a date, hour, and minute."
      );
      return;
    }

    const hour = parseInt(selectedHour);
    const minute = parseInt(selectedMinute);
    const date = new Date(selectedDate);

    if (!isValidTime(hour, minute, date)) {
      showNotification(
        "error",
        "Invalid Time",
        "Please select a time between 6:30 AM - 5:30 PM and not in the past."
      );
      return;
    }

    const customDateTime = new Date(date);
    customDateTime.setHours(hour, minute, 0, 0);

    setPickupTime(customDateTime.toISOString());
  };

  // Reset custom time selection
  const resetCustomTime = () => {
    setSelectedDate("");
    setSelectedHour("");
    setSelectedMinute("");
  };

  // Get display text for pickup time
  const getPickupTimeDisplay = () => {
    if (pickupTime === "asap") {
      return "As soon as possible";
    }
    const date = new Date(pickupTime);
    return (
      date.toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
      }) +
      " at " +
      date.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })
    );
  };

  // Add a helper function to get the pickup time value
  const getPickupTimeValue = () => {
    if (pickupTime === "asap") {
      // Return current time in ISO format when "as soon as possible" is selected
      return new Date().toISOString();
    }
    return pickupTime;
  };

  const showNotification = (
    type: "success" | "error",
    title: string,
    message: string
  ) => {
    setNotification({ type, title, message, isVisible: true });
  };

  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, isVisible: false }));
  };

  const handleSendSMS = async () => {
    if (!customerInfo.phone) {
      showNotification(
        "error",
        "Phone Required",
        "Please enter your phone number first."
      );
      return;
    }

    setSmsVerificationStep("sending");
    try {
      // Use getPickupTimeValue() instead of pickupTime directly
      const result = await sendSMSVerification(
        customerInfo,
        cartItems,
        total,
        getPickupTimeValue()
      );
      if (result.success) {
        setSmsVerificationStep("verifying");
        setSmsMessage(result.message);
      } else {
        showNotification(
          "error",
          "SMS Failed",
          result.message || "Failed to send SMS verification. Please try again."
        );
        setSmsVerificationStep("none");
      }
    } catch (error) {
      console.error("SMS sending failed:", error);
      showNotification(
        "error",
        "SMS Failed",
        "Failed to send SMS verification. Please try again."
      );
      setSmsVerificationStep("none");
    }
  };

  const handleVerifySMS = async () => {
    if (!verificationCode || verificationCode.length !== 6) {
      showNotification(
        "error",
        "Invalid Code",
        "Please enter a valid 6-digit verification code."
      );
      return;
    }

    setIsProcessing(true);
    try {
      // Use getPickupTimeValue() instead of pickupTime directly
      const result = await verifySMSCode(
        customerInfo,
        cartItems,
        total,
        verificationCode,
        getPickupTimeValue()
      );
      if (result.success) {
        showNotification(
          "success",
          "Order Placed!",
          result.message || "Your order has been successfully placed."
        );

        // Clear cart and set order complete immediately
        clearCart();
        setOrderComplete(true);
      } else {
        showNotification(
          "error",
          "Verification Failed",
          result.message || "Invalid verification code. Please try again."
        );
      }
    } catch (error) {
      console.error("SMS verification failed:", error);
      showNotification(
        "error",
        "Verification Failed",
        "Verification failed. Please try again."
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const submitStripeOrder = async (stripePaymentMethodId: string) => {
    console.log("cartItems", cartItems);
    try {
      // Use getPickupTimeValue() instead of pickupTime directly
      const result = await processCardPayment(
        customerInfo,
        cartItems,
        total,
        stripePaymentMethodId,
        getPickupTimeValue()
      );
      if (result.success) {
        // Clear cart from cookies after successful payment
        clearCart();
        setOrderComplete(true);
      } else {
        throw new Error(result.message || "Payment confirmation failed");
      }
    } catch (error) {
      console.error("Order processing failed:", error);
      throw error;
    }
  };

  const handleStripePaymentSuccess = async (paymentMethodId: string) => {
    setPaymentError(null);
    setIsProcessing(true);

    try {
      await submitStripeOrder(paymentMethodId);
    } catch (error) {
      console.error("Card payment processing failed:", error);
      setPaymentError("Card payment processing failed. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleStripePaymentError = (error: string) => {
    setPaymentError(error);
    showNotification(
      "error",
      "Payment Failed",
      error || "Payment processing failed. Please try again."
    );
  };

  const handleSubmitOrder = async (e: React.FormEvent) => {
    e.preventDefault();

    if (paymentMethod === "cash") {
      if (smsVerificationStep === "none") {
        await handleSendSMS();
      } else if (smsVerificationStep === "verifying") {
        await handleVerifySMS();
      }
    }
    // Card payment is now handled by the StripePaymentForm component
  };

  if (orderComplete) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardContent className="p-8 text-center">
            <CheckCircleIcon className="h-16 w-16 text-green-600 mx-auto mb-4" />
            <CardTitle className="text-2xl font-bold mb-4">
              Order Complete!
            </CardTitle>
            <p className="text-muted-foreground mb-6">
              <div className="flex items-center justify-center mb-6">
                <div className="text-black-900 text-lg font-bold tracking-wide drop-shadow-sm">
                  Estimated time:{" "}
                  <p className="text-muted-foreground mb-6">
                    Sandwich/EggSandwich: ~7-10 mins.
                    <br />
                    Other items: ~3-7 mins.
                  </p>
                  <span className="italic text-black-500 font-medium">
                    (depends on kitchen workload)
                  </span>
                </div>
              </div>
            </p>
            <div className="space-y-2">
              <Button onClick={() => navigate("/")} className="w-full">
                Return to Home
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate("/store")}
                className="w-full"
              >
                Continue Shopping
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header with Back Button */}
        <div className="flex items-center justify-between mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate("/store")}
            className="flex items-center gap-2"
          >
            <ArrowLeftIcon className="h-4 w-4" />
            Back to Store
          </Button>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <ShoppingCartIcon className="h-8 w-8 text-primary" />
            Checkout
          </h1>
          <div className="w-24" /> {/* Spacer for centering */}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Order Summary */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2">
                <ShoppingCartIcon className="h-6 w-6 text-primary" />
                Order Summary
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Cart Items */}
                <div className="space-y-3">
                  {cartItems.map((item, index) => {
                    // Extract item name based on item type
                    const getItemName = (item: any) => {
                      switch (item.itemType) {
                        case "Hotdog":
                          return item.data.dog_type || "Hotdog";
                        case "Sandwich":
                          return item.data.meat || "Sandwich";
                        case "EggSandwich":
                          return `${item.data.meat || "Egg"} Sandwich`;
                        case "Salad":
                          return item.data.choice || "Salad";
                        case "Side":
                          return item.data.name || "Side";
                        case "Drink":
                          return item.data.name || "Drink";
                        case "Combo":
                          return "Combo";
                        default:
                          return "Item";
                      }
                    };

                    // Extract toppings based on item type
                    const getToppings = (item: any) => {
                      if (
                        item.data.toppings &&
                        Array.isArray(item.data.toppings)
                      ) {
                        return item.data.toppings;
                      }
                      return [];
                    };

                    return (
                      <div
                        key={`${item.id}-${index}`}
                        className="flex justify-between items-start p-3 bg-muted/30 rounded-lg"
                      >
                        <div className="flex-1">
                          <h4 className="font-semibold text-sm">
                            {getItemName(item)}
                          </h4>
                          <div className="text-xs text-muted-foreground mt-1">
                            {getToppings(item).length > 0 && (
                              <div>
                                Toppings: {getToppings(item).join(", ")}
                              </div>
                            )}
                            <div>Quantity: {item.data.quantity}</div>
                            {item.data.special_instructions && (
                              <div>Notes: {item.data.special_instructions}</div>
                            )}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold">
                            ${(item.price * item.data.quantity).toFixed(2)}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            ${item.price.toFixed(2)} each
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Order Totals */}
                <div className="space-y-2 pt-4 border-t">
                  <div className="flex justify-between">
                    <span>Subtotal:</span>
                    <span>${subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-orange-600">
                    <span>Card Processing Fee (4%):</span>
                    <span>+${cardFee.toFixed(2)}</span>
                  </div>
                  {paymentMethod === "cash" && cashDiscount > 0 && (
                    <div className="flex justify-between text-green-600">
                      <span>Cash Discount (4%):</span>
                      <span>-${cashDiscount.toFixed(2)}</span>
                    </div>
                  )}

                  <div className="flex justify-between font-bold text-lg pt-2 border-t">
                    <span>Total:</span>
                    <span>${total.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Customer Information Form */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Customer Information</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmitOrder} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={customerInfo.name}
                    onChange={handleInputChange}
                    maxLength={100}
                    required
                    className="w-full px-3 py-2 border border-input rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={customerInfo.phone}
                    onChange={handleInputChange}
                    required
                    maxLength={10}
                    className="w-full px-3 py-2 border border-input rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Pickup Time
                  </label>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <input
                        type="radio"
                        id="asap"
                        name="pickupTimeOption"
                        checked={pickupTime === "asap"}
                        onChange={() => setPickupTime("asap")}
                        className="w-4 h-4 text-primary focus:ring-primary focus:ring-2"
                      />
                      <label
                        htmlFor="asap"
                        className="text-sm font-medium cursor-pointer"
                      >
                        As soon as possible
                      </label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input
                        type="radio"
                        id="custom"
                        name="pickupTimeOption"
                        checked={pickupTime !== "asap"}
                        onChange={() => {
                          setShowCustomTimeModal(true);
                          resetCustomTime();
                        }}
                        className="w-4 h-4 text-primary focus:ring-primary focus:ring-2"
                      />
                      <label
                        htmlFor="custom"
                        className="text-sm font-medium cursor-pointer"
                      >
                        Custom time:{" "}
                        {pickupTime !== "asap"
                          ? getPickupTimeDisplay()
                          : "Select time"}
                      </label>
                    </div>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Available 6:30 AM - 5:30 PM, Monday-Saturday only
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Payment Method
                  </label>
                  <div className="space-y-2">
                    {/* Cash Payment Option */}
                    <div className="relative overflow-hidden border-2 rounded-lg p-3 transition-all duration-200 hover:shadow-md hover:border-green-200 bg-gradient-to-r from-green-50 to-emerald-50">
                      <label className="flex items-start space-x-3 cursor-pointer">
                        <input
                          type="radio"
                          name="paymentMethod"
                          value="cash"
                          checked={paymentMethod === "cash"}
                          onChange={(e) => setPaymentMethod(e.target.value)}
                          className="mt-1 w-4 h-4 text-green-600 focus:ring-green-500 focus:ring-2"
                        />
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <div>
                              <h3 className="text-base font-semibold text-gray-900">
                                Pay in Store with Cash
                              </h3>
                              <div className="flex items-center space-x-2">
                                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                  Save 4%
                                </span>
                              </div>
                            </div>
                          </div>
                          <p className="text-xs text-gray-600 mb-2">
                            SMS verification required • Pay when you pick up
                            your order
                          </p>
                          <div className="flex items-center space-x-1">
                            <span className="text-xs text-gray-500">
                              Powered by
                            </span>
                            <svg
                              className="h-3 w-auto"
                              viewBox="0 0 80 24"
                              fill="none"
                            >
                              <rect
                                width="80"
                                height="24"
                                rx="6"
                                fill="#F22F46"
                              />
                              <text
                                x="40"
                                y="16"
                                textAnchor="middle"
                                fill="white"
                                fontSize="12"
                                fontWeight="bold"
                              >
                                Twilio
                              </text>
                            </svg>
                          </div>
                        </div>
                      </label>
                    </div>

                    {/* Card Payment Option */}
                    <div className="relative overflow-hidden border-2 rounded-lg p-3 transition-all duration-200 hover:shadow-md hover:border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50">
                      <label className="flex items-start space-x-3 cursor-pointer">
                        <input
                          type="radio"
                          name="paymentMethod"
                          value="card"
                          checked={paymentMethod === "card"}
                          onChange={(e) => setPaymentMethod(e.target.value)}
                          className="mt-1 w-4 h-4 text-blue-600 focus:ring-blue-500 focus:ring-2"
                        />
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <div>
                              <h3 className="text-base font-semibold text-gray-900">
                                Pay with Card
                              </h3>
                              <div className="flex items-center space-x-2">
                                <p className="text-xs text-gray-600">
                                  Secure online payment
                                </p>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="text-xs text-gray-600">
                              Accepted cards:
                            </span>
                            <div className="flex items-center space-x-1">
                              <svg
                                className="h-5 w-auto"
                                viewBox="0 0 48 30"
                                fill="none"
                              >
                                <rect
                                  width="48"
                                  height="30"
                                  rx="6"
                                  fill="#1A1F71"
                                />
                                <text
                                  x="24"
                                  y="20"
                                  textAnchor="middle"
                                  fill="white"
                                  fontSize="10"
                                  fontWeight="bold"
                                >
                                  VISA
                                </text>
                              </svg>
                              <svg
                                className="h-5 w-auto"
                                viewBox="0 0 48 30"
                                fill="none"
                              >
                                <rect
                                  width="48"
                                  height="30"
                                  rx="6"
                                  fill="#EB001B"
                                />
                                <circle cx="18" cy="15" r="10" fill="#FF5F00" />
                                <circle cx="30" cy="15" r="10" fill="#F79E1B" />
                              </svg>
                              <svg
                                className="h-5 w-auto"
                                viewBox="0 0 48 30"
                                fill="none"
                              >
                                <rect
                                  width="48"
                                  height="30"
                                  rx="6"
                                  fill="#006FCF"
                                />
                                <text
                                  x="24"
                                  y="20"
                                  textAnchor="middle"
                                  fill="white"
                                  fontSize="8"
                                  fontWeight="bold"
                                >
                                  AMEX
                                </text>
                              </svg>
                              <svg
                                className="h-5 w-auto"
                                viewBox="0 0 48 30"
                                fill="none"
                              >
                                <rect
                                  width="48"
                                  height="30"
                                  rx="6"
                                  fill="#FF6000"
                                />
                                <text
                                  x="24"
                                  y="20"
                                  textAnchor="middle"
                                  fill="white"
                                  fontSize="7"
                                  fontWeight="bold"
                                >
                                  DISCOVER
                                </text>
                              </svg>
                            </div>
                          </div>

                          {/* Stripe Payment Form */}
                          {paymentMethod === "card" && (
                            <div className="bg-white border border-gray-200 rounded p-2 mb-2">
                              <h4 className="text-xs font-medium text-gray-900 mb-2">
                                Card Information
                              </h4>
                              <StripePaymentForm
                                onPaymentSuccess={handleStripePaymentSuccess}
                                onPaymentError={handleStripePaymentError}
                                isProcessing={isProcessing}
                                amount={total}
                                customerName={customerInfo.name}
                                customerPhone={customerInfo.phone}
                              />
                              {paymentError && (
                                <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
                                  <p className="text-xs text-red-600">
                                    {paymentError}
                                  </p>
                                </div>
                              )}
                            </div>
                          )}

                          <div className="flex items-center justify-end space-x-1 py-1">
                            <span className="text-xs text-gray-600">
                              Secured by
                            </span>
                            <svg
                              className="h-4 w-auto"
                              viewBox="0 0 100 30"
                              fill="none"
                            >
                              <rect
                                width="100"
                                height="30"
                                rx="6"
                                fill="#635BFF"
                              />
                              <text
                                x="50"
                                y="20"
                                textAnchor="middle"
                                fill="white"
                                fontSize="15"
                                fontWeight="bold"
                              >
                                stripe
                              </text>
                            </svg>
                          </div>
                        </div>
                      </label>
                    </div>
                  </div>
                </div>

                {paymentMethod === "cash" &&
                  smsVerificationStep === "verifying" && (
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          SMS Verification Code *
                        </label>
                        <input
                          type="text"
                          value={verificationCode}
                          onChange={(e) =>
                            setVerificationCode(
                              e.target.value.replace(/\D/g, "").slice(0, 6)
                            )
                          }
                          placeholder="Enter 6-digit code"
                          maxLength={6}
                          className="w-full px-3 py-2 border border-input rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-center text-lg font-mono"
                        />
                        {smsMessage && (
                          <p className="text-sm text-green-600 mt-1">
                            {smsMessage}
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                {paymentMethod === "cash" && (
                  <Button
                    type="submit"
                    disabled={
                      isProcessing ||
                      !customerInfo.name.trim() ||
                      !customerInfo.phone.trim() ||
                      (paymentMethod === "cash" &&
                        smsVerificationStep === "sending") ||
                      (smsVerificationStep === "verifying" &&
                        !verificationCode.trim())
                    }
                    className="w-full h-12 text-base font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                    size="lg"
                  >
                    {isProcessing ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        <span>Confirming order...</span>
                      </div>
                    ) : smsVerificationStep === "sending" ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        <span>Sending SMS...</span>
                      </div>
                    ) : !customerInfo.name.trim() ||
                      !customerInfo.phone.trim() ? (
                      "Complete customer information"
                    ) : smsVerificationStep === "none" ? (
                      "Send SMS Verification"
                    ) : smsVerificationStep === "verifying" ? (
                      !verificationCode.trim() ? (
                        "Enter verification code"
                      ) : (
                        `Verify & Place Order - $${total.toFixed(2)}`
                      )
                    ) : (
                      `Place Order - $${total.toFixed(2)}`
                    )}
                  </Button>
                )}

                {paymentMethod === "cash" &&
                  smsVerificationStep === "verifying" && (
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => {
                        setSmsVerificationStep("none");
                        setVerificationCode("");
                        setSmsMessage("");
                      }}
                      className="w-full"
                    >
                      Resend SMS Code
                    </Button>
                  )}
              </form>
            </CardContent>
          </Card>
        </div>
      </div>

      <Notification
        type={notification.type}
        title={notification.title}
        message={notification.message}
        isVisible={notification.isVisible}
        onClose={hideNotification}
      />

      {/* Custom Time Selection Modal */}
      {showCustomTimeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold mb-4">Select Pickup Time</h3>

            {/* Date Selection */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">
                Select Date
              </label>
              <div className="grid grid-cols-1 gap-2 max-h-40 overflow-y-auto">
                {generateAvailableDates().map((dateOption) => (
                  <button
                    key={dateOption.value}
                    type="button"
                    onClick={() => setSelectedDate(dateOption.value)}
                    className={`p-2 text-left rounded border ${
                      selectedDate === dateOption.value
                        ? "bg-primary text-white border-primary"
                        : "bg-gray-50 border-gray-200 hover:bg-gray-100"
                    }`}
                  >
                    {dateOption.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Time Selection */}
            {selectedDate && (
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">
                  Select Time
                </label>
                <div className="flex space-x-2">
                  <div className="flex-1">
                    <label className="block text-xs text-gray-600 mb-1">
                      Hour
                    </label>
                    <select
                      value={selectedHour}
                      onChange={(e) => setSelectedHour(e.target.value)}
                      className="w-full px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="">--</option>
                      {Array.from({ length: 12 }, (_, i) => {
                        const hour = i + 6; // 6 AM to 5 PM (17)
                        if (hour > 17) return null;
                        return (
                          <option key={hour} value={hour}>
                            {hour > 12 ? hour - 12 : hour === 0 ? 12 : hour}{" "}
                            {hour >= 12 ? "PM" : "AM"}
                          </option>
                        );
                      }).filter(Boolean)}
                    </select>
                  </div>
                  <div className="flex-1">
                    <label className="block text-xs text-gray-600 mb-1">
                      Minute
                    </label>
                    <select
                      value={selectedMinute}
                      onChange={(e) => setSelectedMinute(e.target.value)}
                      className="w-full px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="">--</option>
                      {Array.from({ length: 60 }, (_, i) => (
                        <option key={i} value={i}>
                          {i.toString().padStart(2, "0")}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Business hours: 6:30 AM - 5:30 PM
                </p>
              </div>
            )}

            {/* Modal Actions */}
            <div className="flex space-x-2 justify-end">
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  setShowCustomTimeModal(false);
                  resetCustomTime();
                }}
              >
                Cancel
              </Button>
              <Button
                type="button"
                onClick={handleCustomTimeConfirm}
                disabled={!selectedDate || !selectedHour || !selectedMinute}
              >
                Confirm
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CheckoutPage;
