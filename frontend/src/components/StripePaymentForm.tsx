import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  CardElement,
  useStripe,
  useElements,
} from '@stripe/react-stripe-js';
import { Button } from './ui/button';

// Initialize Stripe
const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || '');

interface PaymentFormProps {
  onPaymentSuccess: (paymentMethodId: string) => void;
  onPaymentError: (error: string) => void;
  amount: number;
  disabled?: boolean;
}

const PaymentForm: React.FC<PaymentFormProps> = ({
  onPaymentSuccess,
  onPaymentError,
  amount,
  disabled = false,
}) => {
  const stripe = useStripe();
  const elements = useElements();
  const [processing, setProcessing] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    const cardElement = elements.getElement(CardElement);

    if (!cardElement) {
      return;
    }

    setProcessing(true);

    try {
      const { error, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
      });

      if (error) {
        onPaymentError(error.message || 'Payment failed');
      } else if (paymentMethod) {
        onPaymentSuccess(paymentMethod.id);
      }
    } catch (error) {
      onPaymentError('An unexpected error occurred');
    } finally {
      setProcessing(false);
    }
  };

  const cardElementOptions = {
    style: {
      base: {
        fontSize: '16px',
        color: '#424770',
        '::placeholder': {
          color: '#aab7c4',
        },
      },
      invalid: {
        color: '#9e2146',
      },
    },
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="p-4 border rounded-lg bg-white">
        <CardElement options={cardElementOptions} />
      </div>
      <Button
        type="submit"
        disabled={!stripe || processing || disabled}
        className="w-full"
      >
        {processing ? 'Processing...' : `Pay $${(amount / 100).toFixed(2)}`}
      </Button>
    </form>
  );
};

interface StripePaymentFormProps {
  onPaymentSuccess: (paymentMethodId: string) => void;
  onPaymentError: (error: string) => void;
  amount: number;
  disabled?: boolean;
  isProcessing?: boolean;
  customerName?: string;
  customerPhone?: string;
}

const StripePaymentForm: React.FC<StripePaymentFormProps> = (props) => {
  return (
    <Elements stripe={stripePromise}>
      <PaymentForm {...props} />
    </Elements>
  );
};

export default StripePaymentForm;