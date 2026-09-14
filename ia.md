# Documentación de uso de IA (EVA2)

- **Herramienta utilizada:** Codex de OpenAI.
- **Pregunta textual:** “¿Cómo creo en Django un modelo `Prenda` para un clóset virtual con SQLite, migraciones, borrado lógico y CRUD protegido por los grupos existentes `admin`, `normal` y `viewer`, sin reescribir el motor de decisión de `solucion.py`?”
- **Aplicación de la respuesta:** Se usó como guía para el modelo, el registro de administración, las migraciones, vistas con `login_required`, decoradores de roles y la importación de datos históricos.
- **Correcciones realizadas:** El repositorio ES1 no contiene una función llamada `decidir`; contiene `evaluar_prenda(estado, formalidad_prenda, formalidad_ocasion)`. No se modificó ni copió esa función: las vistas la importan y la llaman directamente. También se conservó la estructura de usuarios y grupos ya existente, por lo que se eliminó el script que intentaba crear usuarios.
