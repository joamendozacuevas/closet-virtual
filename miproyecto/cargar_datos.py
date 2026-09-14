"""Importa los registros históricos de datos.json a SQLite una sola vez."""
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miproyecto.settings')

import django

django.setup()

from core.models import Prenda
from solucion import evaluar_prenda


def main():
    ruta = os.path.join(os.path.dirname(__file__), 'datos.json')
    with open(ruta, encoding='utf-8') as archivo:
        datos = json.load(archivo)
    creados = 0
    for dato in datos:
        formalidad = dato.get('formalidad', dato.get('formalidad_prenda'))
        estado = dato.get('estado_limpieza', dato.get('estado', '')).lower()
        if estado not in Prenda.Estado.values:
            estado = 'limpio'
        try:
            formalidad = int(formalidad)
            formalidad_ocasion = int(dato.get('formalidad_ocasion', formalidad))
        except (TypeError, ValueError):
            continue
        if not 1 <= formalidad <= 10 or not 1 <= formalidad_ocasion <= 10:
            continue
        Prenda.objects.create(
            nombre=dato.get('nombre', 'Sin nombre'),
            color=dato.get('color', 'Sin especificar'),
            tipo='otro',
            estado=estado,
            formalidad=formalidad,
            resultado_decision=evaluar_prenda(estado, formalidad, formalidad_ocasion),
        )
        creados += 1
    print(f'{creados} registros importados.')


if __name__ == '__main__':
    main()
