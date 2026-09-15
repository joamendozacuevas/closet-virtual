from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from solucion import evaluar_prenda

from .forms import PrendaForm
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
        form = PrendaForm(request.POST)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.resultado_decision = evaluar_prenda(
                prenda.estado, prenda.formalidad, prenda.formalidad_ocasion
            )
            prenda.save()
            messages.success(request, 'Prenda agregada correctamente.')
            return redirect('lista_prendas')
    else:
        form = PrendaForm()
    return render(request, 'formulario.html', {'titulo': 'Agregar prenda', 'form': form})


@requiere_rol('admin')
def editar_prenda(request, prenda_id):
    prenda = get_object_or_404(Prenda, pk=prenda_id, eliminado=False)
    if request.method == 'POST':
        form = PrendaForm(request.POST, instance=prenda)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.resultado_decision = evaluar_prenda(
                prenda.estado, prenda.formalidad, prenda.formalidad_ocasion
            )
            prenda.save()
            messages.success(request, 'Prenda actualizada correctamente.')
            return redirect('lista_prendas')
    else:
        form = PrendaForm(instance=prenda)
    return render(request, 'formulario.html', {
        'titulo': 'Editar prenda', 'form': form,
    })


@requiere_rol('admin')
def eliminar_prenda(request, prenda_id):
    prenda = get_object_or_404(Prenda, pk=prenda_id, eliminado=False)
    if request.method == 'POST':
        prenda.soft_delete()
        messages.success(request, 'Prenda eliminada correctamente.')
        return redirect('lista_prendas')
    return render(request, 'confirmar_eliminar.html', {'prenda': prenda})
