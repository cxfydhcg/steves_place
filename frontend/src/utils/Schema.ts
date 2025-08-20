// TypeScript interfaces corresponding to Pydantic schemas in backend/models/Schema.py

// Enum types from backend models
export enum Category {
  HOTDOG = "Hotdog",
  SANDWICH = "Sandwich",
  EGGSANDWICH = "EggSandwich",
  SALAD = "Salad",
  SIDE = "Side",
  DRINK = "Drink",
  COMBO = "Combo",
}

export enum SideName {
  CHIPS = "Chips",
  SLAW = "Slaw",
  POTATO_SALAD = "Potato Salad",
  MACARONI_SALAD = "Macaroni Salad",
  DEVILED_EGG = "Deviled Egg",
  FRENCH_FRIES = "French Fries",
  TUNA_SALAD = "Tuna Salad",
  CHICKEN_SALAD = "Chicken Salad",
  CHEESE_FRIES = "Cheese Fries",
  CHILLI_CHEESE_FRIES = "Chilli Cheese Fries",
}

export enum SideSize {
  REGULAR = "Regular",
  LARGE = "Large",
}

export enum Chips {
  LAYS_PLAIN = "Lays Plain",
  LAYS_BBQ = "Lays BBQ",
  JALAPENO_KETTLE_CHIPS = "Jalapeno Kettle Chips",
  SOUR_CREAM_ONION_KETTLE_CHIPS = "Sour Cream N' Onion Kettle Chips",
  SALT_VINEGAR_KETTLE_CHIPS = "Salt N' Vinegar Kettle Chips",
  COOKIES = "Cookies",
}

export enum DrinkSize {
  REGULAR = "Regular",
  LARGE = "Large",
  BOTTLE = "Bottle",
}

export enum FountainDrink {
  COKE = "Coke",
  DIET_COKE = "Diet Coke",
  SPRITE = "Sprite",
  MOUNTAIN_DEW_YELLOW = "Mountain Dew Yellow",
  HI_C = "Hi-C",
  ROOT_BEER = "Root Beer",
  DR_PEPPER = "Dr Pepper",
  SWEET_TEA = "Homemade Sweet Tea",
  UNSWEET_TEA = "Homemade Unsweet Tea",
  LEMONADE = "Homemade Lemonade",
}

export enum BottleDrink {
  BOTTLED_SODA = "Bottled Soda",
}

export enum HotDogMeat {
  RED = "Red (Pork & Beef)",
  RED_FOOTLONG = "Red Footlong (Pork & Beef)",
  ITALIAN_SAUSAGE = "Italian Sausage",
  BEEF = "Beef (100%)",
  BEEF_FOOTLONG = "Beef Footlong 1/3lb",
  RED_HOT_SAUSAGE = "Red Hot Sausage",
  TURKEY = "Turkey",
  SMOKED_BEEF = "Smoked Beef",
  JALAPENO = "Jalapeno",
  KIELBASA = "Kielbasa",
  SAUSAGE = "Sausage (Pork & Beef)",
}

export enum HotDogTopping {
  MUSTARD = "Mustard",
  KETCHUP = "Ketchup",
  CHILI = "Chili",
  ONIONS = "Onions",
  SLAW = "Slaw",
  PICKLES = "Pickles",
  KRAUT = "Kraut",
  CHEESE = "Cheese",
  RELISH = "Relish",
  GRILLED_ONIONS = "Grilled Onions",
  GRILLED_PEPPERS = "Grilled Peppers",
  SPICY_MUSTARD = "Spicy Mustard",
  RED_ONION_SAUCE = "Red Onion Sauce",
  JALAPENOS = "Jalapenos",
  MAYO = "Mayo",
  HOT_CHERRY_PEPPERS = "Hot Cherry Peppers",
}

export enum SaladChoice {
  CHEF_HAM_TURKEY = "Chef Salad - Ham & Turkey",
  CHEF_CHICKEN = "Chef Salad - Chicken Salad",
  CHEF_TUNA = "Chef Salad - Tuna Salad",
  GARDEN = "Garden Salad (veggies only)",
}

export enum SaladTopping {
  LETTUCE = "Lettuce",
  BACON = "Bacon",
  TOMATO = "Tomato",
  CUCUMBER = "Cucumber",
  ONIONS = "Onions",
  OLIVES = "Olives",
  EGGS = "Eggs",
  GREEN_PEPPERS = "Green Peppers",
  BANANA_PEPPERS = "Banana Peppers",
  JALAPENOS = "Jalapenos Peppers",
  SALT_PEPPER = "Salt & Pepper",
  OREGANO = "Oregano",
  OIL_VINEGAR = "Oil & Vinegar",
  PICKLES = "Pickles",
  AMERICAN_CHEESE = "American Cheese",
  PROVOLONE_CHEESE = "Provolone Cheese",
  SWISS_CHEESE = "Swiss Cheese",
}

export enum SaladDressing {
  RANCH = "Ranch",
  ITALIAN = "Italian",
  FRENCH = "French",
  THOUSAND_ISLAND = "Thousand Island",
  HONEY_MUSTARD = "Honey Mustard",
}

export enum SaladAddOns {
  CHEESE = "Cheese",
  EGGS = "Eggs",
  MEAT = "Meat",
  DRESSING = "Dressing",
}

export enum SandwichSize {
  REGULAR = "Regular",
  LARGE = "Large",
}

export enum SandwichBread {
  WHITE = "White",
  WHEAT = "Wheat",
  RYE = "Rye",
  KAISER_ROLL = "Kaiser Roll",
  CROISSANT = "Croissant +$0.75",
}

export enum SandwichMeat {
  CHICKEN_SALAD = "Chicken Salad",
  TUNA_SALAD = "Tuna Salad",
  FRIED_BOLOGNA = "Fried Bologna",
  EGG_SALAD = "Egg Salad",
  PIMENTO_CHEESE = "Pimento Cheese",
  GRILLED_CHEESE = "Grilled Cheese",
  BLT = "BLT",
  TURKEY = "Turkey",
  ROAST_BEEF = "Roast Beef",
  CORNED_BEEF_REUBEN = "Corned Beef Reuben",
  HAM = "Ham",
  BUFFALO_CHICKEN_BREAST = "Buffalo Chicken Breast",
  HOT_PASTRAMI = "Hot Pastrami",
  HOT_CORNED_BEEF = "Hot Corned Beef",
  HALF_TURKEY_HALF_HAM = "Half Turkey Half Ham",
  HALF_HOT_PASTRAMI_HALF_CORNED_BEEF = "Half Hot Pastrami Half Corned Beef",
}

export enum SandwichCheese {
  AMERICAN = "American",
  PROVOLONE = "Provolone",
  SWISS = "Swiss",
  PEPPER_JACK = "Pepper Jack",
}

export enum SandwichToppings {
  MAYO = "Mayo",
  TOMATO = "Tomato",
  LETTUCE = "Lettuce",
  ONIONS = "Onions",
  PICKLES = "Pickles",
  SALT = "Salt",
  PEPPER = "Pepper",
  OREGANO = "Oregano",
  THOUSAND_ISLAND = "Thousand Island",
  GRILLED_ONIONS = "Grilled Onions",
  GRILLED_PEPPERS = "Grilled Peppers",
  SPICY_MUSTARD = "Spicy Mustard",
  MUSTARD = "Mustard",
  BANANA_PEPPERS = "Banana Peppers",
  JALAPENO_PEPPERS = "Jalapeno Peppers",
  OLIVES = "Olives",
  OIL = "Oil",
  VINEGAR = "Vinegar",
  KRAUT = "Kraut",
}

export enum SandwichAddOns {
  BACON = "Bacon",
  MEAT = "Meat",
  CHEESE = "Cheese",
}

// Egg Sandwich specific enums
export enum Egg {
  FRIED = "Fried Egg",
  SCRAMBLED = "Scrambled Egg",
  NO_EGG = "No Egg",
}

export enum EggSandwichBread {
  WHITE = "White",
  WHEAT = "Wheat",
  RYE = "Rye",
  KAISER_ROLL = "Kaiser Roll",
  CROISSANT = "Croissant +$0.75",
}

export enum EggSandwichMeat {
  PORK_ROLL = "Pork Roll",
  HAM = "Ham",
  BACON = "Bacon",
  SAUSAGE = "Sausage",
  TURKEY_SAUSAGE = "Turkey Sausage",
  COUNTRY_HAM = "Country Ham",
  TURKEY_BACON = "Turkey Bacon",
}

export enum EggSandwichCheese {
  AMERICAN = "American",
  SWISS = "Swiss",
  PROVOLONE = "Provolone",
  PEPPER_JACK = "Pepper Jack",
}

export enum EggSandwichToppings {
  MAYO = "Mayo",
  SALT = "Salt",
  PEPPER = "Pepper",
  KETCHUP = "Ketchup",
}

export enum EggSandwichAddOns {
  HASHBROWN = "Hashbrown on it (1 Piece)",
  HASHBROWN_ONSIDE = "Hashbrown on Side (2 Piece)",
  MEAT = "Meat",
  EGG = "Egg",
  CHEESE = "Cheese",
}

// Schema interfaces corresponding to Pydantic models
export interface SideSchema {
  quantity: number; // ge=1
  name: SideName;
  size?: SideSize;
  chips_type?: Chips;
  special_instructions?: string; // max_length=100
}

export interface DrinkSchema {
  quantity: number; // ge=1
  size: DrinkSize;
  name: FountainDrink | BottleDrink;
  special_instructions?: string; // max_length=100
}

export interface HotdogSchema {
  quantity: number; // ge=1
  dog_type: HotDogMeat;
  toppings?: HotDogTopping[];
  special_instructions?: string; // max_length=100
}

export interface SaladSchema {
  quantity: number; // ge=1
  choice: SaladChoice;
  toppings: SaladTopping[];
  dressing?: SaladDressing;
  special_instructions?: string; // max_length=100
  add_ons?: SaladAddOns[];
}

export interface SandwichSchema {
  quantity: number; // ge=1
  size: SandwichSize;
  bread: SandwichBread;
  meat: SandwichMeat;
  toasted?: boolean;
  grilled?: boolean;
  cheese?: SandwichCheese;
  toppings?: SandwichToppings[];
  special_instructions?: string; // max_length=100
  add_ons?: SandwichAddOns[];
}

export interface ComboSideSchema {
  name: SideName;
  size?: SideSize;
  chips_type?: Chips;
}

export interface ComboDrinkSchema {
  name: FountainDrink | BottleDrink;
  size?: DrinkSize;
}

export interface ComboSchema {
  quantity: number; // ge=1
  side: ComboSideSchema;
  drink: ComboDrinkSchema;
  special_instructions?: string; // max_length=100
}

export interface EggSandwichSchema {
  quantity: number; // ge=1
  bread: EggSandwichBread;
  egg: Egg;
  toasted?: boolean;
  grilled?: boolean;
  meat?: EggSandwichMeat;
  cheese?: EggSandwichCheese;
  toppings?: EggSandwichToppings[];
  special_instructions?: string; // max_length=100
  add_ons?: EggSandwichAddOns[];
}

export interface selectedItem {
  name: string;
  category: Category;
}

export interface CartItem {
  id: string;
  price: number;
  itemType: Category;
  data:
    | HotdogSchema
    | SandwichSchema
    | EggSandwichSchema
    | SaladSchema
    | SideSchema
    | DrinkSchema
    | ComboSchema;
}

// Union type for drink names
export type DrinkName = FountainDrink | BottleDrink;

// Type guards for drink types
export function isFountainDrink(drink: DrinkName): drink is FountainDrink {
  return Object.values(FountainDrink).includes(drink as FountainDrink);
}

export function isBottleDrink(drink: DrinkName): drink is BottleDrink {
  return Object.values(BottleDrink).includes(drink as BottleDrink);
}

// JSON Display Function for debugging or detailed inspection
export function displayAllValues(item: CartItem): string {
  return JSON.stringify(
    {
      id: item.id,
      price: item.price,
      itemType: item.itemType,
      data: item.data,
    },
    null,
    2
  );
}
