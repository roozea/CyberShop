// En desarrollo con Docker, usamos localhost para acceder desde el navegador
// En producción, usamos la variable de entorno
export const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
console.log('API_URL configured as:', process.env.REACT_APP_API_URL || "http://localhost:8000");
