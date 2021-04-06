from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=100)
	avatar = models.ImageField(upload_to='profiles',null=True,blank=True)
	biografia = models.TextField(null=True,blank=True)
	biografia = models.TextField(null=True,blank=True)
	recibemails = models.BooleanField(default=False)