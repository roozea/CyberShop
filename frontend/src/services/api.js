import axios from "axios";
import { API_URL } from "../config";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (credentials) => {
  const response = await api.post("/auth/login", credentials);
  if (response.data.access_token) {
    localStorage.setItem("token", response.data.access_token);
  }
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post("/auth/register", userData);
  return response.data;
};

export const getProducts = async () => {
  const response = await api.get("/products/");
  return response.data;
};

export const searchProducts = async (query) => {
  const response = await api.get(`/products/search?query=${query}`);
  return response.data;
};

export const addToCart = async (productData) => {
  const response = await api.post("/cart/add", productData);
  return response.data;
};

export const getCart = async () => {
  const response = await api.get("/cart");
  return response.data;
};

export const addComment = async (productId, commentData) => {
  const response = await api.post(`/products/${productId}/comments`, commentData);
  return response.data;
};

export default api;
