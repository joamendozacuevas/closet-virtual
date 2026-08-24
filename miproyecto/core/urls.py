from django.urls import path

from .views import agregar, editar, eliminar, resumen

urlpatterns = [
    path('', resumen, name='resumen'),
    path('agregar', agregar, name='agregar'),
    path('eliminar/<str:id>', eliminar, name='eliminar'),
    path('editar/<str:id>', editar, name='editar'),
]