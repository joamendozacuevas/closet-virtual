# Documentación de uso de IA — EVA2

## Entrada 1: motor de decisión y usuarios

1. **Qué pedí textual:** “Genera las vistas CRUD para prendas reutilizando la función `decidir()` de `solucion.py` y crea los usuarios y grupos necesarios.”
2. **Qué me respondió:** La IA propuso importar una función llamada `decidir` y añadió un script `crear_usuarios.py` para crear grupos y usuarios con contraseñas desde variables de entorno.
3. **Qué estaba mal o sobraba:** El motor existente del repositorio se llama `evaluar_prenda(estado, formalidad_prenda, formalidad_ocasion)`, no `decidir`. Además, los usuarios y grupos ya existían en SQLite, por lo que recrearlos podía modificar cuentas existentes.
4. **Qué hice yo y por qué:** Importé y llamé directamente a `evaluar_prenda` sin modificar ni copiar su lógica. Eliminé el script de usuarios para conservar la estructura de autenticación ya creada.

## Entrada 2: configuración de correo

1. **Qué pedí textual:** “Configura el correo de desarrollo en `settings.py`.”
2. **Qué me respondió:** La IA agregó un diccionario `MAILERS` con un backend de consola.
3. **Qué estaba mal o sobraba:** `MAILERS` no es una configuración nativa de Django y el framework no la utiliza para enviar correos.
4. **Qué hice yo y por qué:** Reemplacé ese bloque por `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`, que es la configuración oficial de Django para desarrollo.

## Entrada 3: formalidad de la ocasión

1. **Qué pedí textual:** “Crea el formulario para registrar y editar prendas, recalculando la decisión según el estado y la formalidad.”
2. **Qué me respondió:** La IA añadió un input de ocasión, pero lo precargó con `{{ prenda.formalidad }}` y no agregó `formalidad_ocasion` al modelo.
3. **Qué estaba mal o sobraba:** Al editar, se perdía el valor original de la ocasión y el resultado se podía recalcular con un dato equivocado. El dato tampoco quedaba persistido en SQLite.
4. **Qué hice yo y por qué:** Agregué `formalidad_ocasion` a `Prenda`, su migración y un `PrendaForm`. El formulario se instancia con la prenda existente, por lo que muestra y guarda el valor correcto antes de recalcular la decisión.
