#!/bin/bash

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Iniciando instalación de CyberShop Vulnerable Lab...${NC}"

# Verificar si se está ejecutando como root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Este script debe ejecutarse como root (sudo)${NC}"
    exit 1
fi

# Actualizar sistema
echo -e "${YELLOW}📦 Actualizando sistema...${NC}"
apt-get update
apt-get upgrade -y

# Instalar dependencias básicas
echo -e "${YELLOW}📦 Instalando dependencias básicas...${NC}"
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    git \
    make

# Instalar Docker
echo -e "${YELLOW}🐳 Instalando Docker...${NC}"
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker $SUDO_USER

# Instalar Docker Compose
echo -e "${YELLOW}🐳 Instalando Docker Compose...${NC}"
curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verificar instalaciones
echo -e "${YELLOW}✅ Verificando instalaciones...${NC}"
docker --version
docker-compose --version

# Clonar repositorio
echo -e "${YELLOW}📥 Clonando repositorio...${NC}"
if [ -d "CyberShop" ]; then
    echo -e "${YELLOW}El directorio CyberShop ya existe. Actualizando...${NC}"
    cd CyberShop
    git pull origin feature/vulnerable-app
else
    git clone https://github.com/roozea/CyberShop.git
    cd CyberShop
    git checkout feature/vulnerable-app
fi

# Configurar permisos
echo -e "${YELLOW}🔒 Configurando permisos...${NC}"
chown -R $SUDO_USER:$SUDO_USER .
chmod +x Makefile

# Desplegar aplicación
echo -e "${YELLOW}🚀 Desplegando aplicación...${NC}"
make install

# Verificar estado
echo -e "${YELLOW}✅ Verificando estado de los contenedores...${NC}"
docker ps

echo -e "${GREEN}✨ Instalación completada exitosamente!${NC}"
echo -e "${YELLOW}📝 La aplicación está disponible en:${NC}"
echo -e "   Frontend: http://localhost:3000"
echo -e "   Backend API: http://localhost:8000"
echo -e "   API Docs: http://localhost:8000/docs"
echo -e "${RED}⚠️  ADVERTENCIA: Esta aplicación es intencionalmente vulnerable.${NC}"
echo -e "${RED}⚠️  NO USAR EN PRODUCCIÓN${NC}"

# Instrucciones post-instalación
echo -e "\n${YELLOW}📌 Comandos útiles:${NC}"
echo -e "   - make help     : Ver todos los comandos disponibles"
echo -e "   - make stop     : Detener la aplicación"
echo -e "   - make clean    : Limpiar contenedores y volúmenes"
echo -e "   - make dev      : Iniciar en modo desarrollo"
