/**
 * API service for communicating with the backend
 */

const API_BASE_URL = "http://localhost:8000";

class ApiService {
  /**
   * Generate a survey using AI
   * @param {Object} surveyData - Survey title and description
   * @param {string} surveyData.title - Survey title
   * @param {string} surveyData.description - Survey description
   * @returns {Promise<Object>} Generated survey data
   */
  static async generateSurvey(surveyData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/surveys/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(surveyData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error generating survey:", error);
      throw error;
    }
  }

  /**
   * Health check endpoint
   * @returns {Promise<Object>} Health status
   */
  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Health check failed:", error);
      throw error;
    }
  }
}

export default ApiService;
