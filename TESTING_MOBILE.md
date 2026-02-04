# 🧪 Guía de Testing para Versión Móvil

## Requisitos
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Dispositivo móvil (opcional, pero recomendado)
- DevTools disponible (F12 en Chrome)

## Testing en Navegador Desktop

### Paso 1: Abrir DevTools
```
Windows/Linux: F12 o Ctrl+Shift+I
Mac: Cmd+Option+I
```

### Paso 2: Activar Device Emulation
```
Presiona Ctrl+Shift+M (o Command+Shift+M en Mac)
O haz clic en el icono de dispositivo móvil
```

### Paso 3: Seleccionar Dispositivos

#### Dispositivos Pequeños (< 576px)
- **iPhone SE** (375×667)
- **iPhone 12** (390×844) ← Muy común
- **iPhone 13** (390×844)
- **Pixel 5** (393×851) ← Android común

#### Dispositivos Medianos (576-768px)
- **iPhone 12 Max** (428×926)
- **iPhone 14 Plus** (430×932)
- **Samsung Galaxy S9** (360×740)

#### Tablets (768px+)
- **iPad** (768×1024)
- **iPad Air** (820×1180)
- **iPad Pro 11"** (834×1194)

### Paso 4: Probar Orientaciones
```
1. Click en el botón de orientación
2. Alterna entre Portrait (vertical) y Landscape (horizontal)
3. Verifica que el layout se adapte correctamente
```

## Checklist de Testing

### ✅ Navbar
- [ ] Logo visible
- [ ] Botón hamburguesa funciona en móvil
- [ ] Menú se expande/colapsa
- [ ] Se queda en la parte superior (sticky)
- [ ] No sobrepone el contenido

### ✅ Sidebar
- [ ] Se oculta en móvil
- [ ] Se muestra al hacer click en hamburguesa
- [ ] Se cierra al hacer click en un enlace
- [ ] Menús están bien espaciados
- [ ] Iconos son visibles

### ✅ Contenido Principal
- [ ] Texto legible sin zoom
- [ ] Imágenes adaptadas al tamaño
- [ ] No hay scroll horizontal innecesario
- [ ] Padding adecuado

### ✅ Tablas
- [ ] Datos visibles sin scroll
- [ ] O con scroll horizontal inteligente
- [ ] Encabezados claros
- [ ] Filas bien diferenciadas
- [ ] Botones de acción accesibles

### ✅ Formularios
- [ ] Campo de texto a 16px (no zoom en iOS)
- [ ] Etiquetas claramente visibles
- [ ] Campos con suficiente padding
- [ ] Botón submit fácil de presionar
- [ ] Validación clara

### ✅ Botones
- [ ] Área mínima 44×44px
- [ ] Espaciados entre sí
- [ ] Color de contraste adecuado
- [ ] Sin necesidad de zoom

### ✅ Páginación
- [ ] Botones claramente visibles
- [ ] Números o texto comprensible
- [ ] Funcionalidad correcta

### ✅ Dark Mode
- [ ] Colores se adaptan
- [ ] Texto legible
- [ ] Sin daño a contraste

## Pruebas Específicas por Pantalla

### iPhone 12 (390×844px)
1. Abre cualquier página con tabla (personal_list)
2. Verifica que se vea sin scroll horizontal
3. Los botones deben ser presionables
4. La tabla debe tener scroll lateral si es necesario

### iPad (768×1024px)
1. Abre la página
2. El sidebar debe ser visible
3. El contenido debe ocupar ~75% del ancho
4. Las tablas deben verse completas

### Desktop (1200px+)
1. Verificar que la interfaz sea completa
2. Sidebar visible a la izquierda
3. Contenido bien distribuido
4. Sin espacios desperdiciados

## Pruebas de Rendimiento

### Velocidad de Carga
```
DevTools > Network
- Medir tiempo de carga en 4G simulado
- Objetivo: < 2 segundos
```

### Memoria
```
DevTools > Performance
- Verificar que no haya memory leaks
- Escroliar la página y revisar uso de memoria
```

## Pruebas en Dispositivo Real

### Via Cable USB
1. Conecta tu móvil a la PC con USB
2. En Chrome: chrome://inspect
3. Abre DevTools remoto
4. Prueba igual que en emulación

### Via Red Local
1. Obtén tu IP local:
   ```bash
   ipconfig (Windows)
   ifconfig (Mac/Linux)
   ```
2. En el móvil accede a:
   ```
   http://[tu-ip]:8000/
   ```
3. Prueba todas las páginas

## Errores Comunes y Soluciones

### ❌ Scroll horizontal innecesario
**Causa:** Elemento muy ancho
**Solución:** Agregar clase `table-responsive` o ajustar max-width

### ❌ Texto muy pequeño
**Causa:** Font size muy reducido
**Solución:** No ir bajo 13px en móvil, 16px en inputs

### ❌ Botones difíciles de presionar
**Causa:** Área de toque < 44px
**Solución:** Aumentar padding o margin

### ❌ Formulario con zoom en iOS
**Causa:** Font size < 16px en inputs
**Solución:** Agregar `font-size: 16px;` en input

## Testing Automatizado (Opcional)

### Lighthouse en Chrome
```
1. Abre DevTools (F12)
2. Vai a la pestaña "Lighthouse"
3. Click en "Analyze page load"
4. Revisar reporte de Mobile Performance
```

## Reportar Problemas

Si encuentras algo que no funciona en móvil:

1. Documenta:
   - Qué dispositivo/resolución
   - Qué acción hace el problema
   - Qué esperabas
   - Qué pasó realmente

2. Envía:
   - Screenshot
   - Resolución de pantalla
   - Navegador y versión
   - Sistema operativo

## Checklist Final

Antes de considerar el testing completo:

- [ ] Probado en 3 tamaños mínimo (móvil, tablet, desktop)
- [ ] Probado en portrait y landscape
- [ ] Todos los botones funcionales
- [ ] Todas las tablas legibles
- [ ] Todas las páginas accesibles
- [ ] Sin scroll horizontal innecesario
- [ ] Dark mode se ve bien
- [ ] Performance aceptable
- [ ] No hay errores en consola
- [ ] Documentación actualizada

---

**¡Listo para usar en móviles! 📱✨**

