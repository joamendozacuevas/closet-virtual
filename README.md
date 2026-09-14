# Clóset Virtual — EVA2

Aplicación Django para administrar un inventario de prendas persistido en SQLite. Incluye CRUD, borrado lógico, administración Django y control de acceso mediante los grupos existentes `admin`, `normal` y `viewer`.

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

## Datos históricos y usuarios

Desde `miproyecto/`:

```bash
python cargar_datos.py
```

Los grupos y usuarios ya existentes en SQLite se conservan y no se generan ni modifican mediante scripts. Los datos históricos de `datos.json` se importan a SQLite una vez mediante el comando anterior; las vistas web ya no lo modifican.

## Roles

- `admin`: lista, crea, edita y realiza borrado lógico.
- `normal`: lista y crea.
- `viewer`: solo lista.
