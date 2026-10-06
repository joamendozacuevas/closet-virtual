# Clóset Virtual - Validador de Prendas

Prueba de Concepto (POC) desarrollada para la evaluación ES1 de Programación Back End en Inacap. El sistema evalúa si una prenda es apta para una ocasión determinada, comparando el nivel de formalidad de la prenda con el nivel requerido para la ocasión.

## Características

- Validación por consola mediante `solucion.py`.
- Registro de nombre, color, estado de limpieza y niveles de formalidad.
- Clasificación en cuatro resultados: `Aceptado`, `Rechazo 1`, `Rechazo 2` y `Dato Inválido`.
- Persistencia local en el archivo `datos.json`.
- Interfaz web desarrollada con Django y Bootstrap 5.
- Lectura y CRUD de prendas mediante las vistas de `core/views.py`.
- API REST para prendas con Django REST Framework, autenticación por token y Swagger.
- SQLite y migraciones compartidas por las páginas HTML de ES2 y la API. La migración inicial importa los registros existentes de `datos.json`.

## Stack Tecnológico

- Python 3
- Django
- Django REST Framework
- drf-spectacular
- Bootstrap 5
- JSON
- python-decouple
- tabulate

## Requisitos Previos

- Python 3 instalado.
- Git instalado.
- Acceso a una terminal.
- Visual Studio Code u otro editor de código (opcional).

## Instalación y Configuración

1. Clona el repositorio:

   ```bash
   git clone https://github.com/joamendozacuevas/closet-virtual.git
   cd closet-virtual
   ```

2. Crea el entorno virtual:

   ```bash
   python3 -m venv entorno
   ```

3. Activa el entorno virtual:

   En macOS o Linux:

   ```bash
   source entorno/bin/activate
   ```

   En Windows PowerShell:

   ```powershell
   .\entorno\Scripts\Activate.ps1
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Entra a la carpeta del proyecto Django:

   ```bash
   cd miproyecto
   ```

6. Crea el archivo local `.env` a partir de la plantilla pública (desde `miproyecto`):

   En macOS o Linux:

   ```bash
   cp ../.env.example ../.env
   ```

   En Windows PowerShell:

   ```powershell
   Copy-Item ..\.env.example ..\.env
   ```

7. Reemplaza `SECRET_KEY=tu-clave-aqui` en `.env` por una clave local propia. Mantén `.env` fuera del repositorio; el archivo está protegido por `.gitignore`.

## Cómo Ejecutarlo

### Versión de consola

Desde `closet-virtual/miproyecto`, con el entorno virtual activo:

```bash
python3 solucion.py
```

El programa solicitará los datos de la prenda, mostrará la decisión y guardará el registro en `datos.json`.

### Servidor Django

Desde `closet-virtual/miproyecto`, con el entorno virtual activo:

```bash
python3 manage.py runserver
```

Luego abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en el navegador.

La interfaz permite agregar, consultar, editar y eliminar prendas almacenadas en SQLite.

Antes de iniciar Django por primera vez, desde `closet-virtual/miproyecto` aplica las migraciones:

```bash
python3 manage.py migrate
```

### API REST

La API requiere autenticación por token. Crea un usuario para desarrollo con `python3 manage.py createsuperuser` y solicita un token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"TU_USUARIO","password":"TU_CLAVE"}'
```

La respuesta incluye el token y su vencimiento (una hora). Usa el token en el encabezado `Authorization: Token TU_TOKEN`. Al solicitar otro token para el mismo usuario, el anterior se invalida. El endpoint limita la emisión a 10 solicitudes por hora.

- `GET/POST /api/prendas/`: listar (paginado) y crear prendas.
- `GET/PUT/PATCH/DELETE /api/prendas/{id}/`: consultar, actualizar o eliminar una prenda. El borrado requiere un usuario staff.
- `GET /api/docs/`: documentación Swagger.
- `GET /api/schema/`: esquema OpenAPI.

La API responde en JSON, con paginación de 10 registros y mensajes de validación de DRF. La API y las vistas HTML de ES2 comparten el modelo `Prenda` y la misma base de datos SQLite. La migración `0002` importa los registros existentes de `datos.json` una sola vez. El JSON original se conserva sin cambios como respaldo de ese momento; los cambios posteriores se guardan en SQLite.

En producción, usa HTTPS y un caché compartido para que el límite de solicitudes al endpoint de token se aplique entre todos los procesos del servidor.

## Seguridad

- No subir `.env` a GitHub.
- Usar `.env.example` como plantilla sin credenciales reales.
- Mantener `.env` fuera de GitHub y usar HTTPS en despliegues para proteger las credenciales y los tokens.
- La migración desde `datos.json` se ejecuta una sola vez. Los cambios posteriores se guardan en SQLite, así que no vuelvas a importar el JSON inicial como si fuera una copia actualizada.
