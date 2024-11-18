FROM node:16-alpine

# Instalar herramientas de depuración
RUN apk add --no-cache curl wget

WORKDIR /app

# Vulnerable: Sin bloqueo de versiones en package.json
COPY package*.json ./
RUN npm install

# Configurar variables de entorno para desarrollo y logging
ENV NODE_ENV=development
ENV NODE_OPTIONS=--max_old_space_size=2048
ENV WATCHPACK_POLLING=true
ENV REACT_APP_API_URL=http://backend:8000
ENV BROWSER=none
ENV CI=false

COPY . .

# Vulnerable: Expone el puerto de desarrollo
EXPOSE 3000
CMD ["sh", "-c", "REACT_APP_API_URL=http://backend:8000 npm start"]
