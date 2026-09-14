# Plan EVA2 — Clóset Virtual

## Alcance

La aplicación evoluciona desde ES1 a una aplicación Django persistente. Los registros se almacenan en SQLite mediante el modelo `Registro`; ya no se escriben desde las vistas en `datos.json`. El sistema implementa crear, listar, editar y eliminar con borrado lógico, por lo que los registros eliminados conservan trazabilidad y no aparecen en el listado activo. Incluye panel de administración, inicio y cierre de sesión, y roles `admin`, `normal` y `viewer` protegidos del lado del servidor.

## Priorización MoSCoW

### Must

- Persistencia SQLite y migraciones Django para `Registro`.
- CRUD web con validación de enteros y cálculo de resultado mediante la función de decisión existente.
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
