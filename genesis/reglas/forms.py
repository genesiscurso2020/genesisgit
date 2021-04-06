from django import forms
from reglas.models import Regla

class ReglaForm(forms.ModelForm):
	class Meta:
		model = Regla

		fields = ('mensaje','codigo', )
		
		widgets = {
			'mensaje': forms.Textarea(attrs={ 'class':'form-control font_control'}),
			'codigo': forms.Textarea(attrs={ 'class':'form-control font_control'}),
		}
		labels = {
			'mensaje': '', 'codigo': ''
		}

