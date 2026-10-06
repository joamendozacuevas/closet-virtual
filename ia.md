# Documentación de uso de IA (Criterio 1.1.4)

1. **Herramienta utilizada:** Codex / GitHub Copilot (integrado en VS Code) y Gemini.
2. **Para qué la consulté:** Para estructurar la lógica de decisión en Python cumpliendo con la regla de los 4 resultados, y para integrar la lectura del archivo JSON dentro de la vista de Django sin usar bases de datos.
3. **Consulta concreta:** "Genera la estructura if/elif para evaluar 5 variables (nombre, color, estado, formalidad prenda, formalidad ocasión) que retorne 4 casos exactos: dato inválido, rechazado por suciedad, rechazado por nivel de formalidad y aceptado."
4. **Correcciones manuales:** La IA inicialmente intentó crear un archivo `models.py` para guardar el "objeto" prenda. Tuve que corregir esto manualmente e indicarle por prompt que construyera un diccionario de Python y lo inyectara directamente en `datos.json` mediante la librería `json`, respetando la restricción de no usar bases de datos de la Fase 0.

## Documentación IA para ES3 (criterio 3.1.4)

1. **Herramienta utilizada:** Codex.
2. **Para qué la consulté:** Para integrar Django REST Framework, autenticación por token, permisos, serialización y documentación OpenAPI manteniendo las vistas HTML de ES2.
3. **Recomendación de seguridad descartada:** Durante la revisión descarté usar autenticación básica enviando usuario y contraseña en cada petición. Aunque DRF la permite, no es adecuada para este API porque expone credenciales repetidamente y depende de HTTPS para protegerlas en tránsito. Elegí tokens de DRF; en producción también se debe servir la API únicamente por HTTPS y proteger los tokens.
4. **Decisión de arquitectura:** ES2 guardaba sus datos en `datos.json` y no tenía modelos ni `ModelForm`. Para satisfacer `ModelSerializer`/`ModelViewSet` y compartir datos entre ES2 y la API, ES3 añade el modelo `Prenda`, SQLite y una migración que importa los registros JSON existentes una vez. Conservé las rutas, formularios y operaciones HTML, y adapté las vistas para usar el mismo modelo/base de datos que la API. El archivo JSON original queda como respaldo sin actualizarse con los cambios nuevos.
