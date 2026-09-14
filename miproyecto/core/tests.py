from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Registro


class RegistroTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin-prueba', password='segura123')
        self.admin.groups.add(Group.objects.create(name='admin'))
        self.normal = User.objects.create_user('normal-prueba', password='segura123')
        self.normal.groups.add(Group.objects.create(name='normal'))

    def test_soft_delete_conserva_el_registro(self):
        registro = Registro.objects.create(
            nombre='Prueba', cantidad=2, estado='al dia', resultado='Aceptado'
        )
        registro.soft_delete()
        registro.refresh_from_db()
        self.assertTrue(registro.eliminado)
        self.assertIsNotNone(registro.fecha_eliminacion)

    def test_lista_no_muestra_eliminados(self):
        Registro.objects.create(nombre='Activo', cantidad=1, estado='al dia', resultado='OK')
        eliminado = Registro.objects.create(nombre='Oculto', cantidad=1, estado='moroso', resultado='OK')
        eliminado.soft_delete()
        self.client.force_login(self.normal)
        respuesta = self.client.get(reverse('lista'))
        self.assertContains(respuesta, 'Activo')
        self.assertNotContains(respuesta, 'Oculto')

    def test_normal_no_puede_editar(self):
        registro = Registro.objects.create(nombre='Prueba', cantidad=1, estado='al dia', resultado='OK')
        self.client.force_login(self.normal)
        respuesta = self.client.get(reverse('editar', args=[registro.pk]))
        self.assertEqual(respuesta.status_code, 403)

# Create your tests here.
