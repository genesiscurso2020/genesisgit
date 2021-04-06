from django.db import models
from proyectos.models import Proyecto
from django.contrib.auth.models import User
from aplicaciones.models import Aplicacion 

class Personaliza(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
	# aplicacion = models.ForeignKey(Aplicacion, on_delete=models.CASCADE)
	aplicacion = models.CharField(max_length=30)
	archivo = models.CharField(max_length=20)
	tag = models.CharField(max_length=30)
	codigo = models.TextField(default='')
	modificatags = models.BooleanField(default=False)

	def __str__(self):
		return self.archivo
		
class AplicacionPorProyecto(models.Model):
	proyectoid = models.IntegerField()
	aplicacionid = models.IntegerField()
