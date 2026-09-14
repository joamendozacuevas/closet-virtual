# Plan EVA2 — Clóset Virtual

## Alcance

La aplicación evoluciona desde ES1 a un inventario digital de prendas en Django. Las prendas se almacenan en SQLite mediante el modelo `Prenda`; `datos.json` deja de ser usado por las vistas. El sistema implementa crear, listar, editar y eliminar con borrado lógico, por lo que las prendas eliminadas conservan trazabilidad y no aparecen en el inventario activo. Incluye panel de administración, inicio y cierre de sesión, y roles `admin`, `normal` y `viewer` protegidos del lado del servidor. El despliegue futuro está proyectado en Render, usando variables de entorno para la configuración.

## Priorización MoSCoW

### Must

- Persistencia SQLite y migraciones Django para `Prenda`.
- CRUD web con validación de datos y cálculo de resultado mediante la función de decisión existente.
- Borrado lógico y fecha de eliminación.
- Panel de administración Django.
- Login, logout y autorización por roles: `admin` administra; `normal` crea; `viewer` solo consulta.

### Should

- Importar los registros históricos de `datos.json` mediante `cargar_datos.py`.
- Búsquedas y filtros adicionales para los registros.

### Could

- Adjuntar fotografías y categorías de prendas.
- Recomendaciones de combinaciones y clima.

### Won't

- Red social o publicación de outfits en esta entrega.
