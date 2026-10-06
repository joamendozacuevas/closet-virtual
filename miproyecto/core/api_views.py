from rest_framework.viewsets import ModelViewSet

from solucion import evaluar_prenda
from .models import Prenda
from .permissions import PrendaPermission
from .serializers import PrendaSerializer


class PrendaViewSet(ModelViewSet):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer
    permission_classes = [PrendaPermission]

    def perform_create(self, serializer):
        datos = serializer.validated_data
        resultado = evaluar_prenda(
            datos['estado_limpieza'],
            datos['formalidad_prenda'],
            datos['formalidad_ocasion'],
        )
        serializer.save(resultado=resultado)

    def perform_update(self, serializer):
        datos = serializer.validated_data
        prenda = serializer.instance
        resultado = evaluar_prenda(
            datos.get('estado_limpieza', prenda.estado_limpieza),
            datos.get('formalidad_prenda', prenda.formalidad_prenda),
            datos.get('formalidad_ocasion', prenda.formalidad_ocasion),
        )
        serializer.save(resultado=resultado)
