from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Personaliza
from proyectos.models import Proyecto
from personalizacion.models import AplicacionPorProyecto
from aplicaciones.models import Aplicacion
from django.core.exceptions import ValidationError
import urllib.request

class PersonalizaForm(forms.ModelForm):

	class Meta:
		model = Personaliza
		fields = ('codigo',)

		widgets = {
			'codigo': forms.Textarea(attrs={'class':'form-control'}),
		}

