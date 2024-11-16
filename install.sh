#!/bin/bash

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Función para mostrar el menú de instalación
show_menu() {
    clear
    echo -e "${GREEN}=== CyberShop Vulnerable Lab - Menú de Instalación ===${NC}"
    echo -e "${YELLOW}1) Instalación Sin Guía (Pre-evaluación)${NC}"
    echo -e "${YELLOW}2) Instalación Con Guía (Post-evaluación)${NC}"
    echo -e "${YELLOW}3) Salir${NC}"
    echo
    read -p "Seleccione una opción (1-3): " choice
}

# Procesar modo de instalación
WITH_GUIDE=false

# Mostrar menú y procesar selección
while true; do
    if [ "$1" = "--with-guide" ]; then
        WITH_GUIDE=true
        break
    elif [ "$1" = "--no-guide" ]; then
        WITH_GUIDE=false
        break
    elif [ -z "$1" ]; then
        show_menu
        case $choice in
            1)
                WITH_GUIDE=false
                break
                ;;
            2)
                WITH_GUIDE=true
                break
                ;;
            3)
                echo -e "${YELLOW}Saliendo...${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Opción inválida${NC}"
                sleep 2
                ;;
        esac
    fi
done

# Mostrar modo de instalación seleccionado
if [ "$WITH_GUIDE" = true ]; then
    echo -e "${GREEN}🚀 Iniciando instalación de CyberShop Vulnerable Lab (Modo: Con Guía)...${NC}"
else
    echo -e "${GREEN}🚀 Iniciando instalación de CyberShop Vulnerable Lab (Modo: Evaluación)...${NC}"
fi

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

# Eliminar guía si no se solicitó
if [ "$WITH_GUIDE" = false ]; then
    echo -e "${YELLOW}🔒 Modo evaluación: Eliminando guía de vulnerabilidades...${NC}"
    rm -f VULNERABILITIES.md
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

if [ "$WITH_GUIDE" = true ]; then
    echo -e "${YELLOW}📚 La guía de vulnerabilidades está disponible en: VULNERABILITIES.md${NC}"
else
    echo -e "${YELLOW}📝 Modo evaluación: La guía de vulnerabilidades no está incluida${NC}"
fi

echo -e "${RED}⚠️  ADVERTENCIA: Esta aplicación es intencionalmente vulnerable.${NC}"
echo -e "${RED}⚠️  NO USAR EN PRODUCCIÓN${NC}"

# Instrucciones post-instalación
echo -e "\n${YELLOW}📌 Comandos útiles:${NC}"
echo -e "   - make help     : Ver todos los comandos disponibles"
echo -e "   - make stop     : Detener la aplicación"
echo -e "   - make clean    : Limpiar contenedores y volúmenes"
echo -e "   - make dev      : Iniciar en modo desarrollo"

# Mostrar información sobre modos de instalación
echo -e "\n${YELLOW}📌 Modos de instalación:${NC}"
echo -e "   - ./install.sh          : Modo evaluación (sin guía)"
echo -e "   - ./install.sh --with-guide : Modo revisión (con guía)"
