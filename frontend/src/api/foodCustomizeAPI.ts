const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000/api";

/**
 * Fetch customize section data
 */
export const getCustomizeData = async (category: string) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/get_${category.toLowerCase()}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data);
    return data || {};
  } catch (error) {
    console.error(`Error fetching ${category}:`, error);
    return {};
  }
};
