from uuid import UUID

from django.http import Http404
from django.shortcuts import redirect, render

from solucion import evaluar_prenda
from .models import Prenda


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
	return render(request, 'resumen.html', {'registros': Prenda.objects.all()})


def agregar(request):
	if request.method == 'POST':
		prenda = _datos_del_formulario(request)
		Prenda.objects.create(**prenda)
	return redirect('resumen')


def eliminar(request, id):
	try:
		identificador = UUID(str(id))
	except (TypeError, ValueError):
		identificador = None
	if identificador is not None:
		Prenda.objects.filter(pk=identificador).delete()
	return redirect('resumen')


def editar(request, id):
	try:
		identificador = UUID(str(id))
		prenda = Prenda.objects.get(pk=identificador)
	except (Prenda.DoesNotExist, TypeError, ValueError):
		raise Http404('La prenda no existe')

	if request.method == 'POST':
		for campo, valor in _datos_del_formulario(request).items():
			setattr(prenda, campo, valor)
		prenda.save()
		return redirect('resumen')

	return render(request, 'editar.html', {'prenda': prenda})
