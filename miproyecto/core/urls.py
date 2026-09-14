from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_prendas, name='lista_prendas'),
    path('agregar/', views.agregar_prenda, name='agregar_prenda'),
    path('editar/<int:prenda_id>/', views.editar_prenda, name='editar_prenda'),
    path('eliminar/<int:prenda_id>/', views.eliminar_prenda, name='eliminar_prenda'),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
]
