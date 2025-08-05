import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { ShoppingCartIcon, MinusIcon, TrashIcon, XIcon } from "lucide-react";
import { useCart } from "../context/CartContext";

interface CartProps {
  isCartOpen: boolean;
  setIsCartOpen: (open: boolean) => void;
}

const Cart: React.FC<CartProps> = ({ isCartOpen, setIsCartOpen }) => {
  const navigate = useNavigate();
  const { getCart, getTotalPrice, removeFromCart, clearCart } = useCart();
  const [showClearConfirmation, setShowClearConfirmation] = useState(false);

  const handleClearCart = () => {
    clearCart();
    setShowClearConfirmation(false);
  };

  return (
    <>
      {/* Floating Cart Button */}
      {getCart().length > 0 && (
        <div className="fixed bottom-6 right-6 sm:bottom-8 sm:right-8 z-40">
          <Button
            onClick={() => setIsCartOpen(!isCartOpen)}
            className="h-16 w-16 sm:h-18 sm:w-18 rounded-full transition-colors duration-200"
            variant="secondary"
            size="sm"
          >
            <div className="relative">
              <ShoppingCartIcon className="h-7 w-7 sm:h-8 sm:w-8" />
              <Badge
                variant="destructive"
                className="absolute -top-3 -right-3 sm:-top-4 sm:-right-4 h-6 w-6 sm:h-7 sm:w-7 rounded-full p-0 flex items-center justify-center text-sm font-bold"
              >
                {getCart().length}
              </Badge>
            </div>
          </Button>
        </div>
      )}

      {/* Mobile Cart Drawer */}
      {isCartOpen && getCart().length > 0 && (
        <>
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 transition-opacity duration-500"
            onClick={() => setIsCartOpen(false)}
          />
          <div className="fixed inset-0 sm:right-0 sm:left-auto h-full w-full sm:max-w-md bg-background shadow-2xl z-50 transform transition-transform duration-500 animate-in slide-in-from-right sm:border-l-4 border-primary/20">
            <div className="p-4 sm:p-8 h-full flex flex-col">
              {/* Header */}
              <div className="flex justify-between items-center mb-4 sm:mb-8 pb-4 sm:pb-6 border-b-2 border-gradient-to-r from-primary/20 to-orange-500/20">
                <div className="space-y-2">
                  <h3 className="text-xl sm:text-2xl font-bold flex items-center gap-2 sm:gap-3">
                    <div className="p-2 rounded-full bg-gradient-to-r from-primary/20 to-orange-500/20">
                      <ShoppingCartIcon className="h-6 w-6 text-primary" />
                    </div>
                    Your Cart
                  </h3>
                  <p className="text-base text-muted-foreground font-medium">
                    {getCart().length} items •{" "}
                    <span className="text-primary font-bold">
                      ${getTotalPrice().toFixed(2)}
                    </span>
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsCartOpen(false)}
                  className="h-12 w-12 rounded-full hover:bg-destructive/10 hover:text-destructive transition-colors duration-300"
                >
                  <XIcon className="h-6 w-6" />
                </Button>
              </div>

              {/* Cart Items */}
              <div className="flex-1 overflow-y-auto space-y-2 mb-3 pr-2">
                {getCart().map((item, index) => (
                  <Card
                    key={`${item.id}-${index}-${JSON.stringify(item.data || {})}`}
                    className="group hover:shadow-md hover:shadow-primary/10 transition-all duration-200 border border-border/50 hover:border-primary/60 rounded-lg overflow-hidden bg-background backdrop-blur-sm hover:scale-[1.01] transform-gpu"
                  >
                    {/* Header */}
                    <div className="pb-1 pt-2 px-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors duration-300 leading-tight">
                            {item.itemType}
                          </h4>
                        </div>
                        <div className="ml-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeFromCart(item.id)}
                            className="h-6 w-6 p-0 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-full transition-colors duration-300"
                          >
                            <MinusIcon className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    </div>

                    {/* Content */}
                    <div className="pt-0 px-3 pb-1">
                      <div className="space-y-2">
                        {/* Item details */}
                        <div className="space-y-1 bg-muted/30 rounded-lg p-2">
                          {Object.entries(item.data || {}).map(
                            ([key, value]) => {
                              if (
                                key === "quantity" ||
                                key === "special_instructions" ||
                                !value
                              )
                                return null;
                              return (
                                <div
                                  key={key}
                                  className="flex justify-between items-center text-xs"
                                >
                                  <span className="text-muted-foreground capitalize font-normal text-xs">
                                    {key.replace(/_/g, " ")}:
                                  </span>
                                  <span className="font-medium text-primary text-xs">
                                    {Array.isArray(value)
                                      ? value.join(", ")
                                      : typeof value === "object" &&
                                          value !== null
                                        ? (() => {
                                            // Handle side object
                                            if (key.toLowerCase() === "side") {
                                              const sideObj = value as any;
                                              let result = sideObj.name || "";
                                              if (sideObj.chips_type) {
                                                result += ` (${sideObj.chips_type})`;
                                              } else if (sideObj.size) {
                                                result += ` (${sideObj.size})`;
                                              }
                                              return result;
                                            }
                                            // Handle drink object
                                            if (key.toLowerCase() === "drink") {
                                              const drinkObj = value as any;
                                              let result = drinkObj.name || "";
                                              if (drinkObj.size) {
                                                result += ` (${drinkObj.size})`;
                                              }
                                              return result;
                                            }
                                            // Fallback for other objects
                                            return JSON.stringify(value);
                                          })()
                                        : String(value)}
                                  </span>
                                </div>
                              );
                            }
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Footer */}
                    <div className="pt-1 px-3 pb-2">
                      <div className="space-y-2">
                        {/* Quantity and pricing */}
                        <div className="flex justify-between items-center">
                          <div className="flex items-center gap-2">
                            <div className="flex items-center gap-1 bg-primary/10 rounded-full px-2 py-0.5">
                              <span className="text-xs font-bold text-primary">
                                {item.data.quantity}x
                              </span>
                            </div>
                            <div className="text-xs text-muted-foreground font-bold">
                              @ ${item.price.toFixed(2)} each
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-sm font-bold text-foreground">
                              $
                              {((item.price || 0) * item.data.quantity).toFixed(
                                2
                              )}
                            </div>
                            <div className="text-xs text-muted-foreground/80 font-medium">
                              Subtotal
                            </div>
                          </div>
                        </div>

                        {/* Special instructions */}
                        {item.data.special_instructions && (
                          <div className="bg-muted/20 border border-border/40 rounded-lg p-2">
                            <div className="flex items-start gap-2">
                              <div className="w-1.5 h-1.5 rounded-full bg-primary/60 mt-1 flex-shrink-0"></div>
                              <div className="flex-1">
                                <span className="text-xs font-bold text-foreground">
                                  Special Instructions
                                </span>
                                <p className="text-xs text-muted-foreground/80 mt-0.5 leading-relaxed font-medium">
                                  {item.data.special_instructions}
                                </p>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </Card>
                ))}
              </div>

              {/* Footer */}
              <div className="space-y-4 sm:space-y-6 pt-4 sm:pt-6 border-t-2 border-gradient-to-r from-primary/20 to-orange-500/20">
                <div className="bg-primary/10 rounded-xl sm:rounded-2xl p-4 sm:p-6">
                  <div className="flex justify-between items-center">
                    <span className="text-lg sm:text-xl font-bold text-foreground">
                      Total:
                    </span>
                    <span className="text-2xl sm:text-3xl font-bold text-primary">
                      ${getTotalPrice().toFixed(2)}
                    </span>
                  </div>
                </div>
                <div className="space-y-4">
                  <Button
                    variant="outline"
                    onClick={() => setShowClearConfirmation(true)}
                    className="w-full h-10 sm:h-12 text-sm sm:text-base rounded transition-colors duration-200"
                    size="sm"
                  >
                    <TrashIcon className="mr-2 h-5 w-5" />
                    Clear Cart
                  </Button>
                  <Button
                    onClick={() => {
                      setIsCartOpen(false);
                      navigate("/checkout", { state: { cartData: getCart() } });
                    }}
                    className="w-full h-12 sm:h-14 text-base sm:text-lg font-bold rounded transition-colors duration-200 bg-green-600 hover:bg-green-700 text-white border-none shadow-lg"
                    variant="secondary"
                    size="lg"
                  >
                    🛒 Proceed to Checkout
                  </Button>
                </div>
              </div>
              {/* Clear Cart Confirmation Dialog */}
              {showClearConfirmation && (
                <>
                  <div
                    className="fixed inset-0 bg-black/70 backdrop-blur-md z-60 transition-opacity duration-300"
                    onClick={() => setShowClearConfirmation(false)}
                  />
                  <div className="fixed inset-0 flex items-center justify-center z-60 p-4">
                    <Card className="w-full max-w-md bg-background border-2 border-primary/20 shadow-2xl">
                      <div className="p-6 space-y-4">
                        <div className="text-center space-y-2">
                          <div className="mx-auto w-12 h-12 bg-destructive/10 rounded-full flex items-center justify-center">
                            <TrashIcon className="h-6 w-6 text-destructive" />
                          </div>
                          <h3 className="text-lg font-bold text-foreground">
                            Clear Cart?
                          </h3>
                          <p className="text-sm text-muted-foreground">
                            Are you sure you want to remove all items from your
                            cart? This action cannot be undone.
                          </p>
                        </div>
                        <div className="flex gap-3">
                          <Button
                            variant="outline"
                            onClick={() => setShowClearConfirmation(false)}
                            className="flex-1"
                          >
                            Cancel
                          </Button>
                          <Button
                            variant="destructive"
                            onClick={handleClearCart}
                            className="flex-1"
                          >
                            Clear Cart
                          </Button>
                        </div>
                      </div>
                    </Card>
                  </div>
                </>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default Cart;
