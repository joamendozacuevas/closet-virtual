import json
import uuid

from django.conf import settings
from django.db import migrations


def importar_datos_json(apps, schema_editor):
    archivo = settings.BASE_DIR / 'datos.json'
    if not archivo.exists():
        return

    Prenda = apps.get_model('core', 'Prenda')
    with archivo.open(encoding='utf-8') as fuente:
        registros = json.load(fuente)

    for registro in registros:
        try:
            identificador = uuid.UUID(str(registro.get('id', uuid.uuid4())))
            estado = str(registro.get('estado_limpieza', 'limpio')).lower()
            formalidad_prenda = int(registro.get('formalidad_prenda', 0))
            formalidad_ocasion = int(registro.get('formalidad_ocasion', 0))
        except (TypeError, ValueError):
            continue

        resultado = registro.get('resultado', 'Dato inválido')
        Prenda.objects.using(schema_editor.connection.alias).get_or_create(
            id=identificador,
            defaults={
                'nombre': str(registro.get('nombre', 'Prenda'))[:120],
                'color': str(registro.get('color', 'Sin especificar'))[:80],
                'estado_limpieza': estado,
                'formalidad_prenda': formalidad_prenda,
                'formalidad_ocasion': formalidad_ocasion,
                'resultado': str(resultado)[:160],
            },
        )


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]

    operations = [
        migrations.RunPython(importar_datos_json, migrations.RunPython.noop),
    ]
