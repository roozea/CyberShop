import axios from "axios";
import { API_URL } from "../config";

console.log('Initializing API with URL:', API_URL); // Debug log

const api = axios.create({
  baseURL: API_URL,
  withCredentials: false, // Cambiado a false para evitar problemas de CORS
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use((config) => {
  console.log('Making API request:', config.method?.toUpperCase(), config.url);
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  console.error('Request interceptor error:', error);
  return Promise.reject(error);
});

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    return Promise.reject(error);
  }
);

export const login = async (credentials) => {
  try {
    const response = await api.post("/auth/login", credentials);
    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);
    }
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post("/auth/register", userData);
    return response.data;
  } catch (error) {
    console.error('Register error:', error);
    throw error;
  }
};

export const getProducts = async () => {
  try {
    console.log('Fetching products from API...');
    const response = await api.get("/products/");
    console.log('Products fetched successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    });
    throw error;
  }
};

export const searchProducts = async (query) => {
  try {
    const response = await api.get(`/products/search?query=${query}`);
    return response.data;
  } catch (error) {
    console.error('Search products error:', error);
    throw error;
  }
};

export const addToCart = async (productData) => {
  try {
    const response = await api.post("/cart/add", productData);
    return response.data;
  } catch (error) {
    console.error('Add to cart error:', error);
    throw error;
  }
};

export const getCart = async () => {
  try {
    const response = await api.get("/cart");
    return response.data;
  } catch (error) {
    console.error('Get cart error:', error);
    throw error;
  }
};

export const addComment = async (productId, commentData) => {
  try {
    const response = await api.post(`/products/${productId}/comments`, commentData);
    return response.data;
  } catch (error) {
    console.error('Add comment error:', error);
    throw error;
  }
};

export default api;
