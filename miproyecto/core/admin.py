from django.contrib import admin

from .models import Prenda


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'color', 'estado', 'formalidad', 'resultado_decision')
    list_filter = ('tipo', 'estado', 'formalidad', 'eliminado')
    search_fields = ('nombre', 'color')
    readonly_fields = ('fecha_eliminacion',)
