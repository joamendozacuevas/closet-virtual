from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Registro

# La entrega ES1 disponible conserva evaluar_prenda con tres argumentos. Esta
# capa reutiliza esa función sin modificarla mientras EVA2 entrega decidir.
try:
    from solucion import decidir
except ImportError:
    from solucion import evaluar_prenda as _decidir_es1

    def decidir(cantidad, estado):
        return _decidir_es1(estado, cantidad, cantidad)


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
    estado = request.POST.get('estado', '').strip()
    try:
        cantidad = int(request.POST.get('cantidad', ''))
    except (TypeError, ValueError):
        return None
    if not nombre or estado not in Registro.Estado.values:
        return None
    return nombre, cantidad, estado


def vista_login(request):
    if request.user.is_authenticated:
        return redirect('lista')
    if request.method == 'POST':
        usuario = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if usuario is not None:
            login(request, usuario)
            return redirect(request.POST.get('next') or 'lista')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')


@require_POST
def vista_logout(request):
    logout(request)
    return redirect('login')


@login_required
def lista(request):
    return render(request, 'lista.html', {
        'registros': Registro.objects.filter(eliminado=False),
        'puede_crear': tiene_rol(request.user, ('admin', 'normal')),
        'puede_administrar': tiene_rol(request.user, ('admin',)),
    })


@requiere_rol('admin', 'normal')
def crear(request):
    if request.method == 'POST':
        datos = _datos_validos(request)
        if datos is None:
            messages.error(request, 'Ingresa un nombre, un estado válido y una cantidad entera.')
        else:
            nombre, cantidad, estado = datos
            Registro.objects.create(
                nombre=nombre,
                cantidad=cantidad,
                estado=estado,
                resultado=decidir(cantidad, estado),
            )
            messages.success(request, 'Registro creado correctamente.')
            return redirect('lista')
    return render(request, 'formulario.html', {'titulo': 'Crear registro'})


@requiere_rol('admin')
def editar(request, registro_id):
    registro = get_object_or_404(Registro, pk=registro_id, eliminado=False)
    if request.method == 'POST':
        datos = _datos_validos(request)
        if datos is None:
            messages.error(request, 'Ingresa un nombre, un estado válido y una cantidad entera.')
        else:
            registro.nombre, registro.cantidad, registro.estado = datos
            registro.resultado = decidir(registro.cantidad, registro.estado)
            registro.save()
            messages.success(request, 'Registro actualizado correctamente.')
            return redirect('lista')
    return render(request, 'formulario.html', {
        'titulo': 'Editar registro', 'registro': registro,
    })


@requiere_rol('admin')
@require_POST
def eliminar(request, registro_id):
    registro = get_object_or_404(Registro, pk=registro_id, eliminado=False)
    registro.soft_delete()
    messages.success(request, 'Registro eliminado correctamente.')
    return redirect('lista')
