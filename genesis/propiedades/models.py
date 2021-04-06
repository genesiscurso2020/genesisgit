from django.db import models
from modelos.models import Modelo
from ckeditor.fields import RichTextField

# Create your models here.

class Propiedad(models.Model):
	nombre = models.CharField(max_length=30)
	descripcion = models.TextField()
	# descripcion = models.TextField()
	tipo = models.CharField(max_length=1, default='s')
	foranea = models.CharField(max_length=30,default='nada')
	textobotones = models.CharField(max_length=100,blank=True)
	modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
	valorinicial = models.CharField(max_length=30,blank=True)
	largostring = models.SmallIntegerField(default=30)
	textoplaceholder = models.CharField(max_length=50,blank=True)
	etiqueta = models.CharField(max_length=100, blank=True)
	mandatoria = models.BooleanField(default=False)
	noestaenformulario = models.BooleanField(default=False)
	participabusquedalista = models.BooleanField(default=False)
	totaliza = models.BooleanField(default=False)

	# Lista de propiedades
	enlista = models.BooleanField(default=False)
	enmobile = models.BooleanField(default=False)
	numerocolumnas = models.SmallIntegerField(default=1)
	textocolumna = models.CharField(max_length=100, blank=True)
	justificaciontextocolumna = models.CharField(max_length=1,default='i')
	formatofecha = models.CharField(max_length=30,default='',blank=True)

	# reporte
	enreporte = models.BooleanField(default=False)
	anchoenreporte = models.SmallIntegerField(default=3)

	# Labels
	etiquetaarriba = models.BooleanField(default=False)
 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	
	def __str__(self):
		return self.nombre
