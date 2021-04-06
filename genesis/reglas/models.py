from django.db import models
from propiedades.models import Propiedad

# Create your models here.

class Regla(models.Model):
	mensaje = models.TextField()
	codigo = models.TextField()
	propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	
	def __str__(self):
		return self.mensaje