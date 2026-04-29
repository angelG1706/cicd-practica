#!/bin/bash
# =============================================================
# SCRIPT DE DEPLOY AUTOMATIZADO
# Simula lo que haría un pipeline en un servidor real
# =============================================================

set -e  # Si cualquier comando falla, el script se detiene

NOMBRE_APP="cicd-practica"
PUERTO=5000
IMAGEN="$NOMBRE_APP:latest"

echo "=========================================="
echo "  INICIANDO DEPLOY AUTOMATIZADO"
echo "  Fecha: $(date)"
echo "=========================================="

# PASO 1: Verificar que las pruebas pasen
echo ""
echo "▶ PASO 1: Ejecutando pruebas..."
source venv/bin/activate
pytest test_app.py -v --tb=short

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Las pruebas fallaron. Deploy cancelado."
    exit 1
fi
echo "✅ Todas las pruebas pasaron"

# PASO 2: Construir imagen Docker
echo ""
echo "▶ PASO 2: Construyendo imagen Docker..."
docker build -t $IMAGEN .
echo "✅ Imagen construida: $IMAGEN"

# PASO 3: Detener contenedor anterior si existe
echo ""
echo "▶ PASO 3: Reemplazando versión anterior..."
docker stop $NOMBRE_APP 2>/dev/null && echo "  Contenedor anterior detenido" || echo "  No había contenedor previo"
docker rm $NOMBRE_APP 2>/dev/null || true

# PASO 4: Iniciar nuevo contenedor
echo ""
echo "▶ PASO 4: Iniciando nueva versión..."
docker run -d \
    --name $NOMBRE_APP \
    -p $PUERTO:5000 \
    --restart unless-stopped \
    $IMAGEN

# PASO 5: Verificar que la app está corriendo
echo ""
echo "▶ PASO 5: Verificando que la app responde..."
sleep 3  # Esperar a que arranque

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PUERTO/salud)

if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ ¡DEPLOY EXITOSO!"
    echo ""
    echo "=========================================="
    echo "  App corriendo en: http://localhost:$PUERTO"
    echo "  Prueba con: curl http://localhost:$PUERTO"
    echo "=========================================="
else
    echo "❌ ERROR: La app no responde (HTTP $HTTP_CODE)"
    docker logs $NOMBRE_APP
    exit 1
fi
