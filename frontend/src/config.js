// En desarrollo con Docker, usamos el nombre del servicio del backend
// En producción, usamos la variable de entorno
export const API_URL = process.env.REACT_APP_API_URL || "http://backend:8000";
console.log('API_URL configured as:', API_URL);

// Configuración adicional para debugging
export const DEBUG = process.env.NODE_ENV === 'development';
if (DEBUG) {
  console.log('Running in development mode');
  console.log('Environment variables:', process.env);
}
