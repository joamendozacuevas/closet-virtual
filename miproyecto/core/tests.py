from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Prenda


class PrendaAPITests(TestCase):
    def setUp(self):
        Prenda.objects.all().delete()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='lector', password='clave-segura-123'
        )
        self.staff = user_model.objects.create_user(
            username='staff', password='clave-segura-123', is_staff=True
        )
        self.client = APIClient()
        self.list_url = reverse('prenda-list')
        self.payload = {
            'nombre': 'Camisa',
            'color': 'azul',
            'estado_limpieza': 'limpio',
            'formalidad_prenda': 6,
            'formalidad_ocasion': 7,
        }

    def authenticate(self, user=None):
        self.client.force_authenticate(user=user or self.user)

    def test_api_requiere_autenticacion_y_usa_401(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crear_prenda_calcula_resultado_en_servidor(self):
        self.authenticate()
        payload = {**self.payload, 'resultado': 'Aceptado por el cliente'}

        response = self.client.post(self.list_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['resultado'], 'Aceptado')
        self.assertEqual(Prenda.objects.count(), 1)
        self.assertEqual(response.data['id'], str(Prenda.objects.get().id))
        self.assertIn('fecha_creacion', response.data)
        listado = self.client.get(self.list_url)
        self.assertEqual(listado.status_code, status.HTTP_200_OK)
        self.assertEqual(listado.data['count'], 1)

    def test_rechaza_formalidad_fuera_de_rango(self):
        self.authenticate()

        response = self.client.post(
            self.list_url, {**self.payload, 'formalidad_prenda': 11}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response['Content-Type'].startswith('application/json'))
        self.assertFalse(Prenda.objects.exists())

    def test_resultado_rechaza_diferencia_mayor_a_dos(self):
        self.authenticate()
        response = self.client.post(
            self.list_url,
            {**self.payload, 'formalidad_prenda': 2, 'formalidad_ocasion': 8},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['resultado'],
            'Rechazo 2: Diferencia de formalidad mayor a 2 puntos',
        )

    def test_listado_esta_paginado_a_diez_registros(self):
        self.authenticate()
        for numero in range(11):
            self.client.post(
                self.list_url,
                {**self.payload, 'nombre': f'Prenda {numero}'},
                format='json',
            )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 10)

    def test_edicion_recalcula_resultado(self):
        self.authenticate()
        prenda = Prenda.objects.create(**self.payload, resultado='Aceptado')

        response = self.client.patch(
            reverse('prenda-detail', args=[prenda.id]),
            {'estado_limpieza': 'sucio'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['resultado'], 'Rechazo 1: La prenda está sucia')

    def test_borrado_es_solo_para_staff_y_devuelve_204(self):
        prenda = Prenda.objects.create(**self.payload, resultado='Aceptado')
        detail_url = reverse('prenda-detail', args=[prenda.id])
        self.authenticate()

        forbidden = self.client.delete(detail_url)
        self.assertEqual(forbidden.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Prenda.objects.filter(pk=prenda.id).exists())

        self.authenticate(self.staff)
        deleted = self.client.delete(detail_url)
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Prenda.objects.filter(pk=prenda.id).exists())

    def test_token_docs_y_pantalla_html_siguen_disponibles(self):
        token_response = self.client.post(
            reverse('api-token'),
            {'username': self.user.username, 'password': 'clave-segura-123'},
            format='json',
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', token_response.data)
        self.assertIn('expires_at', token_response.data)
        self.assertEqual(
            token_response.data['expires_in'], settings.API_TOKEN_LIFETIME_SECONDS
        )
        self.assertEqual(token_response['Cache-Control'], 'no-store')
        self.assertEqual(self.client.get('/api/docs/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/schema/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/').status_code, status.HTTP_200_OK)

    def test_solicitar_token_nuevo_rota_el_anterior(self):
        datos = {'username': self.user.username, 'password': 'clave-segura-123'}
        primer_token = self.client.post(reverse('api-token'), datos, format='json')
        segundo_token = self.client.post(reverse('api-token'), datos, format='json')

        self.assertEqual(primer_token.status_code, status.HTTP_200_OK)
        self.assertEqual(segundo_token.status_code, status.HTTP_200_OK)
        self.assertNotEqual(primer_token.data['token'], segundo_token.data['token'])
        self.assertFalse(Token.objects.filter(key=primer_token.data['token']).exists())

    def test_token_vencido_se_rechaza_y_se_elimina(self):
        token = Token.objects.create(user=self.user)
        Token.objects.filter(pk=token.pk).update(
            created=timezone.now() - timedelta(
                seconds=settings.API_TOKEN_LIFETIME_SECONDS + 1
            )
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response['Content-Type'].startswith('application/json'))
        self.assertFalse(Token.objects.filter(pk=token.pk).exists())

    def test_api_solo_negocia_respuestas_json(self):
        self.authenticate()
        response = self.client.get(self.list_url, HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertTrue(response['Content-Type'].startswith('application/json'))

    def test_vista_html_crea_actualiza_y_borra_en_la_misma_base(self):
        response = self.client.post(
            reverse('agregar'), self.payload, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prenda = Prenda.objects.get(nombre='Camisa')
        self.assertEqual(prenda.resultado, 'Aceptado')

        response = self.client.post(
            reverse('editar', args=[prenda.id]),
            {**self.payload, 'estado_limpieza': 'sucio'},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prenda.refresh_from_db()
        self.assertEqual(prenda.resultado, 'Rechazo 1: La prenda está sucia')

        response = self.client.post(reverse('eliminar', args=[prenda.id]), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Prenda.objects.filter(pk=prenda.id).exists())

    def test_vistas_html_manejan_ids_invalidos_sin_error(self):
        response = self.client.get(reverse('editar', args=['id-invalido']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse('eliminar', args=['id-invalido']))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
