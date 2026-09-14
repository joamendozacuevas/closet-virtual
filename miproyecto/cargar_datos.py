"""Importa los registros históricos de datos.json a SQLite una sola vez."""
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miproyecto.settings')

import django

django.setup()

from core.models import Registro
from core.views import decidir


def main():
    ruta = os.path.join(os.path.dirname(__file__), 'datos.json')
    with open(ruta, encoding='utf-8') as archivo:
        datos = json.load(archivo)
    creados = 0
    for dato in datos:
        cantidad = dato.get('cantidad', dato.get('formalidad_prenda'))
        estado = dato.get('estado')
        if estado not in Registro.Estado.values:
            estado = 'al dia' if dato.get('estado_limpieza') == 'limpio' else 'moroso'
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            continue
        Registro.objects.create(
            nombre=dato.get('nombre', 'Sin nombre'), cantidad=cantidad,
            estado=estado, resultado=decidir(cantidad, estado),
        )
        creados += 1
    print(f'{creados} registros importados.')


if __name__ == '__main__':
    main()
