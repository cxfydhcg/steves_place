import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { UtensilsIcon, XIcon } from "lucide-react";
import {
  Category,
  CartItem,
  EggSandwichBread,
  BottleDrink,
  SideName,
  Chips,
  SandwichBread,
  DrinkSize,
  SandwichSize,
  HotdogSchema,
  SandwichSchema,
  EggSandwichSchema,
  SideSchema,
  SaladSchema,
  DrinkSchema,
  ComboSchema,
  ComboDrinkSchema,
  ComboSideSchema,
} from "../utils/Schema";
import { getCustomizeData } from "../api/foodCustomizeAPI";
import { useCart } from "../context/CartContext";
interface SelectionState {
  [key: string]: string | string[];
}

interface selectedItem {
  name: string;
  category: Category;
}

interface FoodCustomizeProps {
  selectedItem: selectedItem;
  isOpen: boolean;
  onClose: () => void;
  menuData: any;
}

const FoodCustomize: React.FC<FoodCustomizeProps> = ({
  selectedItem,
  isOpen,
  onClose,
  menuData,
}) => {
  const {
    addToCart,
    getCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    getTotalPrice,
  } = useCart();
  const [customizeData, setCustomizeData] = useState<any | null>(null);
  const [selections, setSelections] = useState<SelectionState>({});
  const [errors, setErrors] = useState<string[]>([]);
  const [specialInstructions, setSpecialInstructions] = useState<string>("");
  const [quantity, setQuantity] = useState<number>(1);
  const [price, setPrice] = useState<number>(0);
  const [cartItemData, setCartItemData] = useState<
    | HotdogSchema
    | SandwichSchema
    | EggSandwichSchema
    | SaladSchema
    | SideSchema
    | DrinkSchema
    | ComboSchema
  >(
    {} as
      | HotdogSchema
      | SandwichSchema
      | EggSandwichSchema
      | SaladSchema
      | SideSchema
      | DrinkSchema
      | ComboSchema
  );
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  useEffect(() => {
    getCustomizeData(selectedItem.category).then((data) => {
      // If its bottled soda, it does not have any customize options
      if (
        selectedItem.category === Category.DRINK &&
        selectedItem.name === BottleDrink.BOTTLED_SODA
      ) {
        data = {};
      }
      if (selectedItem.category === Category.SIDE) {
        if (selectedItem.name === SideName.CHIPS) {
          // Only keep the chip key value in the data
          data = {
            Chips: data["Chips"],
          };
        } else {
          // Remove the chip key from the data
          data = {
            Size: data["Size"],
          };
        }
      }
      setCustomizeData(data);
      // Initialize selections with default values
      const initialSelections: SelectionState = {};
      Object.entries(data).forEach(([key, value]) => {
        if (isMultiSelect(key)) {
          initialSelections[key] = [];
        } else {
          initialSelections[key] = "";
        }
      });
      setSelections(initialSelections);
    });
  }, [selectedItem]);

  // Update price whenever selections, customizeData, or menuData change
  useEffect(() => {
    setPrice(parseFloat(calculateTotalPrice()));
  }, [selections, quantity]);

  // Update cartItemData whenever selections change
  useEffect(() => {
    const updatedData: any = {
      quantity: quantity,
      special_instructions: specialInstructions || undefined,
    };
    if (selectedItem.category === Category.HOTDOG) {
      updatedData.dog_type = selectedItem.name;
    }
    // If category is sandwich set the meat to be the name
    if (selectedItem.category === Category.SANDWICH) {
      updatedData.meat = selectedItem.name;
    }
    // If the item is a salad, set the choice to the selected item name
    if (selectedItem.category === Category.SALAD) {
      updatedData.choice = selectedItem.name;
    }

    // If the item is a bottled soda, set the size to bottle and name to the selected item name
    if (selectedItem.name === BottleDrink.BOTTLED_SODA) {
      updatedData.size = DrinkSize.BOTTLE;
      updatedData.name = selectedItem.name;
      // Set cart item data and return early for bottled soda
      setCartItemData(updatedData);
      return;
    }
    console.log(selections);
    // If the item is a combo, set the side and drink data
    if (selectedItem.category === Category.COMBO) {
      updatedData.side = {} as ComboSideSchema;
      updatedData.drink = {} as ComboDrinkSchema;

      updatedData.side.name = selections["Side"];
      if (selections["Side"] === SideName.CHIPS) {
        updatedData.side.chips_type = selections["Chip Type"];
      } else {
        updatedData.side.size = "Regular";
      }

      if (selections["Bottled Soda"] === BottleDrink.BOTTLED_SODA) {
        updatedData.drink.name = selections["Bottled Soda"];
      } else {
        updatedData.drink.name = selections["Drink"];
        updatedData.drink.size = selections["Drink Size"];
      }

      // Set cart item data and return early for combos
      setCartItemData(updatedData);
      return;
    }

    // Map selections to the appropriate schema fields based on category
    Object.entries(selections).forEach(([key, value]) => {
      if (
        value &&
        (typeof value === "string" ||
          (Array.isArray(value) && value.length > 0))
      ) {
        switch (key.toLowerCase()) {
          case "size":
            updatedData.size = value;
            // If the item is a drink, set the name to the selected item name
            if (
              selectedItem.category === Category.DRINK ||
              selectedItem.category === Category.SIDE
            ) {
              updatedData.name = selectedItem.name;
            }
            break;
          case "bread":
            updatedData.bread = value;
            break;
          case "bread prep":
            updatedData.toast = value === "Toasted";
            updatedData.grilled = value === "Grilled";
            break;
          case "meat":
            updatedData.meat = value;

            break;
          case "cheese":
            updatedData.cheese = value;
            break;
          case "toppings":
            updatedData.toppings = Array.isArray(value) ? value : [value];
            break;
          case "dressing":
            updatedData.dressing = value;
            break;
          case "add ons":
            updatedData.add_ons = Array.isArray(value) ? value : [value];
            break;

          case "chips":
            updatedData.name = selectedItem.name;
            updatedData.chips_type = selections["Chips"];
            break;
          default:
            // Handle other fields generically
            updatedData[key.toLowerCase().replace(" ", "_")] = value;
        }
      }
    });

    // Set cart item data once after processing all selections
    setCartItemData(updatedData);
  }, [selections, quantity, specialInstructions]);

  const isOptional = (key: string) => {
    if (Category.SALAD === selectedItem.category && key === "Toppings") {
      return false;
    }
    if (Category.COMBO === selectedItem.category && key === "Side") {
      return false;
    }
    if (
      Category.SIDE === selectedItem.category &&
      selectedItem.name === SideName.CHIPS &&
      key === "Chips"
    ) {
      return false;
    }
    if (
      key === "Size" ||
      key === "Bread" ||
      key === "Bread Prep" ||
      key === "Egg"
    ) {
      return false;
    }
    return true;
  };

  const isMultiSelect = (key: string) => {
    return key === "Toppings" || key === "Add Ons";
  };

  const handleSingleSelection = (category: string, value: string) => {
    setSelections((prev) => {
      // If the same value is clicked again, deselect it only if the field is optional
      const currentValue = prev[category];
      const isOptionalField = isOptional(category);
      const shouldDeselect = currentValue === value && isOptionalField;
      const newValue = shouldDeselect ? "" : value;

      const newSelections = {
        ...prev,
        [category]: newValue,
      };

      // Special handling for combo drinks - clear the other drink option
      if (selectedItem.category === Category.COMBO) {
        if (category === "Drink") {
          newSelections["Bottled Soda"] = "";
          // Set default size for fountain drinks if not already set
          if (!newSelections["Drink Size"]) {
            newSelections["Drink Size"] = "Regular";
          }
        } else if (category === "Bottled Soda") {
          newSelections["Drink"] = "";
          newSelections["Drink Size"] = ""; // Clear drink size for bottled drinks
        }

        // Clear chip type when switching sides for combos
        if (category === "Side") {
          newSelections["Chip Type"] = "";
          // Set default chip type when chips are selected
          if (value === "Chips") {
            newSelections["Chip Type"] = "Lays Plain";
          }
        }
      }

      return newSelections;
    });
  };

  const handleMultiSelection = (category: string, value: string) => {
    setSelections((prev) => {
      const currentSelections = (prev[category] as string[]) || [];
      const isSelected = currentSelections.includes(value);

      return {
        ...prev,
        [category]: isSelected
          ? currentSelections.filter((item) => item !== value)
          : [...currentSelections, value],
      };
    });
  };

  const validateSelections = () => {
    const newErrors: string[] = [];

    Object.entries(customizeData || {}).forEach(([key, value]) => {
      if (!isOptional(key)) {
        const selection = selections[key];
        if (
          !selection ||
          (Array.isArray(selection) && selection.length === 0)
        ) {
          newErrors.push(`Please select ${key}`);
        }
      }
    });

    // Special validation for combo drinks - must choose either drink or bottled drink
    if (selectedItem.category === Category.COMBO) {
      const drinkSelected = selections["Drink"];
      const bottleDrinkSelected = selections["Bottled Soda"];
      const drinkSizeSelected = selections["Drink Size"];

      if (!drinkSelected && !bottleDrinkSelected) {
        newErrors.push(
          "Please select either a Drink or Bottled Soda for your combo"
        );
      } else if (drinkSelected && bottleDrinkSelected) {
        newErrors.push(
          "Please select only one drink option (either Drink or Bottled Soda)"
        );
      } else if (drinkSelected && !drinkSizeSelected) {
        newErrors.push(
          "Please select a size for your fountain drink (Regular or Large)"
        );
      }
    }

    // Check if chip type is selected when chips are chosen as side (for all categories)
    if (selections["Side"] === "Chips" && !selections["Chip Type"]) {
      newErrors.push(
        "Please select a chip type when choosing chips as your side"
      );
    }

    // Special validation for egg sandwich - removed requirement for meat or egg
    // Egg sandwiches can now be ordered without meat or egg toppings
    // if (selectedItem.category === Category.EGGSANDWICH) {
    //   const meatSelected = selections["Meat"];
    //   const eggToppings = (selections["Toppings"] as string[]) || [];
    //   const hasEgg = eggToppings.some((topping) =>
    //     topping.toLowerCase().includes("egg")
    //   );
    //
    //   if (!meatSelected && !hasEgg) {
    //     newErrors.push(
    //       "Egg sandwich must include at least either meat or egg topping"
    //     );
    //   }
    // }

    setErrors(newErrors);
    return newErrors.length === 0;
  };

  const isFormValid = () => {
    if (!customizeData) return false;

    // Check if size is required and selected
    if (customizeData["Size"]) {
      const sizeOptions = customizeData["Size"];
      if (Array.isArray(sizeOptions) && sizeOptions.length > 0) {
        // If size options exist, user must select Regular or Large
        const selectedSize = selections["Size"];
        if (
          !selectedSize ||
          (selectedSize !== "Regular" && selectedSize !== "Large")
        ) {
          return false;
        }
      }
    }

    for (const [key, value] of Object.entries(customizeData)) {
      if (!isOptional(key)) {
        const selection = selections[key];
        if (
          !selection ||
          (Array.isArray(selection) && selection.length === 0)
        ) {
          return false;
        }
      }
    }

    // Special validation for combo drinks
    if (selectedItem.category === Category.COMBO) {
      const drinkSelected = selections["Drink"];
      const bottleDrinkSelected = selections["Bottled Soda"];
      const drinkSizeSelected = selections["Drink Size"];
      if (
        (!drinkSelected && !bottleDrinkSelected) ||
        (drinkSelected && bottleDrinkSelected) ||
        (drinkSelected && !drinkSizeSelected)
      ) {
        return false;
      }
    }

    // Check if chip type is selected when chips are chosen as side (for all categories)
    if (selections["Side"] === "Chips" && !selections["Chip Type"]) {
      return false;
    }

    // Special validation for egg sandwich - removed requirement for meat or egg
    // Egg sandwiches can now be ordered without meat or egg toppings
    // if (selectedItem.category === Category.EGGSANDWICH) {
    //   const meatSelected = selections["Meat"];
    //   const eggToppings = (selections["Toppings"] as string[]) || [];
    //   const hasEgg = eggToppings.some((topping) =>
    //     topping.toLowerCase().includes("egg")
    //   );
    //   if (!meatSelected && !hasEgg) {
    //     return false;
    //   }
    // }

    return true;
  };
  const getBasePrice = (size?: string) => {
    // Find the index of the selected item in the category
    const categoryItems = menuData[selectedItem.category];
    const foundItem = categoryItems.find(
      (item: any) => item.Name === selectedItem.name
    );
    if (foundItem && foundItem.Price) {
      if (typeof foundItem.Price === "object") {
        return parseFloat(foundItem.Price[size || "Regular"] || "0");
      } else {
        return parseFloat(foundItem.Price);
      }
    } else {
      return 0;
    }
  };

  const generateItemId = async (data: any): Promise<string> => {
    // Create a copy of data without quantity for ID generation
    const { quantity, ...dataWithoutQuantity } = data;
    const jsonString = JSON.stringify(
      dataWithoutQuantity,
      Object.keys(dataWithoutQuantity).sort()
    ); // Stable order
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(jsonString);
    const hashBuffer = await crypto.subtle.digest("SHA-256", dataBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
    return `item_${hashHex.slice(0, 12)}`; // Use only first 12 chars for brevity
  };
  const calculateTotalPrice = () => {
    const selectedSize = (selections["Size"] as string) || "Regular";
    let totalPrice = getBasePrice(selectedSize);

    // Handle bread upgrades (like Croissant +$0.75)
    if (
      selections["Bread"] &&
      selections["Bread"] === SandwichBread.CROISSANT
    ) {
      totalPrice += 0.75;
    }

    // Handle egg sandwich meat pricing - add $1.75 if meat is selected
    if (selectedItem.category === Category.EGGSANDWICH && selections["Meat"]) {
      totalPrice += 1.75;
    }

    // Handle combo drink size upgrade
    if (selectedItem.category === Category.COMBO) {
      if (selections["Drink Size"] === DrinkSize.LARGE) {
        totalPrice += 0.5; // Large drink upgrade cost
      }
      if (selections["Bottled Soda"]) {
        totalPrice += 0.5; // Bottled soda upgrade cost
      }
    }

    // Handle add-ons pricing
    if (selections["Add Ons"] && Array.isArray(selections["Add Ons"])) {
      const addOns = selections["Add Ons"] as string[];
      addOns.forEach((addOn) => {
        // Find the add-on in customizeData to get its price
        if (customizeData && customizeData["Add Ons"]) {
          const addOnItem = customizeData["Add Ons"].find(
            (item: any) => typeof item === "object" && item["Add Ons"] === addOn
          );
          if (addOnItem && addOnItem["Add Ons Price"]) {
            if (
              typeof addOnItem["Add Ons Price"] === "object" &&
              selectedSize
            ) {
              // Use size-based add-on pricing
              totalPrice +=
                parseFloat(addOnItem["Add Ons Price"][selectedSize]) || 0;
            } else {
              // Use flat add-on pricing
              totalPrice += parseFloat(addOnItem["Add Ons Price"]) || 0;
            }
          }
        }
      });
    }

    // Ensure totalPrice is a valid number
    const finalPrice =
      isNaN(totalPrice) || totalPrice === null || totalPrice === undefined
        ? 0
        : totalPrice;
    return finalPrice.toFixed(2);
  };

  const handleAddToCart = async () => {
    if (validateSelections()) {
      // Use the cartItemData state which is already updated by useEffect
      const data = cartItemData;

      const cartItem: CartItem = {
        id: await generateItemId(data),
        price: parseFloat(price.toFixed(2)),
        itemType: selectedItem.category,
        data: data,
      };
      addToCart(cartItem);

      // Clear form data after adding to cart
      setSelections({});
      setSpecialInstructions("");
      setQuantity(1);
      setErrors([]);

      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 transition-opacity">
      {/* Modal */}
      <div
        className="fixed inset-0 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <Card
          className="w-full max-w-lg max-h-[90vh] overflow-hidden rounded-t-3xl sm:rounded-xl shadow-2xl animate-in slide-in-from-bottom-full sm:slide-in-from-bottom-0 duration-300"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <CardHeader className="pb-4 bg-gradient-to-r from-primary/5 to-primary/10">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1 space-y-3">
                <div className="flex items-center gap-2">
                  <UtensilsIcon className="h-5 w-5 text-primary" />
                  <Badge variant="secondary" className="text-xs">
                    {selectedItem.category}
                  </Badge>
                </div>
                <CardTitle className="text-xl sm:text-2xl leading-tight">
                  {selectedItem.name}
                </CardTitle>
                {/* Quantity Selection */}
                <div className="flex items-center gap-3">
                  <span className="text-sm font-medium text-gray-700 flex items-center gap-1">
                    <span className="text-green-500">🔢</span>
                    Quantity:
                  </span>
                  <div className="flex items-center space-x-2">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      disabled={quantity <= 1}
                      className="h-8 w-8 rounded-full p-0 flex items-center justify-center"
                    >
                      -
                    </Button>
                    <div className="flex items-center justify-center min-w-[40px]">
                      <span className="text-lg font-semibold text-gray-800">
                        {quantity}
                      </span>
                    </div>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => setQuantity(quantity + 1)}
                      className="h-8 w-8 rounded-full p-0 flex items-center justify-center"
                    >
                      +
                    </Button>
                  </div>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="h-10 w-10 rounded-full hover:bg-destructive/10 hover:text-destructive transition-colors"
              >
                <XIcon className="h-5 w-5" />
              </Button>
            </div>
          </CardHeader>

          {/* Content */}
          <CardContent className="space-y-6 max-h-[60vh] overflow-y-auto">
            {customizeData ? (
              <div className="space-y-6">
                {Object.entries(customizeData).map(([key, value]) => (
                  <div key={key} className="space-y-3">
                    <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                      {key === "Size" && (
                        <span className="text-blue-500">📏</span>
                      )}
                      {key === "Toppings" && (
                        <span className="text-green-500">🥬</span>
                      )}
                      {key === "Bread" && (
                        <span className="text-yellow-600">🍞</span>
                      )}
                      {key === "Cheese" && (
                        <span className="text-yellow-400">🧀</span>
                      )}
                      {key === "Meat" && (
                        <span className="text-red-500">🥩</span>
                      )}
                      {key === "Dressing" && (
                        <span className="text-orange-500">🥗</span>
                      )}
                      {key === "Add Ons" && (
                        <span className="text-purple-500">➕</span>
                      )}
                      {key === "Bread Prep" && (
                        <span className="text-brown-500">🔥</span>
                      )}
                      {key === "Side" && (
                        <span className="text-green-600">🥙</span>
                      )}
                      {key === "Drink" && (
                        <span className="text-blue-600">🥤</span>
                      )}
                      {key === "Bottled Soda" && (
                        <span className="text-blue-700">🍾</span>
                      )}
                      {key === "Drink Size" && (
                        <span className="text-blue-500">📏</span>
                      )}
                      {key}
                    </h3>

                    {!isOptional(key) ? (
                      <Badge variant="destructive" className="text-xs mb-2">
                        Required
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="text-xs mb-2">
                        Optional - Click again to deselect
                      </Badge>
                    )}

                    {Array.isArray(value) ? (
                      <div className="grid grid-cols-2 gap-2">
                        {value
                          .filter((item) => {
                            // Filter out bacon for Garden Salad (veggies only)
                            if (
                              selectedItem.name ===
                                "Garden Salad (veggies only)" &&
                              key === "Toppings"
                            ) {
                              const itemValue =
                                typeof item === "string"
                                  ? item
                                  : item["Add Ons"] || JSON.stringify(item);
                              return itemValue.toLowerCase() !== "bacon";
                            }
                            return true;
                          })
                          .map((item, index) => {
                            const itemValue =
                              typeof item === "string"
                                ? item
                                : item["Add Ons"] || JSON.stringify(item);
                            const isSelected = isMultiSelect(key)
                              ? ((selections[key] as string[]) || []).includes(
                                  itemValue
                                )
                              : selections[key] === itemValue;

                            return (
                              <div key={index}>
                                <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                                  <input
                                    type={
                                      isMultiSelect(key) ? "checkbox" : "radio"
                                    }
                                    name={key}
                                    value={itemValue}
                                    checked={isSelected}
                                    onClick={(e) => {
                                      if (isMultiSelect(key)) {
                                        handleMultiSelection(key, itemValue);
                                      } else {
                                        // For radio buttons, prevent default behavior and handle manually
                                        e.preventDefault();
                                        handleSingleSelection(key, itemValue);
                                      }
                                    }}
                                    onChange={() => {}} // Empty onChange to avoid React warnings
                                    className="w-4 h-4 text-primary focus:ring-primary"
                                  />
                                  <div className="flex-1">
                                    {typeof item === "string" ? (
                                      <span className="text-sm font-medium">
                                        {item}
                                      </span>
                                    ) : typeof item === "object" &&
                                      item["Add Ons"] ? (
                                      <div className="space-y-1">
                                        <div className="text-sm font-medium">
                                          {item["Add Ons"]}
                                        </div>
                                        <div className="text-xs text-muted-foreground">
                                          {typeof item["Add Ons Price"] ===
                                          "object" ? (
                                            <div className="space-y-1">
                                              {Object.entries(
                                                item["Add Ons Price"]
                                              ).map(([size, price]) => (
                                                <div key={size}>
                                                  {String(size)}: $
                                                  {String(price)}
                                                </div>
                                              ))}
                                            </div>
                                          ) : (
                                            <div>${item["Add Ons Price"]}</div>
                                          )}
                                        </div>
                                      </div>
                                    ) : (
                                      <span className="text-sm">
                                        {JSON.stringify(item)}
                                      </span>
                                    )}
                                  </div>
                                </label>

                                {/* Size selection for fountain drinks in combos */}
                                {selectedItem.category === Category.COMBO &&
                                  key === "Drink" &&
                                  isSelected &&
                                  typeof item === "string" && (
                                    <div className="ml-7 mt-2 space-y-2">
                                      <div className="text-sm font-medium text-gray-700 mb-2">
                                        Select Size:
                                      </div>
                                      {["Regular", "Large"].map((size) => {
                                        const isSizeSelected =
                                          selections["Drink Size"] === size;
                                        return (
                                          <label
                                            key={size}
                                            className="flex items-center space-x-3 p-2 border rounded cursor-pointer hover:bg-gray-50 transition-colors"
                                          >
                                            <input
                                              type="radio"
                                              name="Drink Size"
                                              value={size}
                                              checked={isSizeSelected}
                                              onClick={(e) => {
                                                e.preventDefault();
                                                handleSingleSelection(
                                                  "Drink Size",
                                                  size
                                                );
                                              }}
                                              onChange={() => {}}
                                              className="w-4 h-4 text-primary focus:ring-primary"
                                            />
                                            <div className="flex-1">
                                              <span className="text-sm font-medium">
                                                {size}
                                              </span>
                                              {size === "Large" && (
                                                <span className="text-xs text-muted-foreground ml-2">
                                                  (+$0.50)
                                                </span>
                                              )}
                                            </div>
                                          </label>
                                        );
                                      })}
                                    </div>
                                  )}

                                {/* Chip type selection for chips in all categories */}
                                {key === "Side" &&
                                  isSelected &&
                                  typeof item === "string" &&
                                  item === "Chips" && (
                                    <div className="ml-7 mt-2 space-y-2">
                                      <div className="text-sm font-medium text-gray-700 mb-2">
                                        Select Chip Type:
                                      </div>
                                      {Object.values(Chips).map((chipType) => {
                                        const isChipSelected =
                                          selections["Chip Type"] === chipType;
                                        return (
                                          <label
                                            key={chipType}
                                            className="flex items-center space-x-3 p-2 border rounded cursor-pointer hover:bg-gray-50 transition-colors"
                                          >
                                            <input
                                              type="radio"
                                              name="Chip Type"
                                              value={chipType}
                                              checked={isChipSelected}
                                              onClick={(e) => {
                                                e.preventDefault();
                                                handleSingleSelection(
                                                  "Chip Type",
                                                  chipType
                                                );
                                              }}
                                              onChange={() => {}}
                                              className="w-4 h-4 text-primary focus:ring-primary"
                                            />
                                            <div className="flex-1">
                                              <span className="text-sm font-medium">
                                                {chipType}
                                              </span>
                                            </div>
                                          </label>
                                        );
                                      })}
                                    </div>
                                  )}
                              </div>
                            );
                          })}
                      </div>
                    ) : (
                      <div className="text-sm text-muted-foreground">
                        {JSON.stringify(value)}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                <p className="text-muted-foreground">
                  Loading customization options...
                </p>
              </div>
            )}

            {/* Special Instructions */}
            <div className="space-y-3">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <span className="text-blue-500">📝</span>
                Special Instructions
              </h3>
              <Badge variant="secondary" className="text-xs mb-2">
                Optional
              </Badge>
              <textarea
                value={specialInstructions}
                onChange={(e) => setSpecialInstructions(e.target.value)}
                placeholder="Add any special requests or instructions for your order..."
                className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary focus:border-transparent"
                rows={3}
                maxLength={200}
              />
              <div className="text-xs text-muted-foreground text-right">
                {specialInstructions.length}/200 characters
              </div>
            </div>

            {errors.length > 0 && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <h4 className="text-red-800 font-medium mb-2">
                  Please fix the following:
                </h4>
                <ul className="text-red-700 text-sm space-y-1">
                  {errors.map((error, index) => (
                    <li key={index}>• {error}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>

          {/* Footer */}
          <CardFooter className="p-6 bg-gradient-to-r from-primary/5 to-primary/10 border-t space-x-4">
            <Button
              onClick={handleAddToCart}
              disabled={!isFormValid()}
              className="flex-1 h-14 text-lg font-bold rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed"
              size="lg"
            >
              Add to Cart - ${price * quantity}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default FoodCustomize;
