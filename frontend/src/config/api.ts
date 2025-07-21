// API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  BASE: API_BASE_URL,
  AUTH: {
    LOGIN: `${API_BASE_URL}/api/v1/auth/login`,
    ME: `${API_BASE_URL}/api/v1/auth/me`,
  },
  QUERY: {
    ASK: `${API_BASE_URL}/api/v1/query/ask`,
  },
  ANALYTICS: {
    PORTFOLIO_SUMMARY: `${API_BASE_URL}/api/v1/analytics/portfolio-summary`,
    TOP_PERFORMERS: `${API_BASE_URL}/api/v1/analytics/top-performers`,
  },
  DATA: {
    CLIENTS: `${API_BASE_URL}/api/v1/data/clients`,
    TRANSACTIONS: `${API_BASE_URL}/api/v1/data/transactions`,
    PORTFOLIO_HOLDINGS: `${API_BASE_URL}/api/v1/data/portfolio-holdings`,
    RELATIONSHIP_MANAGERS: `${API_BASE_URL}/api/v1/data/relationship-managers`,
    INITIALIZE_SAMPLE_DATA: `${API_BASE_URL}/api/v1/data/initialize-sample-data`,
  },
};

export default API_BASE_URL;
