# Manuales de Usuario

Este directorio contiene los manuales de usuario del sistema CSRT.

## Archivos Disponibles

### Manual de Usuario para Responsables de Área
**Archivo:** `Manual_Usuario_Responsables_Area.pdf`

Manual completo que explica:
- Cómo acceder al sistema
- Navegación por el menú principal
- Gestión de personal
- Uso del Roster Matricial
- Códigos y su significado
- Preguntas frecuentes

## Regenerar el Manual

Si necesita actualizar el manual con nueva información:

```bash
cd docs/manuales
python generar_manual.py
```

Esto generará un nuevo archivo PDF con la fecha actualizada.

## Requisitos

Para regenerar el manual necesita:
- Python 3.8+
- reportlab
- Pillow

Instalar con:
```bash
pip install reportlab Pillow
```

## Personalización

Puede editar el archivo `generar_manual.py` para:
- Agregar nuevas secciones
- Modificar contenido existente
- Cambiar colores y estilos
- Añadir imágenes
- Actualizar información

## Distribución

El manual generado puede ser:
- Enviado por correo electrónico
- Publicado en la intranet
- Impreso para distribución física
- Compartido en plataformas colaborativas
