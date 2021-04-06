from django.db import models
from ckeditor.fields import RichTextField
from aplicaciones.models import Aplicacion
from proyectos.models import Proyecto

# Create your models here.

class Modelo(models.Model):
    # DATOS GENERALES
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(default='')
    padre = models.CharField(max_length=30,default='nada')
    nombreself = models.CharField(max_length=100, default='')
    nombreborrar = models.CharField(max_length=100,default='')
    aplicacion = models.ForeignKey(Aplicacion, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    textoopcionmenu = models.CharField(max_length=30, blank=True,default='')
    modeloenmenu = models.BooleanField(default=True)    
    sinbasedatos = models.BooleanField(default=False)   
    imagenmenu = models.ImageField(upload_to='proyectos',blank=True,null=True)
    tooltip = models.CharField(max_length=30,blank=True,default='')
    ordengeneracion = models.SmallIntegerField(default=1) 
    ultimoregistro = models.CharField(max_length=1,blank=True,default='p')

    # LISTA
    # Titulo
    titulolista = models.CharField(max_length=30,blank=True,default='Lista de registros')
    fonttitulolista = models.CharField(max_length=100,default='Roboto,18,700')
    colorfondotitulolista = models.CharField(max_length=20,default='transparent')
    colortitulolista = models.CharField(max_length=20,default='#1a1a1a')
    altotitulolista = models.SmallIntegerField(default=40)  
    mayusculastitulolista = models.BooleanField(default=False)  
    justificacionverticaltitulolista = models.CharField(max_length=1,default='c')
    justificacionhorizontaltitulolista = models.CharField(max_length=1,default='i')

    # Comentario
    fontcomentariolista = models.CharField(max_length=100,default='Open+Sans,10,normal')
    comentariolista = models.CharField(max_length=200,default='',blank=True)
    colorfondocomentariolista = models.CharField(max_length=20,default='transparent')
    colorcomentariolista = models.CharField(max_length=20,default='#3a3a3a')

    # Columnas
    mayusculascolumnas = models.BooleanField(default=False) 
    altocolumnas = models.SmallIntegerField(default=30) 
    colorfondocolumnaslista = models.CharField(max_length=20,default='#eeeeee')
    colorcolumnaslista = models.CharField(max_length=20,default='#2a2a2a')
    fontcolumnaslista = models.CharField(max_length=100,default='Roboto,10,700')
    columnaslistaconborde = models.BooleanField(default=False)  

    # Datos
    fonttextolista = models.CharField(max_length=100,default='Arial,10,normal')
    colorfondotextolista = models.CharField(max_length=20,default='transparent')
    colortextolista = models.CharField(max_length=20,default='#2a2a2a')
    buscadorlista = models.BooleanField(default=False)  

    # Editar Borrar
    fonteditarborrar = models.CharField(max_length=100,default='Arial,10,normal')
    coloreditarborrar = models.CharField(max_length=20,default='blue')
    textoeditarborrar = models.CharField(max_length=30,default='Editar,Borrar')

    # Nuevo modelo
    fontlinknuevomodelo = models.CharField(max_length=100,default='Arial,12,700')
    colorlinknuevomodelo = models.CharField(max_length=20,default='#ffeeaa')
    colorbotonlinknuevomodelo = models.CharField(max_length=20,default='primary')
    textolinknuevomodelo = models.CharField(max_length=30,default='Nuevo registro')
    linknuevomodelo = models.BooleanField(default=True) 

    # reporte
    reportsize = models.CharField(max_length=20,default='L')
    reportorientation = models.CharField(max_length=20,default='P')
    titulox = models.DecimalField(decimal_places=2, default=10.5, max_digits=5)    
    fechax = models.DecimalField(decimal_places=2, default=10.5, max_digits=5)    
    lineaix = models.DecimalField(decimal_places=2, default=1, max_digits=5)    
    lineafx = models.DecimalField(decimal_places=2, default=20.50, max_digits=5)    
    grosorlinea = models.DecimalField(decimal_places=2, default=0.3, max_digits=5)    
    datoinicialx = models.DecimalField(decimal_places=2, default=1.5, max_digits=5)    
    identacionautomatica = models.BooleanField(default=True) 

    # INSERTA
    # titulo
    tituloinserta = models.CharField(max_length=30,default='Nuevo Modelo')
    fonttituloinserta = models.CharField(max_length=100,default='Roboto,18,700')
    colortituloinserta = models.CharField(max_length=20,default='#1a1a1a')
    colorfondotituloinserta = models.CharField(max_length=20,default='transparent')
    colorfondofilatituloinserta = models.CharField(max_length=20,default='transparent')
    altofilatituloinserta = models.SmallIntegerField(default=40)    
    justificacionverticaltituloinserta = models.CharField(max_length=1,default='c')
    justificacionhorizontaltituloinserta = models.CharField(max_length=1,default='i')

    # Comentario inserta
    colorfondocomentarioinserta = models.CharField(max_length=20,default='transparent')
    colorcomentarioinserta = models.CharField(max_length=20,default='#3a3a3a')
    fontcomentarioinserta = models.CharField(max_length=100,default='Open+Sans,10,normal')
    comentarioinserta = models.CharField(max_length=200,default='',blank=True)

    # Diagrama
    numerocolumnasizquierdainserta = models.SmallIntegerField(default=1)    
    numerocolumnasmodeloinserta = models.SmallIntegerField(default=10)  
    numerocolumnasderechainserta = models.SmallIntegerField(default=1)  

    # UPDATE
    # titulo
    tituloupdate = models.CharField(max_length=30,default='Modelo a editar: ')
    fonttituloupdate = models.CharField(max_length=100,default='Roboto,18,700')
    colortituloupdate = models.CharField(max_length=20,default='#1a1a1a')
    colorfondotituloupdate = models.CharField(max_length=20,default='transparent')
    colorfondofilatituloupdate = models.CharField(max_length=20,default='transparent')
    altofilatituloupdate = models.SmallIntegerField(default=40) 
    justificacionverticaltituloupdate = models.CharField(max_length=1,default='c')
    justificacionhorizontaltituloupdate = models.CharField(max_length=1,default='i')
    
    # Comentario update
    comentarioupdate = models.CharField(max_length=200,default='',blank=True)
    colorfondocomentarioupdate = models.CharField(max_length=20,default='transparent')
    fontcomentarioupdate = models.CharField(max_length=100,default='Open+Sans,10,normal')
    colorcomentarioupdate = models.CharField(max_length=20,default='#3a3a3a')

    # Diagrama
    numerocolumnasizquierdaupdate = models.SmallIntegerField(default=1)
    numerocolumnasderechaupdate = models.SmallIntegerField(default=1)
    numerocolumnasmodeloupdate = models.SmallIntegerField(default=10)

    # Labels
    fontlabelmodelo = models.CharField(max_length=100,default='Arial,10,bold')
    colorlabelmodelo = models.CharField(max_length=20,default='#010203')
    controlesautomaticos = models.BooleanField(default=False)   

    # BORRAR
    # titulo
    tituloborra = models.CharField(max_length=30,blank=True,default='Borrar el modelo')
    fonttituloborra = models.CharField(max_length=100,default='Roboto,18,700')
    colortituloborra = models.CharField(max_length=20,default='#1a1a1a')
    colorfondotituloborra = models.CharField(max_length=20,default='transparent')
    colorfondofilatituloborra = models.CharField(max_length=20,default='transparent')
    altofilatituloborra = models.SmallIntegerField(default=40)  
    justificacionverticaltituloborra = models.CharField(max_length=1,default='c')
    justificacionhorizontaltituloborra = models.CharField(max_length=1,default='i')

    # Comentario borra
    colorfondocomentarioborra = models.CharField(max_length=20,default='transparent')
    colorcomentarioborra = models.CharField(max_length=20,default='#3a3a3a')
    fontcomentarioborra = models.CharField(max_length=100,default='Open+Sans,10,normal')
    comentarioborra = models.CharField(max_length=200,default='',blank=True)

    # Texto borra
    colorfondotextoborra = models.CharField(max_length=20,default='#eaebec')
    colortextoborra = models.CharField(max_length=20,default='#1a1a1a')
    fonttextoborra = models.CharField(max_length=100,default='Arial,10,normal')
    textoborra = models.CharField(max_length=200,default='Borrar el modelo:',blank=True)

    # Boton borra
    textobotonborra = models.CharField(max_length=30,blank=True,default='Borrar')

    # Diagrama
    numerocolumnasizquierdaborra = models.SmallIntegerField(default=1)
    numerocolumnasderechaborra = models.SmallIntegerField(default=1)
    numerocolumnasmodeloborra = models.SmallIntegerField(default=10)

    # HIJOS
    hijoscontiguos = models.BooleanField(default=False) 
    numerocolumnashijosupdate = models.SmallIntegerField(default=5)

    # SEGURIDAD
    listastaff = models.BooleanField(default=False) 
    listalogin = models.BooleanField(default=False) 
    crearstaff = models.BooleanField(default=False) 
    crearlogin = models.BooleanField(default=False) 
    editarstaff = models.BooleanField(default=False)    
    editarlogin = models.BooleanField(default=False)    
    borrarstaff = models.BooleanField(default=False)    
    borrarlogin = models.BooleanField(default=False)    

    # Columnas de labels y controles
    numerocolumnaslabels = models.SmallIntegerField(default=5)
    numerocolumnascontroles = models.SmallIntegerField(default=7)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    def __str__(self):
        return self.nombre