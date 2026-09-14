# Documentación de uso de IA (EVA2)

- **Herramienta utilizada:** Codex de OpenAI.
- **Pregunta textual:** “¿Cómo creo en Django un modelo `Registro` con SQLite, migraciones, borrado lógico, CRUD protegido por grupos `admin`, `normal` y `viewer`, sin reescribir la función `decidir()` de `solucion.py`?”
- **Aplicación de la respuesta:** Se usó como guía para el modelo, el registro de administración, las migraciones, vistas con `login_required` y decoradores de roles, y scripts de carga y usuarios.
- **Correcciones realizadas:** El repositorio ES1 no tenía la función `decidir(cantidad, estado)` indicada: contiene `evaluar_prenda(estado, formalidad_prenda, formalidad_ocasion)`. No se modificó esa función; se añadió una capa de compatibilidad temporal en las vistas para importarla y reutilizarla. Además, el proyecto llama `core` a la app, por lo que el modelo se creó en `core/models.py` y no en una carpeta inexistente llamada `app`.
