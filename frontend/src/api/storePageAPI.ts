// API functions for the store page
import { Category } from "../utils/Schema";
// Define types locally since menuTypes.ts doesn't exist
export type MenuItemResponse = {
  Hotdog: object;
  Sandwich: object;
  EggSandwich: object;
  Side: object;
  Drink: object;
  Salad: object;
  Combo: object;
};

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000/api";

export const getAllCategories = async (): Promise<Category[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/get_category`);
    if (!response.ok) {
      throw new Error("Failed to fetch categories");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching categories:", error);
    return [];
  }
};

/**
 * Fetch all menu items from various endpoints
 */
export const getMenuItems = async (): Promise<MenuItemResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/get_menu`);
    if (!response.ok) {
      throw new Error("Failed to fetch menu items");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching menu items:", error);
    return {
      Hotdog: {},
      Sandwich: {},
      EggSandwich: {},
      Side: {},
      Drink: {},
      Salad: {},
      Combo: {},
    };
  }
};
