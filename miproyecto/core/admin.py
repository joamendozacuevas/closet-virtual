from django.contrib import admin

from .models import Registro


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'cantidad', 'resultado', 'fecha')
    list_filter = ('estado', 'eliminado')
    search_fields = ('nombre',)
    readonly_fields = ('fecha_eliminacion',)
