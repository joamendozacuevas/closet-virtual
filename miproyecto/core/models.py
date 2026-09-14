from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Prenda(models.Model):
    class Tipo(models.TextChoices):
        CAMISA = 'camisa', 'Camisa'
        PANTALON = 'pantalon', 'Pantalón'
        ZAPATOS = 'zapatos', 'Zapatos'
        POLERA = 'polera', 'Polera'
        CHAQUETA = 'chaqueta', 'Chaqueta'
        OTRO = 'otro', 'Otro'

    class Estado(models.TextChoices):
        LIMPIO = 'limpio', 'Limpio'
        SUCIO = 'sucio', 'Sucio'
        PLANCHADO = 'planchado', 'Planchado'

    nombre = models.CharField(max_length=150)
    color = models.CharField(max_length=80)
    tipo = models.CharField(max_length=15, choices=Tipo.choices)
    estado = models.CharField(max_length=12, choices=Estado.choices)
    formalidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    resultado_decision = models.CharField(max_length=255)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()
