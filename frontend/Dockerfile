# Build stage
FROM node:16-alpine as builder

# Instalar herramientas de depuración
RUN apk add --no-cache curl wget

WORKDIR /app

# Copiar solo los archivos necesarios para instalar dependencias
COPY package*.json ./
RUN npm install

# Configurar variables de entorno para construcción
ENV NODE_ENV=production
ENV REACT_APP_API_URL=http://localhost:8000
ENV CI=false

# Copiar el resto de los archivos y construir
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copiar la configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos construidos
COPY --from=builder /app/build /usr/share/nginx/html

# Exponer puerto 3000 (vulnerable intencionalmente)
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
