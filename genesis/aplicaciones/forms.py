from django import forms

from .models import Aplicacion

class AplicacionForm(forms.ModelForm):
	class Meta:
		model = Aplicacion
		fields = ('nombre', 'descripcion', 'textoenmenu', 'homestaff','homelogin','imagenmenu','tooltip','ordengeneracion')
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control font_control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control font_control'}),
			'textoenmenu': forms.TextInput(attrs={'class':'form-control font_control'}),
			'imagenmenu': forms.ClearableFileInput(attrs={'class':'form-control'}),
			'tooltip': forms.TextInput(attrs={'class':'form-control font_control'}),
            'ordengeneracion': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
		}
		labels = {
			'nombre':'', 'descripcion':'','homestaff':'El usuario debe ser miembro de la administracion','homelogin':'La aplicacion requiere identificacion',
		}

	'''
		Se debe controlar que el nombre de la aplicacion no tenga
		espacios. 
	'''
	def clean(self):
		nombre = self.cleaned_data['nombre']
		if ' ' in nombre:
		    raise forms.ValidationError('El nombre no debe tener espacios')
