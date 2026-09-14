from django.db import models
from django.utils import timezone


class Registro(models.Model):
    class Estado(models.TextChoices):
        AL_DIA = 'al dia', 'Al día'
        MOROSO = 'moroso', 'Moroso'

    nombre = models.CharField(max_length=150)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=10, choices=Estado.choices)
    resultado = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.nombre} ({self.estado})'

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()
