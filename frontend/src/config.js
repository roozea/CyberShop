// En desarrollo con Docker, usamos el nombre del servicio 'backend'
// En producción o desarrollo local, usamos la variable de entorno o localhost
export const API_URL = process.env.REACT_APP_API_URL || "http://backend:8000";
console.log('API_URL configured as:', process.env.REACT_APP_API_URL || "http://backend:8000");
