import uuid

from django.db import models


class Prenda(models.Model):
    ESTADOS_LIMPIEZA = [
        ('limpio', 'Limpio'),
        ('sucio', 'Sucio'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=120)
    color = models.CharField(max_length=80)
    estado_limpieza = models.CharField(max_length=10, choices=ESTADOS_LIMPIEZA)
    formalidad_prenda = models.PositiveSmallIntegerField()
    formalidad_ocasion = models.PositiveSmallIntegerField()
    resultado = models.CharField(max_length=160, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre
