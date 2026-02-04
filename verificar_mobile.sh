#!/bin/bash
# Script para verificar las mejoras de responsive design

echo "================================"
echo "🔍 Verificando Mejoras Móviles"
echo "================================"
echo ""

# Verificar archivos modificados
echo "📁 Archivos modificados:"
echo "✅ templates/base.html"
echo "✅ static/css/responsive-mobile.css (NUEVO)"
echo "✅ templates/personal/personal_list.html"
echo ""

# Verificar cambios en base.html
echo "🔎 Verificando base.html..."
if grep -q "sticky-top" templates/base.html; then
    echo "  ✅ Navbar sticky detectado"
else
    echo "  ❌ Navbar sticky NO encontrado"
fi

if grep -q "sidebarNav" templates/base.html; then
    echo "  ✅ Sidebar colapsable detectado"
else
    echo "  ❌ Sidebar colapsable NO encontrado"
fi

if grep -q "responsive-mobile.css" templates/base.html; then
    echo "  ✅ CSS responsive vinculado"
else
    echo "  ❌ CSS responsive NO vinculado"
fi

echo ""

# Verificar archivo CSS responsivo
echo "🎨 Verificando responsive-mobile.css..."
if [ -f "static/css/responsive-mobile.css" ]; then
    echo "  ✅ Archivo CSS responsivo existe"
    LINES=$(wc -l < static/css/responsive-mobile.css)
    echo "  📊 Líneas de CSS: $LINES"
    
    # Verificar media queries
    MEDIA_QUERIES=$(grep -c "@media" static/css/responsive-mobile.css)
    echo "  📱 Media queries: $MEDIA_QUERIES"
else
    echo "  ❌ Archivo CSS responsivo NO existe"
fi

echo ""

# Verificar mejoras en personal_list.html
echo "📋 Verificando personal_list.html..."
if grep -q "d-none d-sm-inline" templates/personal/personal_list.html; then
    echo "  ✅ Clases de visibilidad responsiva detectadas"
else
    echo "  ❌ Clases de visibilidad NO encontradas"
fi

if grep -q "d-none d-md-table-cell" templates/personal/personal_list.html; then
    echo "  ✅ Columnas responsivas detectadas"
else
    echo "  ❌ Columnas responsivas NO detectadas"
fi

echo ""
echo "================================"
echo "✅ Verificación completada"
echo "================================"
echo ""
echo "📱 Para probar en móvil:"
echo "1. Abre el navegador (Chrome/Firefox)"
echo "2. Presiona F12 para DevTools"
echo "3. Haz clic en el icono de dispositivo móvil"
echo "4. Selecciona diferentes dispositivos (iPhone, Pixel, iPad)"
echo "5. Prueba las vistas en orientación portrait y landscape"
echo ""
