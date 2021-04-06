from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):
	usuario = models.ForeignKey(User,on_delete=models.CASCADE)
	motivo = models.CharField(max_length=1)
	created = models.DateTimeField(auto_now_add=True)
	texto = RichTextField()
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.texto

class Respuesta(models.Model):
	usuario = models.ForeignKey(User,on_delete=models.CASCADE)
	review = models.ForeignKey(Review,on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	texto = RichTextField()

	def __str__(self):
		return self.texto		