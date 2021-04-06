from django.db import models

from aplicaciones.models import Aplicacion
from proyectos.models import Proyecto

# Create your models here.

class ErroresCreacion(models.Model):
    proyecto = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50,default='')
    etapa = models.CharField(max_length=50)
    paso = models.TextField(default='')
    descripcion = models.TextField(default='')
    severo = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    def __str__(self):
        return self.etapa

class Reporte(models.Model):
    reportesize = models.CharField(max_length=1,default='l')
    orientacion = models.CharField(max_length=1,default='p')
    logox = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    logoy = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    titulox = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    tituloy = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineaencabezadox = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineaencabezadoy = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    nombrex = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    nombrey = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    fechax = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    fechay = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineacolumnasx = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineacolumnasy = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineacolumnaix = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineacolumnaiy = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    nombrecolumnasy = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    colorcolumna = models.CharField(max_length=100,default='black')
    fontcolumna = models.CharField(max_length=100,default='Helvetica,12,400')
    fontdatos = models.CharField(max_length=100,default='Helvetica,12,400')
    lineapiex = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    lineapiey = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    pagenumberx = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    pagenumbery = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    numerolineaspp = models.IntegerField(default='1')
    numerolineassp = models.IntegerField(default='1')
    numerolineasocupatitulohijo = models.IntegerField(default='1')
    primeralineapp = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    primeralineasp = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    colornombre = models.CharField(max_length=100,default='black')
    fontnombre = models.CharField(max_length=100,default='Helvetica,30,400')
    colortitulo = models.CharField(max_length=100,default='black')
    fonttitulo = models.CharField(max_length=100,default='Helvetica,24,400')
    colorfecha = models.CharField(max_length=100,default='red')
    fontfecha = models.CharField(max_length=100,default='Helvetica,12,400')
    colorpie = models.CharField(max_length=100,default='black')
    fontpie = models.CharField(max_length=100,default='Helvetica,8,400')
    colortitulohijo = models.CharField(max_length=100,default='black')
    fonttitulohijo = models.CharField(max_length=100,default='Helvetica,24,400')
    colorcolumnahijo = models.CharField(max_length=100,default='black')
    fontcolumnahijo = models.CharField(max_length=100,default='Helvetica,12,400')
    identacionposdatoshijo = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    separacionlineasuperiorcolumnas = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    separacioncolumnaslineainferior = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    grosorlineacolumnas = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    grosorlineaencabezado = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    altologo = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    anchologo = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    saltolineadatospadreiniciotitulohijo = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    posxdatospadre = models.DecimalField(decimal_places=2, default=0, max_digits=5)
    saltolineainferiorcolumnadato = models.DecimalField(decimal_places=2, default=0, max_digits=5)

    def __str__(self):
        return self.reportesize

class ReporteNuevo(models.Model):
    
    reportesize = models.CharField(max_length=1,default='l')
    orientacion = models.CharField(max_length=1,default='p')
    posxlogo = models.DecimalField(decimal_places=2, default=1, max_digits=5)
    posylogo = models.DecimalField(decimal_places=2, default=25.70, max_digits=5)
    iniciolineax = models.DecimalField(decimal_places=2, default=1, max_digits=5)
    finallineax = models.DecimalField(decimal_places=2, default=20.50, max_digits=5)
    posxnombre = models.DecimalField(decimal_places=2, default=15, max_digits=5)
    posynombre = models.DecimalField(decimal_places=2, default=26, max_digits=5)
    iniciolineay = models.DecimalField(decimal_places=2, default=25.30, max_digits=5)
    lineapiex = models.DecimalField(decimal_places=2, default=20.50, max_digits=5)
    lineapiey = models.DecimalField(decimal_places=2, default=1.70, max_digits=5)
    piex = models.DecimalField(decimal_places=2, default=20.50, max_digits=5)
    piey = models.DecimalField(decimal_places=2, default=1, max_digits=5)
    maxlineas = models.IntegerField(default=49)
    primeralinea = models.DecimalField(decimal_places=2, default=24.50, max_digits=5)
    grosorlinea = models.DecimalField(decimal_places=2, default=0.9, max_digits=5)
    altologo = models.DecimalField(decimal_places=2, default=1.5, max_digits=5)
    anchologo = models.DecimalField(decimal_places=2, default=1.5, max_digits=5)

    def __str__(self):
        return self.reportesize


class TextFiles(models.Model):
    file = models.CharField(max_length=100)
    texto = models.TextField(default='')

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    def __str__(self):
        return self.file