from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Respuesta
from django.core.exceptions import ValidationError
import urllib.request

MOTIVO_CHOICES = (
   ('c', 'Comentario'),
   ('f', 'Calificacion'),
   ('s', 'Sugerencia'),
   ('t', 'Consulta'),
	)

class ReviewForm(forms.ModelForm):

	class Meta:
		model = Review
		fields = ('motivo','texto',)

		widgets = {
			'texto': forms.Textarea(attrs={'class':'form-control'}),
			'motivo': forms.Select(attrs={'class':'form-control'},choices=MOTIVO_CHOICES),
		}
		labels = {
			'motivo':'', 'texto':''
		}

class RespuestaForm(forms.ModelForm):

	class Meta:
		model = Respuesta
		fields = ('texto',)

		widgets = {
			'texto': forms.Textarea(attrs={'class':'form-control'}),
		}
		labels = {
			'texto':''
		}		