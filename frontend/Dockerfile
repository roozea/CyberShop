FROM node:16-alpine

WORKDIR /app

# Vulnerable: Sin bloqueo de versiones en package.json
COPY package*.json ./
RUN npm install

# Configurar variables de entorno para mejorar la estabilidad
ENV NODE_OPTIONS=--max_old_space_size=2048
ENV WATCHPACK_POLLING=true

COPY . .

# Vulnerable: Expone el puerto de desarrollo
EXPOSE 3000
CMD ["sh", "-c", "npm start || (sleep 5 && npm start)"]
