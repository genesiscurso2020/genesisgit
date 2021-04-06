from django.db import models
from proyectos.models import Proyecto

# Create your models here.

class Aplicacion(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    textoenmenu = models.CharField(max_length=30,blank=True,default='')
    imagenmenu = models.ImageField(upload_to='proyectos',blank=True,null=True)
    tooltip = models.CharField(max_length=30,blank=True,default='')
    ordengeneracion = models.SmallIntegerField(default=1) 

    #seguridad
    homelogin = models.BooleanField(default=False)
    homestaff = models.BooleanField(default=False)
        
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre