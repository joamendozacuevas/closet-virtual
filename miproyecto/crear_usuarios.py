"""Crea roles y usuarios iniciales con contraseñas recibidas por entorno."""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miproyecto.settings')

import django

django.setup()

from django.contrib.auth.models import Group, User


USUARIOS = {
    'admin': ('ADMIN_PASSWORD', 'admin'),
    'normal': ('NORMAL_PASSWORD', 'normal'),
    'viewer': ('VIEWER_PASSWORD', 'viewer'),
}


def main():
    grupos = {nombre: Group.objects.get_or_create(name=nombre)[0] for nombre in USUARIOS}
    for username, (variable_password, grupo) in USUARIOS.items():
        password = os.environ.get(variable_password)
        if not password:
            print(f'Omitido {username}: falta la variable {variable_password}.')
            continue
        usuario, creado = User.objects.get_or_create(username=username)
        usuario.set_password(password)
        usuario.is_staff = username == 'admin'
        usuario.is_superuser = username == 'admin'
        usuario.save()
        usuario.groups.set([grupos[grupo]])
        print(f"Usuario {username} {'creado' if creado else 'actualizado'}.")


if __name__ == '__main__':
    main()
