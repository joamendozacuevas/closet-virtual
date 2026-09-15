from django import forms

from .models import Prenda


class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ('nombre', 'color', 'tipo', 'estado', 'formalidad', 'formalidad_ocasion')
        labels = {
            'formalidad_ocasion': 'Formalidad de la ocasión',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'formalidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'formalidad_ocasion': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 10}
            ),
        }
