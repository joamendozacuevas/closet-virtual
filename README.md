# Clóset Virtual — EVA2

Aplicación Django con registros persistidos en SQLite. Incluye CRUD, borrado lógico, administración Django y control de acceso mediante los grupos `admin`, `normal` y `viewer`.

## Puesta en marcha

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd miproyecto
python manage.py migrate
python manage.py runserver
```

Copie `.env.example` como `miproyecto/.env` y asigne valores locales a `SECRET_KEY` y `DEBUG`. El archivo de ejemplo solo enumera variables y no contiene secretos.

## Datos y usuarios

Desde `miproyecto/`:

```bash
python cargar_datos.py
ADMIN_PASSWORD='una-clave-segura' NORMAL_PASSWORD='otra-clave' VIEWER_PASSWORD='otra-clave' python crear_usuarios.py
```

El segundo comando crea los grupos y usuarios `admin`, `normal` y `viewer`; `admin` es superusuario y puede ingresar a `/admin/`. Las contraseñas solo se leen desde variables de entorno. Los datos históricos de `datos.json` se importan a SQLite una vez mediante el primer comando; las vistas web ya no lo modifican.

## Roles

- `admin`: lista, crea, edita y realiza borrado lógico.
- `normal`: lista y crea.
- `viewer`: solo lista.
