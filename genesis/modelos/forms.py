from django import forms
from .models import Modelo
from aplicaciones.models import Aplicacion
from proyectos.models import Proyecto

MENU_COLOR_CHOICES = (
   ('primary', 'Primary'),
   ('secondary', 'Secondary'),
   ('success', 'Success'),
   ('danger', 'Danger'),
   ('warning', 'Warning'),
   ('info', 'Info'),
   ('dark', 'Dark'),
   ('light', 'Light'),
   ('white', 'White'),
   ('transparent', 'Transparent'),
   )

JUSTIFICACION_CHOICES = (
   ('i', 'Izquierda'),
   ('d', 'Derecha'),
   ('c', 'Centro'),
    )

JUSTIFICACION_V_CHOICES = (
   ('s', 'Superior'),
   ('c', 'Centro'),
   ('i', 'Inferior'),
    )

MENU_REPORT_SIZE = (
   ('L', 'Letter'),
   ('A', 'A4'),
    )

MENU_ORIENTATION = (
   ('L', 'Landscape'),
   ('P', 'Portrait'),
    )

lista = []

class ModeloForm(forms.ModelForm):

    class Meta:
        model = Modelo
        # fields='__all__'
        fields = ('nombre', 
            'descripcion',
            'aplicacion',
            'padre',
            'nombreself',
            'nombreborrar',
            'textoopcionmenu',
            'titulolista',
            'fonttitulolista',
            'colorfondotitulolista',
            'colortitulolista',
            'altotitulolista',                        
            'mayusculastitulolista',
            'justificacionverticaltitulolista',
            'justificacionhorizontaltitulolista',
            'fontcomentariolista',
            'comentariolista',
            'colorfondocomentariolista',
            'colorcomentariolista',
            'mayusculascolumnas',
            'altocolumnas',
            'colorfondocolumnaslista',
            'colorcolumnaslista',
            'fontcolumnaslista',
            'columnaslistaconborde',
            'fonttextolista',
            'colorfondotextolista',
            'colortextolista',
            'fonteditarborrar',
            'coloreditarborrar',
            'textoeditarborrar',
            'fontlinknuevomodelo',
            'colorlinknuevomodelo',
            'colorbotonlinknuevomodelo',
            'textolinknuevomodelo',
            'linknuevomodelo',
            'tituloinserta',
            'fonttituloinserta',
            'colortituloinserta',
            'colorfondotituloinserta',
            'colorfondofilatituloinserta',
            'altofilatituloinserta',
            'justificacionverticaltituloinserta',
            'justificacionhorizontaltituloinserta',
            'colorfondocomentarioinserta',
            'colorcomentarioinserta',
            'fontcomentarioinserta',
            'comentarioinserta',
            'numerocolumnasizquierdainserta',
            'numerocolumnasmodeloinserta',
            'numerocolumnasderechainserta',
            'tituloupdate',
            'fonttituloupdate',
            'colortituloupdate',
            'colorfondotituloupdate',
            'colorfondofilatituloupdate',
            'altofilatituloupdate',
            'justificacionverticaltituloupdate',
            'justificacionhorizontaltituloupdate',
            'comentarioupdate',
            'colorfondocomentarioupdate',
            'fontcomentarioupdate',
            'colorcomentarioupdate',
            'numerocolumnasizquierdaupdate',
            'numerocolumnasderechaupdate',
            'numerocolumnasmodeloupdate',
            'fontlabelmodelo',
            'colorlabelmodelo',
            'controlesautomaticos',
            'tituloborra',
            'fonttituloborra',
            'colortituloborra',
            'colorfondotituloborra',
            'colorfondofilatituloborra',
            'altofilatituloborra',
            'justificacionverticaltituloborra',
            'justificacionhorizontaltituloborra',
            'colorfondocomentarioborra',
            'colorcomentarioborra',
            'fontcomentarioborra',
            'comentarioborra',
            'colorfondotextoborra',
            'colortextoborra',
            'fonttextoborra',
            'textoborra',
            'textobotonborra',
            'numerocolumnasizquierdaborra',
            'numerocolumnasderechaborra',
            'numerocolumnasmodeloborra',
            'hijoscontiguos',
            'numerocolumnashijosupdate',
            'listastaff',
            'listalogin',
            'crearstaff',
            'crearlogin',
            'editarstaff',
            'editarlogin',
            'borrarstaff',
            'borrarlogin',
            'numerocolumnaslabels',
            'numerocolumnascontroles',
            'modeloenmenu',
            'sinbasedatos',
            'imagenmenu',
            'tooltip',
            'ordengeneracion',
            'buscadorlista',
            'reportsize',
            'reportorientation',
            'titulox',
            'fechax',
            'lineaix',
            'lineafx',
            'grosorlinea',
            'datoinicialx',  
            'identacionautomatica'           
            )
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'descripcion': forms.Textarea(attrs={ 'class':'form-control font_control'}),
            'aplicacion': forms.Select(attrs={ 'class':'form-control font_control'}),
            # 'padre': forms.Select(attrs={ 'class':'form-control font_control'}),
            'nombreself': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'nombreborrar': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'textoopcionmenu': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'titulolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fonttitulolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondotitulolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colortitulolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'altotitulolista': forms.NumberInput(attrs={ 'class':'form-control font_control'}),                        
            'mayusculastitulolista': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'justificacionverticaltitulolista': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_V_CHOICES),
            'justificacionhorizontaltitulolista': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_CHOICES),
            'fontcomentariolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'comentariolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondocomentariolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorcomentariolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'mayusculascolumnas': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'altocolumnas': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'colorfondocolumnaslista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorcolumnaslista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fontcolumnaslista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'columnaslistaconborde': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'fonttextolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondotextolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colortextolista': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fonteditarborrar': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'coloreditarborrar': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'textoeditarborrar': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fontlinknuevomodelo': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorlinknuevomodelo': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorbotonlinknuevomodelo': forms.Select(attrs={ 'class':'form-control font_control'},choices=MENU_COLOR_CHOICES),
            'textolinknuevomodelo': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'linknuevomodelo': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'tituloinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fonttituloinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colortituloinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondotituloinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondofilatituloinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'altofilatituloinserta': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'justificacionverticaltituloinserta': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_V_CHOICES),
            'justificacionhorizontaltituloinserta': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_CHOICES),
            'colorfondocomentarioinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorcomentarioinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fontcomentarioinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'comentarioinserta': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasizquierdainserta': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasmodeloinserta': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasderechainserta': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'tituloupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fonttituloupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colortituloupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondotituloupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondofilatituloupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'altofilatituloupdate': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'justificacionverticaltituloupdate': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_V_CHOICES),
            'justificacionhorizontaltituloupdate': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_CHOICES),
            'comentarioupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondocomentarioupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fontcomentarioupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorcomentarioupdate': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasizquierdaupdate': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasderechaupdate': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasmodeloupdate': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'fontlabelmodelo': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorlabelmodelo': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'controlesautomaticos': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'tituloborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fonttituloborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colortituloborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondotituloborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondofilatituloborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'altofilatituloborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'justificacionverticaltituloborra': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_CHOICES),
            'justificacionhorizontaltituloborra': forms.Select(attrs={ 'class':'form-control font_control'},choices=JUSTIFICACION_CHOICES),
            'colorfondocomentarioborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorcomentarioborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fontcomentarioborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'comentarioborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colorfondotextoborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'colortextoborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'fonttextoborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'textoborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'textobotonborra': forms.TextInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasizquierdaborra': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasderechaborra': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnasmodeloborra': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'hijoscontiguos': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnashijosupdate': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'listastaff': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'listalogin': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'crearstaff': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'crearlogin': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'editarstaff': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'editarlogin': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'borrarstaff': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'borrarlogin': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnaslabels': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'numerocolumnascontroles': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'modeloenmenu': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'sinbasedatos': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'imagenmenu': forms.ClearableFileInput(attrs={'class':'form-control'}),            
            'tooltip': forms.TextInput(attrs={'class':'form-control font_control'}),
            'ordengeneracion': forms.NumberInput(attrs={ 'class':'form-control font_control'}),
            'buscadorlista': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            'reportsize': forms.Select(attrs={ 'class':'form-control font_control'},choices=MENU_REPORT_SIZE),
            'reportorientation': forms.Select(attrs={ 'class':'form-control font_control'},choices=MENU_ORIENTATION),
            'titulox': forms.TextInput(attrs={'class':'form-control font_control'}),
            'fechax': forms.TextInput(attrs={'class':'form-control font_control'}),
            'lineaix': forms.TextInput(attrs={'class':'form-control font_control'}),
            'lineafx': forms.TextInput(attrs={'class':'form-control font_control'}),
            'grosorlinea': forms.TextInput(attrs={'class':'form-control font_control'}),
            'datoinicialx': forms.TextInput(attrs={'class':'form-control font_control'}),
            'identacionautomatica': forms.CheckboxInput(attrs={ 'class':'form-control font_control'}),
            # 'colorbotonlinknuevomodelolistahijos': forms.Select(attrs={'class':'form-control font_control'},choices=MENU_COLOR_CHOICES),
        }
        labels = {
            'nombre':'', 'descripcion':'', 'aplicacion':'Aplicacion','nombreself':'','nombreborrar':'','colorbotonlinknuevomodelo':'Color boton nuevo modelo',
        }

    def __init__(self, *args, **kwargs):
        try:
            self.proyect = kwargs.pop('proyect', None)
            super(ModeloForm, self).__init__(*args, **kwargs)
            proyecto = Proyecto.objects.get(id=self.proyect)
            self.fields['aplicacion'].queryset  = Aplicacion.objects.filter(proyecto=proyecto)
        except:
            pass

    # def clean_nombre(self):
    #     print('Proyecto form ',self.proyecto_id)

    def clean(self):
        # # self.proyecto_id
        # print('Proyecto form ',self.proyect)
        nombre = self.cleaned_data['nombre']
        if ' ' in nombre:
            raise forms.ValidationError('El nombre no debe tener espacios')

class ModeloFormUpdate(forms.ModelForm):

    class Meta:
        model = Modelo
        # fields='__all__'
        fields = ('nombre', 'descripcion','aplicacion','nombreself','padre','nombreborrar','colorbotonlinknuevomodelo',)
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class':'form-control font_control','placeholder': 'Nombre del Modelo'}),
            'nombreself': forms.TextInput(attrs={ 'class':'form-control font_control','placeholder': 'Estructura de retorno del modelo'}),
            'nombreborrar': forms.TextInput(attrs={ 'class':'form-control font_control','placeholder': 'Propiedad de referencia de borrado'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control font_control', 'placeholder': 'Descripcion del Modelo'}),
            'padre' : forms.TextInput(attrs={ 'class':'form-control font_control','placeholder': 'Nombre del modelo padre'}),
            'aplicacion': forms.Select(attrs={'class':'form-control font_control'}),
            'colorbotonlinknuevomodelo': forms.Select(attrs={'class':'form-control font_control'},choices=MENU_COLOR_CHOICES),
        }
        labels = {
            'nombre':'', 'descripcion':'', 'aplicacion':'Aplicacion','nombreself':'','nombreborrar':'','colorbotonlinknuevomodelo':'Color boton nuevo modelo', 
        }

    # def __init__(self, *args, **kwargs):
    #     self.proyect = kwargs.pop('proyect', None)
    #     print('self proyecto init ', self.proyect)
    #     super(ModeloForm, self).__init__(*args, **kwargs)

    # def clean_nombre(self):
    #     print('Proyecto form ',self.proyecto_id)

    def clean(self):
        # # self.proyecto_id
        # print('Proyecto form ',self.proyect)
        nombre = self.cleaned_data['nombre']
        if ' ' in nombre:
            raise forms.ValidationError('El nombre no debe tener espacios')

                