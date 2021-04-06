from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
	email = forms.EmailField(required=True, help_text='Campo requerido y debe ser valido, hasta 254 caracteres como maximo')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email):
			raise forms.ValidationError('El email ya existe, ingresa uno nuevo')
		return email

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['nombre','avatar','biografia','recibemails']

		widgets = {
			'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file'}),
			'biografia': forms.Textarea(attrs={'class':'form-control', 'rows': '5', 'placeholder': 'Biografia'}),
			'nombre': forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Nombre completo'}),
		}
		labels = {'nombre':'','biografia':'','recibemails':'Recibir mails',}

class EmailForm(forms.ModelForm):
	email = forms.EmailField(required=True, help_text='Campo requerido y debe ser valido, hasta 254 caracteres como maximo')

	class Meta:
		model = User
		fields =['email']
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		# Verificar si el campo emial ha cambiado
		if 'email' in self.changed_data:
			if User.objects.filter(email=email):
				raise forms.ValidationError('El email ya existe, ingresa uno nuevo')
		return email