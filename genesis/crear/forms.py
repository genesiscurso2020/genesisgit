from django import forms

from .models import ReporteNuevo

class ReporteForm(forms.ModelForm):
	class Meta:
		model = ReporteNuevo
		fields = ('primeralinea',
    			  'maxlineas',
    			  'anchologo',
    			  'altologo',
    			  'posxlogo',
    			  'posylogo',
    			  'posxnombre',
    			  'posynombre',
    			  'iniciolineax',
    			  'finallineax',
    			  'iniciolineay',
    			  'grosorlinea',
    			  'piex',
    			  'piey',
    			  'lineapiex',
    			  'lineapiey',)
		widgets = {
   			'primeralinea': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'maxlineas':forms.NumberInput(attrs={'class':'form-control'}),
    		'anchologo': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'altologo': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'posxlogo': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'posylogo': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'posxnombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'posynombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'iniciolineax': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'finallineax': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'iniciolineay': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'grosorlinea': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'piex': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'piey': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'lineapiex': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
    		'lineapiey': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
		}

