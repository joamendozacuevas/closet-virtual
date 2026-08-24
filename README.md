# Clóset Virtual - Validador de Prendas

Prueba de Concepto (POC) desarrollada para la evaluación ES1 de Programación Back End en Inacap. El sistema evalúa si una prenda es apta para una ocasión determinada, comparando el nivel de formalidad de la prenda con el nivel requerido para la ocasión.

## Características

- Validación por consola mediante `solucion.py`.
- Registro de nombre, color, estado de limpieza y niveles de formalidad.
- Clasificación en cuatro resultados: `Aceptado`, `Rechazo 1`, `Rechazo 2` y `Dato Inválido`.
- Persistencia local en el archivo `datos.json`.
- Interfaz web desarrollada con Django y Bootstrap 5.
- Lectura y CRUD de prendas mediante las vistas de `core/views.py`.
- No utiliza bases de datos, SQLite ni migraciones.

## Stack Tecnológico

- Python 3
- Django
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

6. Crea el archivo local `.env` a partir de la plantilla pública:

   En macOS o Linux:

   ```bash
   cp .env.example .env
   ```

   En Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
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

La interfaz permite agregar, consultar, editar y eliminar prendas almacenadas en `datos.json`.

## Seguridad

- No subir `.env` a GitHub.
- Usar `.env.example` como plantilla sin credenciales reales.
- No se almacenan datos en una base de datos; toda la persistencia se realiza en `datos.json`.
