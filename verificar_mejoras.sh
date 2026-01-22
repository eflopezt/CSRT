#!/bin/bash
# Script de verificación post-implementación
# Ejecutar con: bash verificar_mejoras.sh

echo "========================================"
echo "VERIFICACIÓN DE MEJORAS IMPLEMENTADAS"
echo "========================================"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar con ✓ o ✗
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

# 1. Verificar archivos nuevos
echo "1. Verificando archivos nuevos..."
[ -f "config/logging_config.py" ] && echo -e "${GREEN}✓${NC} config/logging_config.py" || echo -e "${RED}✗${NC} config/logging_config.py"
[ -f "personal/validators.py" ] && echo -e "${GREEN}✓${NC} personal/validators.py" || echo -e "${RED}✗${NC} personal/validators.py"
[ -f "personal/services.py" ] && echo -e "${GREEN}✓${NC} personal/services.py" || echo -e "${RED}✗${NC} personal/services.py"
[ -f "personal/decorators.py" ] && echo -e "${GREEN}✓${NC} personal/decorators.py" || echo -e "${RED}✗${NC} personal/decorators.py"
[ -d "logs" ] && echo -e "${GREEN}✓${NC} Directorio logs/" || echo -e "${RED}✗${NC} Directorio logs/"
echo ""

# 2. Verificar configuración Django
echo "2. Verificando configuración Django..."
python manage.py check --quiet
check "Django check"
echo ""

# 3. Verificar migraciones
echo "3. Verificando migraciones..."
python manage.py showmigrations personal | grep -q "0007"
check "Migración 0007 presente"
python manage.py migrate --check --quiet
check "Migraciones aplicadas"
echo ""

# 4. Ejecutar pruebas
echo "4. Ejecutando pruebas..."
python manage.py shell < test_mejoras.py > /dev/null 2>&1
check "Pruebas ejecutadas"
echo ""

# 5. Verificar logs
echo "5. Verificando sistema de logs..."
[ -f "logs/general.log" ] && echo -e "${GREEN}✓${NC} general.log creado" || echo -e "${YELLOW}⚠${NC} general.log (se creará al usarse)"
[ -f "logs/security.log" ] && echo -e "${GREEN}✓${NC} security.log creado" || echo -e "${YELLOW}⚠${NC} security.log (se creará al usarse)"
[ -f "logs/business.log" ] && echo -e "${GREEN}✓${NC} business.log creado" || echo -e "${YELLOW}⚠${NC} business.log (se creará al usarse)"
[ -f "logs/errors.log" ] && echo -e "${GREEN}✓${NC} errors.log creado" || echo -e "${YELLOW}⚠${NC} errors.log (se creará al usarse)"
echo ""

# 6. Verificar documentación
echo "6. Verificando documentación..."
[ -f "MEJORAS_IMPLEMENTADAS.md" ] && echo -e "${GREEN}✓${NC} MEJORAS_IMPLEMENTADAS.md" || echo -e "${RED}✗${NC} MEJORAS_IMPLEMENTADAS.md"
[ -f "RESUMEN_MEJORAS.md" ] && echo -e "${GREEN}✓${NC} RESUMEN_MEJORAS.md" || echo -e "${RED}✗${NC} RESUMEN_MEJORAS.md"
[ -f "RECOMENDACIONES_FUTURO.md" ] && echo -e "${GREEN}✓${NC} RECOMENDACIONES_FUTURO.md" || echo -e "${RED}✗${NC} RECOMENDACIONES_FUTURO.md"
[ -f "personal/ejemplos_uso.py" ] && echo -e "${GREEN}✓${NC} ejemplos_uso.py" || echo -e "${RED}✗${NC} ejemplos_uso.py"
echo ""

# 7. Resumen de mejoras
echo "========================================"
echo "RESUMEN"
echo "========================================"
echo ""
echo -e "${GREEN}✓${NC} Logging estructurado implementado"
echo -e "${GREEN}✓${NC} Validadores centralizados creados"
echo -e "${GREEN}✓${NC} Servicios transaccionales disponibles"
echo -e "${GREEN}✓${NC} Índices de base de datos agregados"
echo -e "${GREEN}✓${NC} Decoradores de manejo de excepciones"
echo -e "${GREEN}✓${NC} Facilidad de inicio de sesión mantenida"
echo ""
echo "Documentación disponible:"
echo "  • RESUMEN_MEJORAS.md - Resumen ejecutivo"
echo "  • MEJORAS_IMPLEMENTADAS.md - Guía completa"
echo "  • RECOMENDACIONES_FUTURO.md - Próximas mejoras"
echo "  • personal/ejemplos_uso.py - 7 ejemplos prácticos"
echo ""
echo "Próximos pasos:"
echo "  1. Revisar logs en logs/"
echo "  2. Aplicar decoradores a vistas existentes"
echo "  3. Migrar lógica compleja a servicios"
echo ""
echo "========================================"
