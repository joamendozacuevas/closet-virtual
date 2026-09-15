from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Prenda


class PrendaTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin-prueba', password='segura123')
        self.admin.groups.add(Group.objects.create(name='admin'))
        self.normal = User.objects.create_user('normal-prueba', password='segura123')
        self.normal.groups.add(Group.objects.create(name='normal'))

    def test_soft_delete_conserva_el_registro(self):
        prenda = Prenda.objects.create(
            nombre='Prueba', color='Azul', tipo='camisa', estado='limpio',
            formalidad=2, formalidad_ocasion=2, resultado_decision='Aceptado'
        )
        prenda.soft_delete()
        prenda.refresh_from_db()
        self.assertTrue(prenda.eliminado)
        self.assertIsNotNone(prenda.fecha_eliminacion)

    def test_lista_no_muestra_eliminados(self):
        Prenda.objects.create(nombre='Activo', color='Negro', tipo='polera', estado='limpio', formalidad=1, formalidad_ocasion=1, resultado_decision='OK')
        eliminado = Prenda.objects.create(nombre='Oculto', color='Rojo', tipo='polera', estado='sucio', formalidad=1, formalidad_ocasion=1, resultado_decision='OK')
        eliminado.soft_delete()
        self.client.force_login(self.normal)
        respuesta = self.client.get(reverse('lista_prendas'))
        self.assertContains(respuesta, 'Activo')
        self.assertNotContains(respuesta, 'Oculto')

    def test_normal_no_puede_editar(self):
        prenda = Prenda.objects.create(nombre='Prueba', color='Azul', tipo='camisa', estado='limpio', formalidad=1, formalidad_ocasion=1, resultado_decision='OK')
        self.client.force_login(self.normal)
        respuesta = self.client.get(reverse('editar_prenda', args=[prenda.pk]))
        self.assertEqual(respuesta.status_code, 403)

# Create your tests here.
