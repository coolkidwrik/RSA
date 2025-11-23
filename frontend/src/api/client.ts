import axios, { AxiosInstance, AxiosError } from 'axios';
import config from '@/config/settings';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: config.api.baseURL,
  timeout: config.api.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error: AxiosError) => {
    if (error.response) {
      console.error('API Error Response:', error.response.data);
      const errorData = error.response.data as any;
      throw new Error(errorData.detail || 'API request failed');
    } else if (error.request) {
      console.error('Network Error:', error.request);
      throw new Error('Network error - please check if backend is running');
    } else {
      console.error('Request Error:', error.message);
      throw new Error(error.message);
    }
  }
);

export default apiClient;