import axios from 'axios';

// Vulnerable: No validación de certificados SSL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  validateStatus: () => true, // Vulnerable: Acepta cualquier código de estado
});

// Vulnerable: No sanitización de datos
export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });

    // Vulnerable: Almacenamiento inseguro de datos sensibles
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('userData', JSON.stringify(response.data.user_data));
    }

    return response.data;
  } catch (error) {
    console.error('Error en login:', error);
    return null;
  }
};

// Vulnerable: No validación de datos de entrada
export const register = async (userData) => {
  try {
    const response = await api.post('/auth/register', userData);
    return response.data;
  } catch (error) {
    console.error('Error en registro:', error);
    return null;
  }
};

// Vulnerable: No revocación de token
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('userData');
};

// Vulnerable: No verificación de token
export const getCurrentUser = () => {
  const userData = localStorage.getItem('userData');
  return userData ? JSON.parse(userData) : null;
};

// Vulnerable: No validación de headers
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
