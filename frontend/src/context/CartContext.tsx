import React, {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";
import { CartItem } from "../utils/Schema";

// Add custom deep equality function
const isEqual = (obj1: any, obj2: any): boolean => {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
};

type CartContextType = {
  cart: CartItem[];
  addToCart: (newItem: CartItem) => void;
  removeFromCart: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  getCart: () => CartItem[];
  getTotalPrice: () => number;
};

const CartContext = createContext<CartContextType | undefined>(undefined);

// LocalStorage key
const CART_STORAGE_KEY = "steve's place hotdog cart";

export const CartProvider = ({ children }: { children: ReactNode }) => {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [totalPrice, setTotalPrice] = useState<number>(0);
  // Load cart from localStorage on mount
  useEffect(() => {
    const cart = localStorage.getItem(CART_STORAGE_KEY);
    try {
      if (cart) {
        setCart(JSON.parse(cart));
      }
    } catch (error) {
      console.error("Error loading cart from localStorage:", error);
    }
  }, []);

  // Save cart to localStorage when it changes
  useEffect(() => {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    const newTotalPrice = cart.reduce(
      (total, item) => total + item.price * item.data.quantity,
      0
    );
    setTotalPrice(newTotalPrice);
    console.log("totalPrice", newTotalPrice);
    console.log("cart", cart);
  }, [cart]);

  const addToCart = (newItem: CartItem) => {
    setCart((prevCart) => {
      const existIndex = prevCart.findIndex((ci) => ci.id === newItem.id);
      if (existIndex !== -1) {
        // exist item, increment the data's quantity
        const updatedCart = [...prevCart];
        updatedCart[existIndex].data.quantity += 1;
        return updatedCart;
      } else {
        // Don't auto-open cart when first item is added
        return [...prevCart, newItem];
      }
    });
  };

  const removeFromCart = (id: string) => {
    console.log("removeFromCart called for id:", id);
    updateQuantity(id, -1);
  };

  const updateQuantity = (id: string, quantity: number) => {
    setCart((prevCart) => {
      const existIndex = prevCart.findIndex((ci) => ci.id === id);
      if (existIndex !== -1) {
        const updatedCart = [...prevCart];
        updatedCart[existIndex].data.quantity += quantity;
        if (updatedCart[existIndex].data.quantity <= 0) {
          updatedCart.splice(existIndex, 1);
        }
        return updatedCart;
      }
      return cart;
    });
  };

  const clearCart = () => {
    setCart([]);
  };

  const getCart = () => {
    return cart;
  };

  const getTotalPrice = () => {
    return totalPrice;
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        getCart,
        getTotalPrice,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};
