import json
import os
import uuid

from django.http import Http404
from django.shortcuts import redirect, render
from solucion import evaluar_prenda


def _leer_datos():
	if os.path.exists('datos.json'):
		with open('datos.json', 'r', encoding='utf-8') as archivo:
			return json.load(archivo)
	return []


def _guardar_datos(registros):
	with open('datos.json', 'w', encoding='utf-8') as archivo:
		json.dump(registros, archivo, ensure_ascii=False, indent=4)


def _datos_del_formulario(request):
	try:
		formalidad_prenda = int(request.POST.get('formalidad_prenda', 0))
	except ValueError:
		formalidad_prenda = 0
	try:
		formalidad_ocasion = int(request.POST.get('formalidad_ocasion', 0))
	except ValueError:
		formalidad_ocasion = 0

	estado_limpieza = request.POST.get('estado_limpieza', '').strip()
	return {
		'nombre': request.POST.get('nombre', '').strip(),
		'color': request.POST.get('color', '').strip(),
		'estado_limpieza': estado_limpieza,
		'formalidad_prenda': formalidad_prenda,
		'formalidad_ocasion': formalidad_ocasion,
		'resultado': evaluar_prenda(
			estado_limpieza, formalidad_prenda, formalidad_ocasion
		),
	}


def resumen(request):
	return render(request, 'resumen.html', {'registros': _leer_datos()})


def agregar(request):
	if request.method == 'POST':
		prenda = _datos_del_formulario(request)
		prenda['id'] = str(uuid.uuid4())
		registros = _leer_datos()
		registros.append(prenda)
		_guardar_datos(registros)
	return redirect('resumen')


def eliminar(request, id):
	registros = _leer_datos()
	registros = [registro for registro in registros if registro.get('id') != id]
	_guardar_datos(registros)
	return redirect('resumen')


def editar(request, id):
	registros = _leer_datos()
	prenda = next(
		(registro for registro in registros if registro.get('id') == id), None
	)
	if prenda is None:
		raise Http404('La prenda no existe')

	if request.method == 'POST':
		prenda.update(_datos_del_formulario(request))
		_guardar_datos(registros)
		return redirect('resumen')

	return render(request, 'editar.html', {'prenda': prenda})
