// API functions for the checkout page
import { CartItem } from "../utils/Schema";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

export interface CustomerInfo {
  name: string;
  phone: string;
}

export interface OrderData {
  items: CartItem[];
  customer: CustomerInfo;
  paymentMethod: string;
  total: number;
  subtotal?: number;
  tax?: number;
  orderDate?: string;
}

export interface OrderResponse {
  success: boolean;
  orderId?: string;
  message: string;
  estimatedDelivery?: string;
}

export interface PaymentInfo {
  method: string;
  cardNumber?: string;
  expiryDate?: string;
  cvv?: string;
  cardholderName?: string;
}

/**
 * Send SMS verification code for cash payment
 * Updated to match backend endpoint: /api/checkout/send_sms_verification
 */
export const sendSMSVerification = async (
  customerInfo: CustomerInfo,
  orderItems: CartItem[],
  orderPrice: number,
  pickupTime?: string
): Promise<{ success: boolean; message: string }> => {
  try {
    console.log(
      "Sending SMS verification to:",
      `${API_BASE_URL}/api/checkout/send_sms_verification`
    );
    console.log("Request data:", {
      customerInfo,
      orderItems,
      orderPrice,
      pickupTime,
    });

    const formData = new FormData();
    formData.append("customer_name", customerInfo.name);
    formData.append("phone_number", customerInfo.phone);
    formData.append(
      "order_items",
      JSON.stringify(
        orderItems.map((item) => ({
          type: item.itemType,
          ...item.data,
        }))
      )
    );
    formData.append("order_price", orderPrice.toString());
    if (pickupTime) {
      formData.append("pickup_at", pickupTime); // Changed from 'pickup_time' to 'pickup_at'
    }

    const response = await fetch(
      `${API_BASE_URL}/api/checkout/send_sms_verification`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.error || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    console.log("SMS verification response:", data);

    return {
      success: data.success || false,
      message: data.message || "SMS verification code sent successfully",
    };
  } catch (error) {
    console.error("Error sending SMS verification:", error);
    console.error("API Base URL:", API_BASE_URL);
    throw error;
  }
};

/**
 * Verify SMS code for cash payment
 * Updated to match backend endpoint: /api/checkout/verify_sms
 */
export const verifySMSCode = async (
  customerInfo: CustomerInfo,
  orderItems: CartItem[],
  orderPrice: number,
  smsCode: string,
  pickupTime?: string
): Promise<{ success: boolean; message: string }> => {
  console.log("Verifying SMS code:", {
    customerInfo,
    orderItems,
    orderPrice,
    smsCode,
  });
  try {
    const formData = new FormData();
    formData.append("customer_name", customerInfo.name);
    formData.append("phone_number", customerInfo.phone);
    formData.append("sms_code", smsCode);
    formData.append(
      "order_items",
      JSON.stringify(
        orderItems.map((item) => ({
          type: item.itemType,
          ...item.data,
        }))
      )
    );
    formData.append("order_price", orderPrice.toString());
    if (pickupTime) {
      formData.append("pickup_at", pickupTime); // Changed from 'pickup_time' to 'pickup_at'
    }

    const response = await fetch(`${API_BASE_URL}/api/checkout/verify_sms`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.error || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    return {
      success: data.success || false,
      message: data.message || "Verification failed",
    };
  } catch (error) {
    console.error("Error verifying SMS code:", error);
    throw error;
  }
};

/**
 * Process card payment with Stripe
 * Updated to use only payment method ID
 */
export const processCardPayment = async (
  customerInfo: CustomerInfo,
  orderItems: CartItem[],
  orderPrice: number,
  paymentMethodId: string,
  pickupTime?: string
): Promise<{ success: boolean; message: string }> => {
  try {
    console.log("Processing card payment:", {
      customerInfo,
      orderItems,
      orderPrice,
      paymentMethodId,
    });

    const formData = new FormData();
    formData.append("customer_name", customerInfo.name);
    formData.append("phone_number", customerInfo.phone);
    formData.append("payment_method_id", paymentMethodId);
    formData.append(
      "order_items",
      JSON.stringify(
        orderItems.map((item) => ({
          type: item.itemType,
          // Quantity is included in item.data spread below
          // Pass through the actual data structure
          ...item.data,
        }))
      )
    );
    formData.append("order_price", orderPrice.toString());
    if (pickupTime) {
      formData.append("pickup_at", pickupTime); // Changed from 'pickup_time' to 'pickup_at'
    }

    const response = await fetch(
      `${API_BASE_URL}/api/checkout/confirm_payment`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.error || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    console.log("Card payment response:", data);
    return {
      success: data.success || false,
      message: data.message || "Payment processing failed",
    };
  } catch (error) {
    console.error("Error processing card payment:", error);
    throw error;
  }
};

/**
 * Get order details by ID
 * New function to match backend endpoint: /api/checkout/order/<id>
 */
export const getOrder = async (
  orderId: number
): Promise<{ success: boolean; order?: any; error?: string }> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/checkout/order/${orderId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.error || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    return {
      success: data.success || false,
      order: data.order,
    };
  } catch (error) {
    console.error("Error getting order:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
};

/**
 * Format price for display
 */
export const formatPrice = (price: number): string => {
  return `$${price.toFixed(2)}`;
};
