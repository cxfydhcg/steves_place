// API functions for the home page

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export interface FeaturedItem {
  id: string;
  name: string;
  price: number;
  category: string;
  description: string;
  featured: boolean;
}

export interface HomeStats {
  totalItems: number;
  categories: string[];
  specialOffers: number;
}

/**
 * Fetch all available categories
 */
export const getCategories = async (): Promise<string[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/get_all_category`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data['All Category'] || [];
  } catch (error) {
    console.error('Error fetching categories:', error);
    return ['Hotdog', 'Sandwich', 'Egg Sandwich', 'Drink', 'Side', 'Combo'];
  }
};