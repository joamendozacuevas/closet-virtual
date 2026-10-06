from rest_framework import serializers

from .models import Prenda


class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenda
        fields = [
            'id', 'nombre', 'color', 'estado_limpieza',
            'formalidad_prenda', 'formalidad_ocasion', 'resultado',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'resultado', 'fecha_creacion']

    def validate_formalidad_prenda(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Debe estar entre 1 y 10.')
        return value

    def validate_formalidad_ocasion(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Debe estar entre 1 y 10.')
        return value
