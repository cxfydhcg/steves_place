import React, {
  useState,
  useEffect,
  useMemo,
  useCallback,
  useRef,
} from "react";
import { useNavigate } from "react-router-dom";
import {
  getMenuItems,
  getAllCategories,
  MenuItemResponse,
} from "../api/storePageAPI";
import { Button } from "../components/ui/button";
import { createContext, useContext, ReactNode } from "react";
import {
  Category,
  HotdogSchema,
  SandwichSchema,
  EggSandwichSchema,
  SaladSchema,
  SideSchema,
  DrinkSchema,
  ComboSchema,
  displayAllValues,
  selectedItem,
} from "../utils/Schema";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import FoodCustomize from "./foodcustomize";
import {
  FaSearch,
  FaUtensils,
  FaExclamationTriangle,
  FaHotdog,
  FaCheese,
  FaFire,
  FaLeaf,
  FaArrowLeft,
} from "react-icons/fa";
import { RiDrinks2Line } from "react-icons/ri";
import { LuSandwich } from "react-icons/lu";
import { useCart } from "../context/CartContext";
import { PlusIcon } from "lucide-react";
import { CiFries } from "react-icons/ci";
import Cart from "./Cart";

// Type the icons properly
const SearchIcon = FaSearch as React.ComponentType<{ className?: string }>;
const UtensilsIcon = FaUtensils as React.ComponentType<{ className?: string }>;
const ExclamationTriangleIcon = FaExclamationTriangle as React.ComponentType<{
  className?: string;
}>;

const HotdogIcon = FaHotdog as React.ComponentType<{ className?: string }>;
const DrinksIcon = RiDrinks2Line as React.ComponentType<{ className?: string }>;
const SandwichIcon = LuSandwich as React.ComponentType<{ className?: string }>;
const FriesIcon = CiFries as React.ComponentType<{ className?: string }>;

const CheeseIcon = FaCheese as React.ComponentType<{ className?: string }>;
const FireIcon = FaFire as React.ComponentType<{ className?: string }>;
const LeafIcon = FaLeaf as React.ComponentType<{ className?: string }>;
const ArrowLeftIcon = FaArrowLeft as React.ComponentType<{
  className?: string;
}>;

// Function to get appropriate icon for each category
const getCategoryIcon = (category: string) => {
  switch (category) {
    case Category.SANDWICH:
      return <SandwichIcon className="h-6 w-6 text-orange-500" />;
    case Category.EGGSANDWICH:
      return <SandwichIcon className="h-6 w-6 text-yellow-400" />;
    case Category.HOTDOG:
      return <HotdogIcon className="h-6 w-6 text-red-500" />;
    case Category.DRINK:
      return (
        <div className="flex items-center space-x-1">
          <DrinksIcon className="h-5 w-5 text-blue-500" />
        </div>
      );
    case Category.SIDE:
      return <CheeseIcon className="h-6 w-6 text-yellow-500" />;
    case Category.SALAD:
      return <LeafIcon className="h-6 w-6 text-green-500" />;
    case Category.COMBO:
      return (
        <div className="flex items-center space-x-1">
          <FriesIcon className="h-5 w-5 text-yellow-500" />
          <DrinksIcon className="h-5 w-5 text-blue-500" />
        </div>
      );
    default:
      return <UtensilsIcon className="h-6 w-6 text-blue-500" />;
  }
};

const StorePage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const { getCart } = useCart();
  const [selectedItem, setSelectedItem] = useState<selectedItem>();
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<string[]>(["All"]);
  const [menuData, setMenuData] = useState<MenuItemResponse>({
    Hotdog: [],
    Sandwich: [],
    EggSandwich: [],
    Side: [],
    Drink: [],
    Salad: [],
    Combo: [],
  });
  // Initialize categoryRefs properly
  const categoryRefs = useRef<Record<string, HTMLDivElement | null>>({});

  // Callback ref function to store category refs
  const setCategoryRef = useCallback((category: string) => {
    return (el: HTMLDivElement | null) => {
      categoryRefs.current[category] = el;
    };
  }, []);

  const scrollToCategory = (category: string) => {
    if (category === "All") {
      // Scroll to top for "All" category
      window.scrollTo({ top: 0, behavior: "smooth" });
      setSelectedCategory(category);
      return;
    }

    setSelectedCategory(category);
    const element = categoryRefs.current[category];
    if (element) {
      // Get the sticky header height dynamically
      const stickyHeader = document.querySelector(".sticky");
      const stickyHeaderHeight = stickyHeader
        ? stickyHeader.getBoundingClientRect().height
        : 0;

      // Add some padding to ensure the category header is clearly visible
      const additionalPadding = 20;
      const totalOffset = stickyHeaderHeight + additionalPadding;

      const elementPosition =
        element.getBoundingClientRect().top + window.pageYOffset;
      const targetPosition = elementPosition - totalOffset;

      // Ensure we don't scroll to negative position or past document height
      const maxScrollTop =
        document.documentElement.scrollHeight - window.innerHeight;
      const finalScrollPosition = Math.max(
        0,
        Math.min(targetPosition, maxScrollTop)
      );

      window.scrollTo({
        top: finalScrollPosition,
        behavior: "smooth",
      });
    }
  };
  const fetchCategories = async () => {
    try {
      const categoryList = await getAllCategories();
      setCategories(["All", ...categoryList]);
    } catch (error) {
      console.error("Failed to fetch categories:", error);
    }
  };

  const fetchAllMenuItems = async () => {
    try {
      setError(null);
      const data = await getMenuItems();
      console.log(data);
      setMenuData(data);
    } catch (error) {
      console.error("Failed to fetch menu items:", error);
      setError("Failed to load menu items. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  // Fetch data on component mount
  useEffect(() => {
    fetchCategories();
    fetchAllMenuItems();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 flex items-center justify-center">
        <div className="text-center space-y-6 p-8">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary/20 border-t-primary mx-auto"></div>
            <UtensilsIcon className="h-8 w-8 text-primary absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-foreground">
              Loading Menu
            </h2>
            <p className="text-muted-foreground">
              Preparing our delicious offerings...
            </p>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/10 mobile-scroll-fix">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        {/* Back Button */}
        <div className="mb-6">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/")}
            className="flex items-center gap-2 hover:bg-primary/10 transition-colors"
          >
            <ArrowLeftIcon className="h-4 w-4" />
            Back to Home
          </Button>
        </div>
        {/* Header */}
        <div className="text-center mb-12 space-y-6">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-orange-500/20 to-red-500/20 blur-3xl opacity-30 rounded-full"></div>
            <div className="relative">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-foreground mb-6 bg-gradient-to-r from-primary via-orange-500 to-red-500 bg-clip-text text-transparent flex items-center justify-center gap-4">
                Steve's Place Menu
                <FireIcon className="h-10 w-10 sm:h-12 sm:w-12 lg:h-16 lg:w-16 text-orange-500 animate-bounce" />
              </h1>
            </div>
          </div>
          <div className="max-w-3xl mx-auto space-y-4">
            <p className="text-xl sm:text-2xl text-muted-foreground leading-relaxed font-medium">
              Discover our handcrafted selection of fresh food
            </p>
            <p className="text-base sm:text-lg text-muted-foreground/80">
              Tap any item to customize your perfect order
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="max-w-md mx-auto p-4 bg-destructive/10 border border-destructive/20 rounded-xl">
              <div className="flex items-center gap-2 text-destructive">
                <ExclamationTriangleIcon className="h-4 w-4" />
                <span className="text-sm font-medium">{error}</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => fetchAllMenuItems()}
                className="mt-2 h-8 text-xs"
              >
                Try Again
              </Button>
            </div>
          )}
        </div>
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative max-w-lg mx-auto">
            <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-orange-500/10 rounded-2xl blur opacity-50"></div>
            <div className="relative">
              <SearchIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search delicious menu items..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-6 py-4 border-2 border-border/50 rounded-2xl focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all duration-300 text-base bg-background/80 backdrop-blur-sm shadow-lg hover:shadow-xl"
              />
            </div>
          </div>
        </div>
        {/* Category Filter - Sticky */}
        <div className="sticky top-0 z-50 mb-10 py-6">
          <div className="relative">
            <div className="relative bg-white/90 backdrop-blur-sm border-b border-gray-200/30 px-4 py-4 sm:px-6 sm:py-6 overscroll-none">
              <div className="flex flex-wrap gap-3 justify-center px-2">
                {categories.map((category) => (
                  <Button
                    key={category}
                    variant={
                      selectedCategory === category ? "default" : "outline"
                    }
                    size="sm"
                    onClick={() => scrollToCategory(category)}
                    className={`text-sm sm:text-base px-4 py-2 sm:px-6 sm:py-3 rounded transition-colors duration-200 font-medium ${
                      selectedCategory === category
                        ? "bg-primary/10 text-primary"
                        : "hover:bg-gray-100"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {category !== "All" && getCategoryIcon(category)}
                      <span>{category}</span>
                      {category !== "All" && (
                        <Badge
                          variant={
                            selectedCategory === category
                              ? "secondary"
                              : "outline"
                          }
                          className="text-xs ml-1 px-2 py-0.5"
                        >
                          {(
                            menuData[
                              category as keyof MenuItemResponse
                            ] as any[]
                          )?.length || 0}
                        </Badge>
                      )}
                    </div>
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </div>
        {/* Menu Items Sections based on category */}
        {categories
          .filter((category) => category !== "All")
          .map((category) => {
            const categoryItems = menuData[
              category as keyof MenuItemResponse
            ] as any[];

            // Filter items based on search only (removed category filtering)
            const filteredItems =
              categoryItems?.filter((item) => {
                const matchesSearch =
                  searchQuery === "" ||
                  item.Name.toLowerCase().includes(searchQuery.toLowerCase());
                // Removed the matchesCategory condition
                return matchesSearch;
              }) || [];

            // Don't render empty categories when searching
            if (filteredItems.length === 0 && searchQuery !== "") {
              return null;
            }

            return (
              <div
                key={category}
                ref={setCategoryRef(category)}
                className="mb-12"
              >
                <div className="flex items-center gap-3 mb-6">
                  {getCategoryIcon(category)}
                  <h2 className="text-2xl font-bold text-foreground">
                    {category}
                  </h2>
                  <Badge variant="secondary" className="text-sm">
                    {filteredItems.length} items
                  </Badge>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 sm:gap-8">
                  {filteredItems.map((item, index) => {
                    const hasMultiplePrices = typeof item.Price === "object";

                    return (
                      <Card
                        key={`${category}-${index}`}
                        className="group hover:shadow-2xl hover:shadow-primary/10 transition-all duration-500 cursor-pointer border-2 border-border/50 hover:border-primary/60 rounded-2xl overflow-hidden bg-gradient-to-br from-background to-background/80 backdrop-blur-sm hover:scale-[1.02] transform-gpu"
                        onClick={() => {
                          setSelectedItem({
                            name: item.Name,
                            category: category as Category,
                          });
                          setIsModalOpen(true);
                        }}
                      >
                        <CardHeader className="pb-4 pt-6 px-6">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <CardTitle className="text-xl font-bold text-foreground group-hover:text-primary transition-colors duration-300 leading-tight">
                                {item.Name}
                              </CardTitle>
                              <CardDescription className="text-sm text-muted-foreground/80 mt-2 font-medium">
                                {category}
                              </CardDescription>
                            </div>
                            <div className="ml-3 p-2 rounded-full bg-primary/10 group-hover:bg-primary/20 transition-colors duration-300">
                              {getCategoryIcon(category)}
                            </div>
                          </div>
                        </CardHeader>

                        <CardContent className="pt-0 px-6 pb-4">
                          <div className="space-y-3">
                            {hasMultiplePrices ? (
                              <div className="space-y-1 sm:space-y-2 bg-muted/30 rounded-lg sm:rounded-xl p-2 sm:p-4">
                                {Object.entries(item.Price).map(
                                  ([size, price]) => (
                                    <div
                                      key={size}
                                      className="flex justify-between items-center text-sm"
                                    >
                                      <span className="text-muted-foreground capitalize font-normal text-xs">
                                        {size}:
                                      </span>
                                      <span className="font-bold text-primary text-sm sm:text-lg">
                                        ${String(price)}
                                      </span>
                                    </div>
                                  )
                                )}
                              </div>
                            ) : (
                              <div className="space-y-1 bg-muted/30 rounded-lg p-2">
                                <div className="flex justify-between items-center text-sm">
                                  <span className="text-muted-foreground capitalize font-medium">
                                    Price:
                                  </span>
                                  <span className="font-medium text-primary text-xs">
                                    ${String(item.Price)}
                                  </span>
                                </div>
                              </div>
                            )}
                          </div>
                        </CardContent>

                        <CardFooter className="pt-4 px-6 pb-6">
                          <Button
                            className="w-full h-12 font-semibold rounded transition-colors duration-200"
                            variant="secondary"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedItem({
                                name: item.Name,
                                category: category as Category,
                              });
                              setIsModalOpen(true);
                            }}
                          >
                            <PlusIcon className="h-5 w-5 mr-2" />
                            <span className="text-base">Customize & Add</span>
                          </Button>
                        </CardFooter>
                      </Card>
                    );
                  })}
                </div>

                {/* Show message if category is empty */}
                {filteredItems.length === 0 &&
                  searchQuery === "" &&
                  selectedCategory === "All" && (
                    <div className="text-center py-8">
                      <p className="text-muted-foreground">
                        No items available in this category.
                      </p>
                    </div>
                  )}
              </div>
            );
          })}
        {/* Empty State */}
        {Object.values(menuData)
          .flat()
          .filter(
            (item) =>
              (selectedCategory === "All" ||
                (item as any).category === selectedCategory) &&
              (searchQuery === "" ||
                (item as any).name
                  .toLowerCase()
                  .includes(searchQuery.toLowerCase()))
          ).length === 0 && (
          <div className="text-center py-16">
            <div className="space-y-2 sm:space-y-4">
              <SearchIcon className="h-16 w-16 text-muted-foreground/50 mx-auto" />
              <div className="space-y-2">
                <h3 className="text-xl font-semibold text-foreground">
                  No items found
                </h3>
                <p className="text-muted-foreground max-w-md mx-auto">
                  {searchQuery
                    ? `No items match "${searchQuery}" in ${selectedCategory === "All" ? "any category" : selectedCategory}.`
                    : `No items available in ${selectedCategory}.`}
                </p>
              </div>
              {(searchQuery || selectedCategory !== "All") && (
                <Button
                  variant="outline"
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedCategory("All");
                  }}
                  className="mt-4"
                >
                  Clear filters
                </Button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Cart Component */}
      <Cart isCartOpen={isCartOpen} setIsCartOpen={setIsCartOpen} />

      {/* Item Detail Modal */}
      {selectedItem && (
        <FoodCustomize
          selectedItem={selectedItem}
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          menuData={menuData}
        />
      )}
    </div>
  );
};

export default StorePage;
