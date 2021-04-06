from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Genesis(models.Model):
	nombre = models.CharField(max_length=30, default='GENESIS')
	descripcion = models.TextField(default='')
	logo = models.ImageField(upload_to='genesis',blank=True,null=True)
	titulo = models.CharField(max_length=50)
	directorio = models.CharField(max_length=200)
	directoriogenesis = models.CharField(max_length=200,default='')
	directoriotexto = models.CharField(max_length=200,default='')
	directoriozip = models.CharField(max_length=200,default='')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.nombre

class Precio(models.Model):
	titulo = models.CharField(max_length=50, default='')
	descripcion = models.TextField(default='')
	importe = models.CharField(max_length=10, default='')
	paypal = models.TextField(default='')
	
	def __str__(self):
		return self.titulo

		