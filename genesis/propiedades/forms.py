from django import forms
from .models import Propiedad

TIPO_CHOICES = (
        # ('a','Lista'),
        ('b','Boolean'),
        ('d','Decimal'),
        ('e','Hora'),
        ('f','Foranea'),
        ('h','RichText'),
        ('i','Entero'),
        ('l','Entero largo'),
        ('m','Entero pequeno'),
        ('n','Fecha'),
        ('p','Imagen'),
        ('r','Radio Button'),
        ('s','String'),
        ('t','Hora y Fecha'),
        ('u','Usuario'),
        ('x','Text Field'),
    )

JUSTIFICACION_CHOICES = (
   ('i', 'Izquierda'),
   ('d', 'Derecha'),
   ('c', 'Centro'),
    )

class PropiedadForm(forms.ModelForm):

    class Meta:
        model = Propiedad
        # fields='__all__'
        fields = ('nombre', 'descripcion','tipo','foranea', 'textobotones',
                  'enlista','enmobile','largostring','textoplaceholder',
                  'etiqueta', 'valorinicial','formatofecha','justificaciontextocolumna','numerocolumnas',
                  'textocolumna','etiquetaarriba','mandatoria','noestaenformulario','participabusquedalista',
                  'enreporte','anchoenreporte','totaliza')
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control font_control'}),
            'tipo': forms.Select(attrs={'class':'form-control font_control'},choices=TIPO_CHOICES),        
            'foranea': forms.TextInput(attrs={'class':'form-control font_control'}),
            'textobotones': forms.TextInput(attrs={'class':'form-control font_control'}),
            'textocolumna': forms.TextInput(attrs={'class':'form-control font_control'}),
            'enlista' : forms.CheckboxInput(attrs={'disabled':False}),
            'enmobile' : forms.CheckboxInput(attrs={'disabled':False}),
            'etiquetaarriba' : forms.CheckboxInput(attrs={'disabled':False}),
            'valorinicial': forms.TextInput(attrs={'class':'form-control font_control'}),
            'largostring': forms.NumberInput(attrs={'class':'form-control font_control'}),
            'numerocolumnas': forms.NumberInput(attrs={'class':'form-control font_control'}),
            'textoplaceholder': forms.TextInput(attrs={'class':'form-control font_control'}),
            'etiqueta': forms.TextInput(attrs={'class':'form-control font_control'}),
            'textocolumna': forms.TextInput(attrs={'class':'form-control font_control'}),
            'formatofecha': forms.TextInput(attrs={'class':'form-control font_control'}),
            'justificaciontextocolumna': forms.Select(attrs={'class':'form-control font_control'},choices=JUSTIFICACION_CHOICES),
            'mandatoria' : forms.CheckboxInput(attrs={'disabled':False}),
            'noestaenformulario' : forms.CheckboxInput(attrs={'disabled':False}),
            'participabusquedalista' : forms.CheckboxInput(attrs={'disabled':False}),
            'enreporte' : forms.CheckboxInput(attrs={'disabled':False}),
            'anchoenreporte': forms.NumberInput(attrs={'class':'form-control font_control'}),
            'totaliza' : forms.CheckboxInput(attrs={'disabled':False}),
        }
        labels = {
            'foranea':'Modelo foraneo',
            'nombre':'', 
            'descripcion':'', 
            'tipo':'Tipo de Propiedad', 
            'enlista':'La propiedad aparece en las listas',
            'enmobile':'La propiedad aparece en dispositivos mobiles',
            'textobotones':'',
            'valorinicial':'',
            'textoplaceholder':'',
            'etiqueta':'',
            'formatofecha':'',
            'largostring':'Longitud del string',
        }

    def clean(self):
        nombre = self.cleaned_data['nombre']
        if ' ' in nombre:
            raise forms.ValidationError('El nombre no debe tener espacios')
