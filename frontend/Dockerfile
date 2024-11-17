FROM node:16-alpine

WORKDIR /app

# Vulnerable: Sin bloqueo de versiones en package.json
COPY package*.json ./
RUN npm install

COPY . .

# Vulnerable: Expone el puerto de desarrollo
EXPOSE 3000
CMD ["npm", "start"]
