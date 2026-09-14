from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from solucion import evaluar_prenda

from .models import Prenda


def tiene_rol(usuario, roles):
    """Indica si un usuario pertenece a alguno de los grupos permitidos."""
    return usuario.is_authenticated and (
        usuario.is_superuser or usuario.groups.filter(name__in=roles).exists()
    )


def requiere_rol(*roles):
    """Protege una vista en el servidor según grupos de Django."""
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not tiene_rol(request.user, roles):
                return HttpResponseForbidden('No tienes permisos para esta acción.')
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador


def _datos_validos(request):
    nombre = request.POST.get('nombre', '').strip()
    color = request.POST.get('color', '').strip()
    tipo = request.POST.get('tipo', '').strip()
    estado = request.POST.get('estado', '').strip()
    try:
        formalidad = int(request.POST.get('formalidad', ''))
        formalidad_ocasion = int(request.POST.get('formalidad_ocasion', ''))
    except (TypeError, ValueError):
        return None
    if (
        not nombre
        or not color
        or tipo not in Prenda.Tipo.values
        or estado not in Prenda.Estado.values
        or not 1 <= formalidad <= 10
        or not 1 <= formalidad_ocasion <= 10
    ):
        return None
    return nombre, color, tipo, estado, formalidad, formalidad_ocasion


def vista_login(request):
    if request.user.is_authenticated:
        return redirect('lista_prendas')
    if request.method == 'POST':
        usuario = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if usuario is not None:
            login(request, usuario)
            return redirect(request.POST.get('next') or 'lista_prendas')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')


@require_POST
def vista_logout(request):
    logout(request)
    return redirect('login')


@login_required
def lista_prendas(request):
    return render(request, 'lista.html', {
        'prendas': Prenda.objects.filter(eliminado=False),
        'puede_crear': tiene_rol(request.user, ('admin', 'normal')),
        'puede_administrar': tiene_rol(request.user, ('admin',)),
    })


@requiere_rol('admin', 'normal')
def agregar_prenda(request):
    if request.method == 'POST':
        datos = _datos_validos(request)
        if datos is None:
            messages.error(request, 'Completa todos los campos y usa formalidades entre 1 y 10.')
        else:
            nombre, color, tipo, estado, formalidad, formalidad_ocasion = datos
            Prenda.objects.create(
                nombre=nombre,
                color=color,
                tipo=tipo,
                estado=estado,
                formalidad=formalidad,
                resultado_decision=evaluar_prenda(estado, formalidad, formalidad_ocasion),
            )
            messages.success(request, 'Prenda agregada correctamente.')
            return redirect('lista_prendas')
    return render(request, 'formulario.html', {'titulo': 'Agregar prenda'})


@requiere_rol('admin')
def editar_prenda(request, prenda_id):
    prenda = get_object_or_404(Prenda, pk=prenda_id, eliminado=False)
    if request.method == 'POST':
        datos = _datos_validos(request)
        if datos is None:
            messages.error(request, 'Completa todos los campos y usa formalidades entre 1 y 10.')
        else:
            nombre, color, tipo, estado, formalidad, formalidad_ocasion = datos
            prenda.nombre = nombre
            prenda.color = color
            prenda.tipo = tipo
            prenda.estado = estado
            prenda.formalidad = formalidad
            prenda.resultado_decision = evaluar_prenda(estado, formalidad, formalidad_ocasion)
            prenda.save()
            messages.success(request, 'Prenda actualizada correctamente.')
            return redirect('lista_prendas')
    return render(request, 'formulario.html', {
        'titulo': 'Editar prenda', 'prenda': prenda,
    })


@requiere_rol('admin')
@require_POST
def eliminar_prenda(request, prenda_id):
    prenda = get_object_or_404(Prenda, pk=prenda_id, eliminado=False)
    prenda.soft_delete()
    messages.success(request, 'Prenda eliminada correctamente.')
    return redirect('lista_prendas')
