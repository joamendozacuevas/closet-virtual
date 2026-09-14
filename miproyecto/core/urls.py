from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:registro_id>/', views.editar, name='editar'),
    path('eliminar/<int:registro_id>/', views.eliminar, name='eliminar'),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
]
