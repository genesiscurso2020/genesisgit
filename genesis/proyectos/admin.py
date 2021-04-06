from django.contrib import admin
from .models import Proyecto,Crear,LicenciaUso, ProyectoTexto

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(ProyectoTexto)
admin.site.register(Crear)
admin.site.register(LicenciaUso)
