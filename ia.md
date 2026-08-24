# Documentación de uso de IA (Criterio 1.1.4)

1. **Herramienta utilizada:** Codex / GitHub Copilot (integrado en VS Code) y Gemini.
2. **Para qué la consulté:** Para estructurar la lógica de decisión en Python cumpliendo con la regla de los 4 resultados, y para integrar la lectura del archivo JSON dentro de la vista de Django sin usar bases de datos.
3. **Consulta concreta:** "Genera la estructura if/elif para evaluar 5 variables (nombre, color, estado, formalidad prenda, formalidad ocasión) que retorne 4 casos exactos: dato inválido, rechazado por suciedad, rechazado por nivel de formalidad y aceptado."
4. **Correcciones manuales:** La IA inicialmente intentó crear un archivo `models.py` para guardar el "objeto" prenda. Tuve que corregir esto manualmente e indicarle por prompt que construyera un diccionario de Python y lo inyectara directamente en `datos.json` mediante la librería `json`, respetando la restricción de no usar bases de datos de la Fase 0.