from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from proyectos.models import Proyecto
from aplicaciones.models import Aplicacion
from modelos.models import Modelo
from propiedades.models import Propiedad
from reglas.models import Regla
from personalizacion.models import Personaliza
from .models import ErroresCreacion
from core.models import Genesis
from registration.views import VerificaVigenciaUsuario
from crear.models import Reporte, ReporteNuevo
from django.urls import reverse_lazy
from .models import ReporteNuevo, TextFiles
from .forms import ReporteForm

import os
import errno
import shutil
import string

class HomeView(TemplateView):
    template_name = "crear/home.html"

    def get_context_data(self,**kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
        gen = Genesis.objects.get(nombre='GENESIS')
        user = self.request.user
        # directorio = '/home/alterego/Documents/proyectos/'
        # directorioArchivosTexto = '/home/alterego/Documents/proyectos/genesisnuevo/core/static/core/textfiles/'
        directorio = gen.directorio
        directoriogenesis = gen.directoriogenesis
        directorioArchivosTexto = gen.directoriotexto
        context['errores'] = False
        estado=int(self.request.GET['estado'])
        if estado == 1: # Se esta creando el proyecto
            CrearProyecto(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 1
                proyecto.save()
        if estado == 2: # Se estan creando las aplicaciones
            CrearProyecto(proyecto,directorio, directorioArchivosTexto,user.username)
            CrearAplicaciones(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 2
                proyecto.save()
        if estado == 3: # Se estan creando los modelos
            CrearProyecto(proyecto,directorio, directorioArchivosTexto,user.username)
            CrearAplicaciones(proyecto,directorio, directorioArchivosTexto,user.username)
            CrearModelos(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 3
                proyecto.save()
        if estado == 4: # Se estan creando las vistas
            CrearVistas(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 4
                proyecto.save()
        if estado == 5: # Se estan creando las urls
            CrearUrls(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 5
                proyecto.save()
        if estado == 6: # Se estan creando los formularios
            CrearForms(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 6
                proyecto.save()
        if estado == 7: # Se estan creando los templates
            # context['avatarwidth'] = proyecto.avatarwidth
            # context['avatarheight'] = proyecto.avatarheight
            
            CrearTemplates(proyecto,directorio, directoriogenesis, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 7
                proyecto.save()
        if estado == 8: # Se estan creando la seguridad
            CrearSeguridad(proyecto,directorio, directorioArchivosTexto,user.username)
            if ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0:
                context['errores'] = True
            else:
                proyecto.estadogeneracion = 8
                proyecto.save()
        context['proyecto'] = proyecto
        context['tiene_errores'] = ErroresCreacion.objects.filter(proyecto=proyecto).count() > 0
        return context

class ListaErroresView(ListView):
    model = Proyecto
    template_name = 'crear/lista_errores.html'

    def get_context_data(self, **kwargs):
        context = super(ListaErroresView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['proyecto'] = proyecto
            context['lista_errores'] = ErroresCreacion.objects.filter(proyecto = proyecto)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        
        return context

class ConfigurarBaseNuevaView(TemplateView):
    template_name = "crear/configuracion_nueva.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarBaseNuevaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomediocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['enfila'] = proyecto.altofilaenizcede
            context['bumefila'] = proyecto.altofilabume
            context['piefila'] = proyecto.altofilapie

            context['separacion'] = proyecto.separacionsecciones
            
            context['proyecto'] = proyecto
            try:
                seccion = self.request.GET['seccion']
                if seccion == 'enfila':
                    proyecto.altofilaenizcede = int(self.request.GET['valor'])
                    context['enfila'] = proyecto.altofilaenizcede
                    proyecto.save()
                if seccion == 'bumefila':
                    proyecto.altofilabume = int(self.request.GET['valor'])
                    context['bumefila'] = proyecto.altofilabume
                    proyecto.save()
                if seccion == 'piefila':
                    proyecto.altofilapie = int(self.request.GET['valor'])
                    context['piefila'] = proyecto.altofilapie
                    proyecto.save()

                if seccion == 'enizquierda':
                    proyecto.numerocolumnaenizquierda = int(self.request.GET['valor'])
                    context['enizquierda'] = proyecto.numerocolumnaenizquierda
                    proyecto.save()
                if seccion == 'enlogo':
                    proyecto.numerocolumnalogo = int(self.request.GET['valor'])
                    context['enlogo'] = proyecto.numerocolumnalogo
                    proyecto.save()
                if seccion == 'entitulo':
                    proyecto.numerocolumnatitulo = int(self.request.GET['valor'])
                    context['entitulo'] = proyecto.numerocolumnatitulo
                    proyecto.save()
                if seccion == 'enlogin':
                    proyecto.numerocolumnalogin = int(self.request.GET['valor'])
                    context['enlogin'] = proyecto.numerocolumnalogin
                    proyecto.save()
                if seccion == 'enderecha':
                    proyecto.numerocolumnaenderecha = int(self.request.GET['valor'])
                    context['enderecha'] = proyecto.numerocolumnaenderecha
                    proyecto.save()

                if seccion == 'bumeizquierda':
                    proyecto.numerocolumnabumeizquierda = int(self.request.GET['valor'])
                    context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
                    proyecto.save()
                if seccion == 'bumebusqueda':
                    proyecto.numerocolumnabusqueda = int(self.request.GET['valor'])
                    context['anchobusqueda'] = proyecto.numerocolumnabusqueda
                    proyecto.save()
                if seccion == 'bumemenu':
                    proyecto.numerocolumnamenu = int(self.request.GET['valor'])
                    context['anchomenu'] = proyecto.numerocolumnamenu
                    proyecto.save()
                if seccion == 'bumederecha':
                    proyecto.numerocolumnabumederecha = int(self.request.GET['valor'])
                    context['anchobumederecha'] = proyecto.numerocolumnabumederecha
                    proyecto.save()

                if seccion == 'cenizquierda':
                    proyecto.numerocolumnamedioizquierda = int(self.request.GET['valor'])
                    context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
                    proyecto.save()
                if seccion == 'cencentro':
                    proyecto.numerocolumnamediocentro = int(self.request.GET['valor'])
                    context['anchomediocentro'] = proyecto.numerocolumnamediocentro
                    proyecto.save()
                if seccion == 'cenderecha':
                    proyecto.numerocolumnamedioderecha = int(self.request.GET['valor'])
                    context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
                    proyecto.save()
            except:
                pass
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class ConfigurarBaseView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configuracion.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarBaseView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha
            # Alto y ancho de secciones

            try:
                flecha = self.request.GET['flecha']
                if flecha == "faltoencabezado": #alto encabezado
                    elpor = 5
                    if self.request.GET['direccion'] == 'menos':
                        elpor = -5
                    proyecto.altofilaenizcede = proyecto.altofilaenizcede + elpor
                    proyecto.altocolumnaenizquierda = proyecto.altofilaenizcede
                    proyecto.altocolumnalogo = proyecto.altofilaenizcede
                    proyecto.altocolumnatitulo = proyecto.altofilaenizcede
                    proyecto.altocolumnalogin = proyecto.altofilaenizcede
                    proyecto.altocolumnaenderecha = proyecto.altofilaenizcede
                    proyecto.save()
                    context['altoencabezado'] = str(int(self.request.GET['height']) + elpor) + 'px'
                if flecha == "ei": #ancho izquierda encabezado
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnaenizquierda > 0:
                            context['numerocolumnaenizquierda'] =  proyecto.numerocolumnaenizquierda - 1
                            proyecto.numerocolumnaenizquierda =  proyecto.numerocolumnaenizquierda - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnaenizquierda + proyecto.numerocolumnalogo + proyecto.numerocolumnatitulo + proyecto.numerocolumnalogin+ proyecto.numerocolumnaenderecha < 12:
                            context['numerocolumnaenizquierda'] =  proyecto.numerocolumnaenizquierda + 1
                            proyecto.numerocolumnaenizquierda =  proyecto.numerocolumnaenizquierda + 1
                            proyecto.save()
                if flecha == "logo": #ancho logo
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnalogo > 0:
                            context['numerocolumnalogo'] =  proyecto.numerocolumnalogo - 1
                            proyecto.numerocolumnalogo =  proyecto.numerocolumnalogo - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnaenizquierda + proyecto.numerocolumnalogo + proyecto.numerocolumnatitulo + proyecto.numerocolumnalogin+ proyecto.numerocolumnaenderecha < 12:
                            context['numerocolumnalogo'] =  proyecto.numerocolumnalogo + 1
                            proyecto.numerocolumnalogo =  proyecto.numerocolumnalogo + 1
                            proyecto.save()
                if flecha == "titulo": #ancho titulo
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnatitulo > 0:
                            context['numerocolumnatitulo'] =  proyecto.numerocolumnatitulo - 1
                            proyecto.numerocolumnatitulo =  proyecto.numerocolumnatitulo - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnaenizquierda + proyecto.numerocolumnalogo + proyecto.numerocolumnatitulo + proyecto.numerocolumnalogin+ proyecto.numerocolumnaenderecha < 12:
                            context['numerocolumnatitulo'] =  proyecto.numerocolumnatitulo + 1
                            proyecto.numerocolumnatitulo =  proyecto.numerocolumnatitulo + 1
                            proyecto.save()
                if flecha == "login": #ancho login encabezado
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnalogin > 0:
                            context['numerocolumnalogin'] =  proyecto.numerocolumnalogin - 1
                            proyecto.numerocolumnalogin =  proyecto.numerocolumnalogin - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnaenizquierda + proyecto.numerocolumnalogo + proyecto.numerocolumnatitulo + proyecto.numerocolumnalogin+ proyecto.numerocolumnaenderecha < 12:
                            context['numerocolumnalogin'] =  proyecto.numerocolumnalogin + 1
                            proyecto.numerocolumnalogin =  proyecto.numerocolumnalogin + 1
                            proyecto.save()
                if flecha == "ed": #ancho derecha encabezado
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnaenderecha > 0:
                            context['numerocolumnaenderecha'] =  proyecto.numerocolumnaenderecha - 1
                            proyecto.numerocolumnaenderecha =  proyecto.numerocolumnaenderecha - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnaenizquierda + proyecto.numerocolumnalogo + proyecto.numerocolumnatitulo + proyecto.numerocolumnalogin+ proyecto.numerocolumnaenderecha < 12:
                            context['numerocolumnaenderecha'] =  proyecto.numerocolumnaenderecha + 1
                            proyecto.numerocolumnaenderecha =  proyecto.numerocolumnaenderecha + 1
                            proyecto.save()
                if flecha == "faltobume": #alto bume
                    elpor = 5
                    if self.request.GET['direccion'] == 'menos':
                        elpor = -5
                    proyecto.altofilabume = proyecto.altofilabume + elpor
                    proyecto.altocolumnabumeizquierda = proyecto.altofilabume
                    proyecto.altocolumnabumederecha = proyecto.altofilabume
                    proyecto.altocolumnabusqueda = proyecto.altofilabume
                    proyecto.altocolumnamenu = proyecto.altofilabume
                    proyecto.save()
                    context['altobume'] = str(int(self.request.GET['height']) + elpor) + 'px'
                if flecha == "bi": #ancho izquierda busqueda
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnabumeizquierda > 0:
                            context['numerocolumnabumeizquierda'] =  proyecto.numerocolumnabumeizquierda - 1
                            proyecto.numerocolumnabumeizquierda =  proyecto.numerocolumnabumeizquierda - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnabumeizquierda + proyecto.numerocolumnabusqueda + proyecto.numerocolumnamenu + proyecto.numerocolumnabumederecha < 12:
                            context['numerocolumnabumeizquierda'] =  proyecto.numerocolumnabumeizquierda + 1
                            proyecto.numerocolumnabumeizquierda =  proyecto.numerocolumnabumeizquierda + 1
                            proyecto.save()
                if flecha == "busqueda": #ancho busqueda
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnabusqueda > 0:
                            context['numerocolumnabusqueda'] =  proyecto.numerocolumnabusqueda - 1
                            proyecto.numerocolumnabusqueda =  proyecto.numerocolumnabusqueda - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnabumeizquierda + proyecto.numerocolumnabusqueda + proyecto.numerocolumnamenu + proyecto.numerocolumnabumederecha < 12:
                            context['numerocolumnabusqueda'] =  proyecto.numerocolumnabusqueda + 1
                            proyecto.numerocolumnabusqueda =  proyecto.numerocolumnabusqueda + 1
                            proyecto.save()
                if flecha == "menu": #ancho menu
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnamenu > 0:
                            context['numerocolumnamenu'] =  proyecto.numerocolumnamenu - 1
                            proyecto.numerocolumnamenu =  proyecto.numerocolumnamenu - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnabumeizquierda + proyecto.numerocolumnabusqueda + proyecto.numerocolumnamenu + proyecto.numerocolumnabumederecha < 12:
                            context['numerocolumnamenu'] =  proyecto.numerocolumnamenu + 1
                            proyecto.numerocolumnamenu =  proyecto.numerocolumnamenu + 1
                            proyecto.save()
                if flecha == "bd": #ancho bume derecha
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnabumederecha > 0:
                            context['numerocolumnabumederecha'] =  proyecto.numerocolumnabumederecha - 1
                            proyecto.numerocolumnabumederecha =  proyecto.numerocolumnabumederecha - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnabumeizquierda + proyecto.numerocolumnabusqueda + proyecto.numerocolumnamenu + proyecto.numerocolumnabumederecha < 12:
                            context['numerocolumnabumederecha'] =  proyecto.numerocolumnabumederecha + 1
                            proyecto.numerocolumnabumederecha =  proyecto.numerocolumnabumederecha + 1
                            proyecto.save()
                if flecha == "mi": #ancho izquierda medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnamedioizquierda > 0:
                            context['numerocolumnamedioizquierda'] =  proyecto.numerocolumnamedioizquierda - 1
                            proyecto.numerocolumnamedioizquierda =  proyecto.numerocolumnamedioizquierda - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnamedioizquierda + proyecto.numerocolumnamediocentro + proyecto.numerocolumnamedioderecha < 12:
                            context['numerocolumnamedioizquierda'] =  proyecto.numerocolumnamedioizquierda + 1
                            proyecto.numerocolumnamedioizquierda =  proyecto.numerocolumnamedioizquierda + 1
                            proyecto.save()
                if flecha == "mc": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnamediocentro > 0:
                            context['numerocolumnamediocentro'] =  proyecto.numerocolumnamediocentro - 1
                            proyecto.numerocolumnamediocentro =  proyecto.numerocolumnamediocentro - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnamedioizquierda + proyecto.numerocolumnamediocentro + proyecto.numerocolumnamedioderecha < 12:
                            context['numerocolumnamediocentro'] =  proyecto.numerocolumnamediocentro + 1
                            proyecto.numerocolumnamediocentro =  proyecto.numerocolumnamediocentro + 1
                            proyecto.save()
                if flecha == "md": #ancho medio derecha
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if proyecto.numerocolumnamedioderecha > 0:
                            context['numerocolumnamedioderecha'] =  proyecto.numerocolumnamedioderecha - 1
                            proyecto.numerocolumnamedioderecha =  proyecto.numerocolumnamedioderecha - 1
                            proyecto.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if proyecto.numerocolumnamedioizquierda + proyecto.numerocolumnamediocentro + proyecto.numerocolumnamedioderecha < 12:
                            context['numerocolumnamedioderecha'] =  proyecto.numerocolumnamedioderecha + 1
                            proyecto.numerocolumnamedioderecha =  proyecto.numerocolumnamedioderecha + 1
                            proyecto.save()
                if flecha == "faltopie": #alto pie
                    elpor = 5
                    if self.request.GET['direccion'] == 'menos':
                        elpor = -5
                    proyecto.altofilapie = proyecto.altofilapie + elpor
                    proyecto.save()
                    context['altopie'] = str(int(self.request.GET['height']) + elpor) + 'px'

            except:
                pass

            c1 = '#abadaf'
            c2 = '#bbbdbf'
            c3 = '#cbcdcf'
            c4 = '#dbdddf'
            c5 = '#ebedef'

            context['colorfilaenizcede'] = proyecto.colorfilaenizcede
            context['colorcolumnaenizquierda'] = c1
            context['colorcolumnalogo'] = c2
            context['colorcolumnatitulo'] = c3
            context['colorcolumnalogin'] = c4
            context['colorcolumnaenderecha'] = c5
            context['colorfilabume'] = proyecto.colorfilabume
            context['colorcolumnabumeizquierda'] = c1
            context['colorcolumnabusqueda'] = c2
            context['colorcolumnamenu'] = c3
            context['colorcolumnabumederecha'] = c4
            context['colorfilamedio'] = proyecto.colorfilamedio
            context['colorcolumnamedioizquierda'] = c1
            context['colorcolumnamedioderecha'] = c2
            context['colorcolumnamediocentro'] = c3
            context['colorfilapie'] = proyecto.colorfilapie
            context['colorcolumnapie'] = c1
            
            context['proyecto'] = proyecto
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class PaletaView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/paleta.html"

    def get_context_data(self,**kwargs):
        context = super(PaletaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            configuracion = self.request.GET['configuracion_proyecto']
            context['configuracion'] = configuracion
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['proyecto'] = proyecto
            context['div'] = self.request.GET['div']
            context['red'] = self.request.GET['red']
            context['green'] = self.request.GET['green']
            context['blue'] = self.request.GET['blue']

            listaf1 = []
            listaf2 = []

            # lista.append([te.topico.upper(),te.descripcion,str(te.correlativo) + '.',te.diagrama,'e',te.id])
            listaf1.append(['003366','10','-5'])
            listaf1.append(['336699','12','-5'])
            listaf1.append(['3366cc','14','-5'])
            listaf1.append(['003399','16','-5'])
            listaf1.append(['000099','18','-5'])
            listaf1.append(['0000cc','20','-5'])
            listaf1.append(['000066','22','-5'])

            listaf1.append(['006666','9','-3.3'])
            listaf1.append(['006699','11','-5'])
            listaf1.append(['0099cc','13','-5'])
            listaf1.append(['0066cc','15','-5'])
            listaf1.append(['0033cc','17','-5'])
            listaf1.append(['0000ff','19','-5'])
            listaf1.append(['3333ff','21','-5'])
            listaf1.append(['333399','23','-5'])

            listaf1.append(['669999','8','-3.3'])
            listaf1.append(['009999','10','-5'])
            listaf1.append(['33cccc','12','-5'])
            listaf1.append(['00ccff','14','-5'])
            listaf1.append(['0099ff','16','-5'])
            listaf1.append(['0066ff','18','-5'])
            listaf1.append(['3366ff','20','-5'])
            listaf1.append(['3333cc','22','-5'])
            listaf1.append(['666699','24','-5'])

            listaf1.append(['339966','7','-3.3'])
            listaf1.append(['00cc99','9','-5'])
            listaf1.append(['00ffcc','11','-5'])
            listaf1.append(['00ffff','13','-5'])
            listaf1.append(['33ccff','15','-5'])
            listaf1.append(['3399ff','17','-5'])
            listaf1.append(['6699ff','19','-5'])
            listaf1.append(['6666ff','21','-5'])
            listaf1.append(['6600ff','23','-5'])
            listaf1.append(['6600cc','25','-5'])

            listaf1.append(['339933','6','-3.3'])
            listaf1.append(['00cc66','8','-5'])
            listaf1.append(['00ff99','10','-5'])
            listaf1.append(['66ffcc','12','-5'])
            listaf1.append(['66ffff','14','-5'])
            listaf1.append(['66ccff','16','-5'])
            listaf1.append(['99ccff','18','-5'])
            listaf1.append(['9999ff','20','-5'])
            listaf1.append(['9966ff','22','-5'])
            listaf1.append(['9933ff','24','-5'])
            listaf1.append(['9900ff','26','-5'])

            listaf1.append(['006600','5','-3.3'])
            listaf1.append(['00cc00','7','-5'])
            listaf1.append(['00ff00','9','-5'])
            listaf1.append(['66ff99','11','-5'])
            listaf1.append(['99ffcc','13','-5'])
            listaf1.append(['ccffff','15','-5'])
            listaf1.append(['ccccff','17','-5'])
            listaf1.append(['cc99ff','19','-5'])
            listaf1.append(['cc66ff','21','-5'])
            listaf1.append(['cc33ff','23','-5'])
            listaf1.append(['cc00ff','25','-5'])
            listaf1.append(['9900cc','27','-5'])

            listaf1.append(['003300','4','-3.3'])
            listaf1.append(['009933','6','-5'])
            listaf1.append(['33cc33','8','-5'])
            listaf1.append(['66ff66','10','-5'])
            listaf1.append(['99ff99','12','-5'])
            listaf1.append(['ccffcc','14','-5'])
            listaf1.append(['ffffff','16','-5'])
            listaf1.append(['ffccff','18','-5'])
            listaf1.append(['ff99ff','20','-5'])
            listaf1.append(['ff66ff','22','-5'])
            listaf1.append(['ff00ff','24','-5'])
            listaf1.append(['cc00cc','26','-5'])
            listaf1.append(['660066','28','-5'])

            listaf1.append(['336600','5','-3.3'])
            listaf1.append(['009900','7','-5'])
            listaf1.append(['66ff33','9','-5'])
            listaf1.append(['99ff66','11','-5'])
            listaf1.append(['ccff99','13','-5'])
            listaf1.append(['ffffcc','15','-5'])
            listaf1.append(['ffcccc','17','-5'])
            listaf1.append(['ff99cc','19','-5'])
            listaf1.append(['ff66cc','21','-5'])
            listaf1.append(['ff33cc','23','-5'])
            listaf1.append(['cc0099','25','-5'])
            listaf1.append(['993399','27','-5'])

            listaf1.append(['333300','6','-3.3'])
            listaf1.append(['669900','8','-5'])
            listaf1.append(['99ff33','10','-5'])
            listaf1.append(['ccff66','12','-5'])
            listaf1.append(['ffff99','14','-5'])
            listaf1.append(['ffcc99','16','-5'])
            listaf1.append(['ff9999','18','-5'])
            listaf1.append(['ff6699','20','-5'])
            listaf1.append(['ff3399','22','-5'])
            listaf1.append(['cc3399','24','-5'])
            listaf1.append(['990099','26','-5'])

            listaf1.append(['666633','7','-3.3'])
            listaf1.append(['99cc00','9','-5'])
            listaf1.append(['ccff33','11','-5'])
            listaf1.append(['ffff66','13','-5'])
            listaf1.append(['ffcc66','15','-5'])
            listaf1.append(['ff9966','17','-5'])
            listaf1.append(['ff6666','19','-5'])
            listaf1.append(['ff0066','21','-5'])
            listaf1.append(['cc6699','23','-5'])
            listaf1.append(['993366','25','-5'])

            listaf1.append(['999966','8','-3.3'])
            listaf1.append(['cccc00','10','-5'])
            listaf1.append(['ffff00','12','-5'])
            listaf1.append(['ffcc00','14','-5'])
            listaf1.append(['ff9933','16','-5'])
            listaf1.append(['ff6600','18','-5'])
            listaf1.append(['ff5050','20','-5'])
            listaf1.append(['cc0066','22','-5'])
            listaf1.append(['660033','24','-5'])

            listaf1.append(['996633','9','-3.3'])
            listaf1.append(['cc9900','11','-5'])
            listaf1.append(['ff9900','13','-5'])
            listaf1.append(['cc6600','15','-5'])
            listaf1.append(['ff3300','17','-5'])
            listaf1.append(['ff0000','19','-5'])
            listaf1.append(['cc0000','21','-5'])
            listaf1.append(['990033','23','-5'])

            listaf1.append(['663300','10','-3.3'])
            listaf1.append(['996600','12','-5'])
            listaf1.append(['cc3300','14','-5'])
            listaf1.append(['993300','16','-5'])
            listaf1.append(['990000','18','-5'])
            listaf1.append(['800000','20','-5'])
            listaf1.append(['993333','22','-5'])

            # Nuevo colores

            listaf2.append(['008844','10','-5'])
            listaf2.append(['884422','12','-5'])
            listaf2.append(['8844cc','14','-5'])
            listaf2.append(['008822','16','-5'])
            listaf2.append(['000022','18','-5'])
            listaf2.append(['0000cc','20','-5'])
            listaf2.append(['000044','22','-5'])

            listaf2.append(['004444','9','-3.3'])
            listaf2.append(['004422','11','-5'])
            listaf2.append(['0022cc','13','-5'])
            listaf2.append(['0044cc','15','-5'])
            listaf2.append(['0088cc','17','-5'])
            listaf2.append(['0000ff','19','-5'])
            listaf2.append(['8888ff','21','-5'])
            listaf2.append(['888822','23','-5'])

            listaf2.append(['442222','8','-3.3'])
            listaf2.append(['002222','10','-5'])
            listaf2.append(['88cccc','12','-5'])
            listaf2.append(['00ccff','14','-5'])
            listaf2.append(['0022ff','16','-5'])
            listaf2.append(['0044ff','18','-5'])
            listaf2.append(['8844ff','20','-5'])
            listaf2.append(['8888cc','22','-5'])
            listaf2.append(['444422','24','-5'])

            listaf2.append(['882244','7','-3.3'])
            listaf2.append(['00cc22','9','-5'])
            listaf2.append(['00ffcc','11','-5'])
            listaf2.append(['00ffff','13','-5'])
            listaf2.append(['88ccff','15','-5'])
            listaf2.append(['8822ff','17','-5'])
            listaf2.append(['4422ff','19','-5'])
            listaf2.append(['4444ff','21','-5'])
            listaf2.append(['4400ff','23','-5'])
            listaf2.append(['4400cc','25','-5'])

            listaf2.append(['882288','6','-3.3'])
            listaf2.append(['00cc44','8','-5'])
            listaf2.append(['00ff22','10','-5'])
            listaf2.append(['44ffcc','12','-5'])
            listaf2.append(['44ffff','14','-5'])
            listaf2.append(['44ccff','16','-5'])
            listaf2.append(['22ccff','18','-5'])
            listaf2.append(['2222ff','20','-5'])
            listaf2.append(['2244ff','22','-5'])
            listaf2.append(['2288ff','24','-5'])
            listaf2.append(['2200ff','26','-5'])

            listaf2.append(['004400','5','-3.3'])
            listaf2.append(['00cc00','7','-5'])
            listaf2.append(['00ff00','9','-5'])
            listaf2.append(['44ff22','11','-5'])
            listaf2.append(['22ffcc','13','-5'])
            listaf2.append(['ccffff','15','-5'])
            listaf2.append(['ccccff','17','-5'])
            listaf2.append(['cc22ff','19','-5'])
            listaf2.append(['cc44ff','21','-5'])
            listaf2.append(['cc88ff','23','-5'])
            listaf2.append(['cc00ff','25','-5'])
            listaf2.append(['2200cc','27','-5'])

            listaf2.append(['008800','4','-3.3'])
            listaf2.append(['002288','6','-5'])
            listaf2.append(['88cc88','8','-5'])
            listaf2.append(['44ff44','10','-5'])
            listaf2.append(['22ff22','12','-5'])
            listaf2.append(['ccffcc','14','-5'])
            listaf2.append(['ffffff','16','-5'])
            listaf2.append(['ffccff','18','-5'])
            listaf2.append(['ff22ff','20','-5'])
            listaf2.append(['ff44ff','22','-5'])
            listaf2.append(['ff00ff','24','-5'])
            listaf2.append(['cc00cc','26','-5'])
            listaf2.append(['440044','28','-5'])

            listaf2.append(['884400','5','-3.3'])
            listaf2.append(['002200','7','-5'])
            listaf2.append(['44ff88','9','-5'])
            listaf2.append(['22ff44','11','-5'])
            listaf2.append(['ccff22','13','-5'])
            listaf2.append(['ffffcc','15','-5'])
            listaf2.append(['ffcccc','17','-5'])
            listaf2.append(['ff22cc','19','-5'])
            listaf2.append(['ff44cc','21','-5'])
            listaf2.append(['ff88cc','23','-5'])
            listaf2.append(['cc0022','25','-5'])
            listaf2.append(['228822','27','-5'])

            listaf2.append(['888800','6','-3.3'])
            listaf2.append(['442200','8','-5'])
            listaf2.append(['22ff88','10','-5'])
            listaf2.append(['ccff44','12','-5'])
            listaf2.append(['ffff22','14','-5'])
            listaf2.append(['ffcc22','16','-5'])
            listaf2.append(['ff2222','18','-5'])
            listaf2.append(['ff4422','20','-5'])
            listaf2.append(['ff8822','22','-5'])
            listaf2.append(['cc8822','24','-5'])
            listaf2.append(['220022','26','-5'])

            listaf2.append(['444488','7','-3.3'])
            listaf2.append(['22cc00','9','-5'])
            listaf2.append(['ccff88','11','-5'])
            listaf2.append(['ffff44','13','-5'])
            listaf2.append(['ffcc44','15','-5'])
            listaf2.append(['ff2244','17','-5'])
            listaf2.append(['ff4444','19','-5'])
            listaf2.append(['ff0044','21','-5'])
            listaf2.append(['cc4422','23','-5'])
            listaf2.append(['228844','25','-5'])

            listaf2.append(['222244','8','-3.3'])
            listaf2.append(['cccc00','10','-5'])
            listaf2.append(['ffff00','12','-5'])
            listaf2.append(['ffcc00','14','-5'])
            listaf2.append(['ff2288','16','-5'])
            listaf2.append(['ff4400','18','-5'])
            listaf2.append(['ff5050','20','-5'])
            listaf2.append(['cc0044','22','-5'])
            listaf2.append(['440088','24','-5'])

            listaf2.append(['224488','9','-3.3'])
            listaf2.append(['cc2200','11','-5'])
            listaf2.append(['ff2200','13','-5'])
            listaf2.append(['cc4400','15','-5'])
            listaf2.append(['ff8800','17','-5'])
            listaf2.append(['ff0000','19','-5'])
            listaf2.append(['cc0000','21','-5'])
            listaf2.append(['220088','23','-5'])

            listaf2.append(['448800','10','-3.3'])
            listaf2.append(['224400','12','-5'])
            listaf2.append(['cc8800','14','-5'])
            listaf2.append(['228800','16','-5'])
            listaf2.append(['220000','18','-5'])
            listaf2.append(['800000','20','-5'])
            listaf2.append(['228888','22','-5'])



            context['l1'] = listaf1
            context['l2'] = listaf2

            # lista=list(range(0,255,10))
            listar=list(range(0,255))
            listag=list(range(0,255))
            listab=list(range(0,255))
            # print('lista ',lista)
            # context['numeros'] = lista
            context['listar'] = listar
            context['listag'] = listag
            context['listab'] = listab
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class ColoresView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configuracion_color.html"

    def get_context_data(self,**kwargs):
        context = super(ColoresView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            configuracion = self.request.GET['configuracion_proyecto']
            context['configuracion'] = configuracion
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha

            # colores de secciones

            try:
                # color = 'rgba(' + self.request.GET['color'] + ')'
                color = '#' + self.request.GET['color']
                div = self.request.GET['div']
                context[div] = div
                if div == 'colorfilaenizcede':
                    proyecto.colorfilaenizcede = color
                if div == 'colorcolumnaenizquierda':
                    proyecto.colorcolumnaenizquierda = color
                if div == 'colorcolumnalogo':
                    proyecto.colorcolumnalogo = color
                if div == 'colorcolumnatitulo':
                    proyecto.colorcolumnatitulo = color
                if div == 'colorcolumnalogin':
                    proyecto.colorcolumnalogin = color
                if div == 'colorcolumnaenderecha':
                    proyecto.colorcolumnaenderecha = color
                if div == 'colorfilabume':
                    proyecto.colorfilabume = color
                if div == 'colorcolumnabumeizquierda':
                    proyecto.colorcolumnabumeizquierda = color
                if div == 'colorcolumnabusqueda':
                    proyecto.colorcolumnabusqueda = color
                if div == 'colorcolumnamenu':
                    proyecto.colorcolumnamenu = color
                if div == 'colorcolumnabumederecha':
                    proyecto.colorcolumnabumederecha = color
                if div == 'colorfilamedio':
                    proyecto.colorfilamedio = color
                if div == 'colorcolumnamedioizquierda':
                    proyecto.colorcolumnamedioizquierda = color
                if div == 'colorcolumnamedioderecha':
                    proyecto.colorcolumnamedioderecha = color
                if div == 'colorcolumnamediocentro':
                    proyecto.colorcolumnamediocentro = color
                if div == 'colorfilapie':
                    proyecto.colorfilapie = color
                if div == 'colorcolumnapie':
                    proyecto.colorcolumnapie = color
                proyecto.save()
            except:
                pass        
            # Colores
            context['colorfilaenizcede'] = proyecto.colorfilaenizcede
            context['colorcolumnaenizquierda'] = proyecto.colorcolumnaenizquierda
            context['colorcolumnalogo'] = proyecto.colorcolumnalogo
            context['colorcolumnatitulo'] = proyecto.colorcolumnatitulo
            context['colorcolumnalogin'] = proyecto.colorcolumnalogin
            context['colorcolumnaenderecha'] = proyecto.colorcolumnaenderecha
            context['colorfilabume'] = proyecto.colorfilabume
            context['colorcolumnabumeizquierda'] = proyecto.colorcolumnabumeizquierda
            context['colorcolumnabusqueda'] = proyecto.colorcolumnabusqueda
            context['colorcolumnamenu'] = proyecto.colorcolumnamenu
            context['colorcolumnabumederecha'] = proyecto.colorcolumnabumederecha
            context['colorfilamedio'] = proyecto.colorfilamedio
            context['colorcolumnamedioizquierda'] = proyecto.colorcolumnamedioizquierda
            context['colorcolumnamedioderecha'] = proyecto.colorcolumnamedioderecha
            context['colorcolumnamediocentro'] = proyecto.colorcolumnamediocentro
            context['colorfilapie'] = proyecto.colorfilapie
            context['colorcolumnapie'] = proyecto.colorcolumnapie
            context['proyecto'] = proyecto
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class OtrosView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configuracion_otros.html"

    def get_context_data(self,**kwargs):
        context = super(OtrosView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha
        
            salto = 10
            saltoy = 5
            incremento = 5

            try:
                direccion = self.request.GET['direccion']
                if direccion == 'logocentro':
                    proyecto.justificacionverticallogo = 'c'
                    proyecto.justificacionhorizontallogo = 'c'
                if direccion == 'logoabajo':
                    proyecto.justificacionverticallogo = 'i'
                if direccion == 'logoarriba':
                    proyecto.justificacionverticallogo = 's'
                if direccion == 'logoderecha':
                    proyecto.justificacionhorizontallogo = 'd'
                if direccion == 'logoizquierda':
                    proyecto.justificacionhorizontallogo = 'i'
                if direccion == 'titulocentro':
                    proyecto.justificacionverticaltitulo = 'c'
                    proyecto.justificacionhorizontaltitulo = 'c'
                if direccion == 'tituloabajo':
                    proyecto.justificacionverticaltitulo = 'i'
                if direccion == 'tituloarriba':
                    proyecto.justificacionverticaltitulo = 's'
                if direccion == 'tituloderecha':
                    proyecto.justificacionhorizontaltitulo = 'd'
                if direccion == 'tituloizquierda':
                    proyecto.justificacionhorizontaltitulo = 'i'
                # if direccion == 'logocentro':
                #     proyecto.justificacionhorizontallogo = 'c'
                #     proyecto.justificacionverticallogo = 'c'
                # if direccion == 'titulocentro':
                #     proyecto.justificacionhorizontaltitulo = 'c'
                #     proyecto.justificacionverticaltitulo = 'c'

                proyecto.save()
            except:
                pass

            try:
                direccion = self.request.GET['dimension']
                if direccion == 'logomasabajo':
                    proyecto.avatarheight = proyecto.avatarheight + incremento
                if direccion == 'logomenosarriba':
                    proyecto.avatarheight = proyecto.avatarheight - incremento
                if direccion == 'logomasderecha':
                    proyecto.avatarwidth = proyecto.avatarwidth + incremento
                if direccion == 'logomenosizquierda':
                    proyecto.avatarwidth = proyecto.avatarwidth - incremento
                if direccion == 'titulomasabajo':
                    proyecto.imagentituloheight = proyecto.imagentituloheight + incremento
                if direccion == 'titulomenosarriba':
                    proyecto.imagentituloheight = proyecto.imagentituloheight - incremento
                if direccion == 'titulomasderecha':
                    proyecto.imagentitulowidth = proyecto.imagentitulowidth + incremento
                if direccion == 'titulomenosizquierda':
                    proyecto.imagentitulowidth = proyecto.imagentitulowidth - incremento
                # if direccion == 'logocentro':
                #     proyecto.justificacionhorizontallogo = 'c'
                #     proyecto.justificacionverticallogo = 'c'
                # if direccion == 'titulocentro':
                #     proyecto.justificacionhorizontaltitulo = 'c'
                #     proyecto.justificacionverticaltitulo = 'c'

                proyecto.save()
            except  Exception as e:
                print(e)

            if proyecto.justificacionhorizontallogo == 'i':
                context['horizontallogo'] = 'justify-content-start'    
            if proyecto.justificacionhorizontallogo == 'c':
                context['horizontallogo'] = 'justify-content-center'    
            if proyecto.justificacionhorizontallogo == 'd':
                context['horizontallogo'] = 'justify-content-end'    
            if proyecto.justificacionverticallogo == 'i':
                context['verticallogo'] = 'align-items-end'    
            if proyecto.justificacionverticallogo == 'c':
                context['verticallogo'] = 'align-items-center'    
            if proyecto.justificacionverticallogo == 's':
                context['verticallogo'] = 'align-items-start'    
            if proyecto.justificacionhorizontaltitulo == 'i':
                context['horizontaltitulo'] = 'justify-content-start'    
            if proyecto.justificacionhorizontaltitulo == 'c':
                context['horizontaltitulo'] = 'justify-content-center'    
            if proyecto.justificacionhorizontaltitulo == 'd':
                context['horizontaltitulo'] = 'justify-content-end'    
            if proyecto.justificacionverticaltitulo == 'i':
                context['verticaltitulo'] = 'align-items-end'    
            if proyecto.justificacionverticaltitulo == 'c':
                context['verticaltitulo'] = 'align-items-center'    
            if proyecto.justificacionverticaltitulo == 's':
                context['verticaltitulo'] = 'align-items-start'    

            # # Alto y ancho de secciones
            # if proyecto.justificacionhorizontallogo == 'c':
            #     context['horizontallogo'] = 'justify-content-center'
            # if proyecto.justificacionhorizontallogo == 'i':
            #     context['horizontallogo'] = 'justify-content-start'
            # if proyecto.justificacionhorizontallogo == 'd':
            #     context['horizontallogo'] = 'justify-content-end'
            # if proyecto.justificacionverticallogo == 's':
            #     context['verticallogo'] = 'align-items-start'
            # if proyecto.justificacionverticallogo == 'c':
            #     context['verticallogo'] = 'align-items-center'
            # if proyecto.justificacionverticallogo == 'i':
            #     context['verticallogo'] = 'align-items-end'
            # if proyecto.justificacionhorizontaltitulo == 'c':
            #     context['horizontaltitulo'] = 'justify-content-center'
            # if proyecto.justificacionhorizontaltitulo == 'i':
            #     context['horizontaltitulo'] = 'justify-content-start'
            # if proyecto.justificacionhorizontaltitulo == 'd':
            #     context['horizontaltitulo'] = 'justify-content-end'
            # if proyecto.justificacionverticaltitulo == 's':
            #     context['verticaltitulo'] = 'align-items-start'
            # if proyecto.justificacionverticaltitulo == 'c':
            #     context['verticaltitulo'] = 'align-items-center'
            # if proyecto.justificacionverticaltitulo == 'i':
            #     context['verticaltitulo'] = 'align-items-end'
        
            # Colores

            context['altologo'] = str(proyecto.avatarheight) + 'px'
            context['anchologo'] = str(proyecto.avatarwidth) + 'px'
            context['altotitulo'] = str(proyecto.imagentituloheight) + 'px'
            context['anchotitulo'] = str(proyecto.imagentitulowidth) + 'px'

            context['proyecto'] = proyecto
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        
        return context

def AltoNegativo(alto):
    return str(alto) + 'px' if alto >0 else str(alto*-1) + "%"

def ManejoArchivos(proyecto,directorio):

    # Crear directorios
    # print('CREANDO DIRECTORIOS')
    try:
        os.mkdir(directorio + proyecto.nombre)
    except:
        print('existe')

    # print('LEYENDO ARCHIVOS EN BLOQUE')
    # Leer archivos en bloque
    filename = '/home/alterego/Downloads/cambiotecladoubuntu'
    try:
        with open(filename) as file_object:
            contents = file_object.read()
    except:
        print('no hay archivo')

    # print('LEYENDO ARCHIVOS LINEA A LINEA')
    # Leer archivos linea a linea
    filename = '/home/alterego/Downloads/cambiotecladoubuntu'
    try:
        with open(filename) as file_object:
            for line in file_object:
                pass
                # print(line)
    except:
        print('No existe el archivo')

    # print('ESCRIBIENDO ARCHIVOS')
    # Escribir archivos
    try:
        filename = '/home/alterego/Downloads/pruebanuevo.txt'
        with open(filename, 'w') as file_object:
            file_object.write("Python, el lenguaje del futuro")
    except:
        print('No se escribe el archivo')

    # print('COPIANDO ARCHIVOS')
    # Copiar archivos
    origen = '/home/alterego/Downloads/cambiotecladoubuntu'
    destino = '/home/alterego/Downloads/nuevocambiotecladoubuntu'
    try:
        shutil.copy(origen, destino)
    except:
        print('No se copio el archivo')

    # print('MOVER ARCHIVOS')
    # # Mover archivos
    origen = '/home/alterego/Downloads/nuevocambiotecladoubuntu'
    destino = '/home/alterego/Documents/proyectos/Tercer proyecto/nuevocambiotecladoubuntu'
    shutil.move(origen, destino)

    # print('COPIAR DIRECTORIOS')
    # Copiar directorios
    origen = '/home/alterego/Documents/proyectos/Tercer proyecto'
    destino = '/home/alterego/Documents/proyectos/Tercer proyecto nuevo'
    try:
        shutil.copytree(origen, destino)
    except:
        print('No se movio el directorio')

    # print('MOVER DIRECTORIOS')
    # Mover directorios
    origen = '/home/alterego/Documents/proyectos/Tercer proyecto nuevo'
    destino = '/home/alterego/Downloads/Tercer proyecto nuevo'
    try:
        shutil.move(origen, destino)
    except:
        print('No se movio el directorio')

    # print('ELIMINAR ARCHIVOS')
    # Eliminar archivos
    filename = '/home/alterego/Downloads/Tercer proyecto nuevo/nuevocambiotecladoubuntu'
    try:
        os.remove(filename)
    except:
        print('No se borro')

    # print('ELIMINAR DIRECTORIOS')
    # Eliminar directorios
    directorio = '/home/alterego/Documents/proyectos/Tercer proyecto'
    try:
        shutil.rmtree(directorio)
    except:
        print('No se borro')

def CrearProyecto(proyecto,directorio,dt,usuario):

    etapa = "CrearProyecto"

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()
    nombre = proyecto.nombre

    # Directorio del proyecto
    CrearDirectorio(directorio + nombre,etapa,nombre,usuario,True)
    # Directorio media
    CrearDirectorio(directorio + nombre + "/media",etapa,nombre,usuario,True)
    # # Directorio media por aplicacion
    # for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
    #     CrearDirectorio(directorio + nombre + "/media/" + aplicacion.nombre,etapa,nombre,True)
    # Directorio del directorio del directorio del proyecto
    CrearDirectorio(directorio + nombre + "/" + nombre,etapa,nombre,usuario,True)
    # Archivo __init__.py debajo del directorio del directorio del proyecto
    CopiarArchivos(dt + "__init__.py", directorio + nombre + "/" + nombre + "/__init__.py",etapa,nombre, usuario,True)
    
    # Archivo settings.py debajo del directorio del directorio del proyecto
    stri = TextFiles.objects.get(file = "settings.py").texto
    # stri = LeerArchivo(dt + "settings.py",etapa,nombre,usuario)
    stri = stri.replace('@proyecto',nombre)

    ProcesoPersonalizacion(proyecto,nombre,'settings.py',directorio + nombre + "/" + nombre + "/",stri,nombre,etapa,usuario)
    # stri = EscribePersonalizacion(proyecto,None,'settings.py',stri)
    # #Sin lineas de personalizacion
    # if not proyecto.conetiquetaspersonalizacion:
    #     stri = QuitaLineasPersonalizacion(stri)

    # EscribirArchivo(directorio + nombre + "/" + nombre + "/settings.py",etapa,nombre,stri,True)

    # Archivo urls.py debajo del directorio del directorio del proyecto
    stri = TextFiles.objects.get(file = "core_urls.py").texto
    CopiarArchivos(dt + "urls.py", directorio + nombre + "/" + nombre + "/urls.py",etapa,nombre, usuario,True)
    # Archivo wsgi.py debajo del directorio del directorio del proyecto
    stri = TextFiles.objects.get(file = "wsgi.py").texto
    # stri = LeerArchivo(dt + "wsgi.py",etapa,nombre,usuario)
    stri = stri.replace('@proyecto',nombre)
    EscribirArchivo(directorio + nombre + "/" + nombre + "/wsgi.py",etapa,nombre,stri,usuario,True)
    # Archivo manage.py debajo del directorio del proyecto
    stri = TextFiles.objects.get(file = "manage.py").texto
    # stri = LeerArchivo(dt + "manage.py",etapa,nombre,usuario)
    stri = stri.replace('@proyecto',nombre)
    EscribirArchivo(directorio + nombre + "/manage.py",etapa,nombre,stri,usuario,True)

def CrearAplicaciones(proyecto,directorio,dt,usuario):

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()

    etapa = "CrearAplicaciones"
    nombre = proyecto.nombre
    
    # Crear en la base de datos la aplicacion core
    try:
        Aplicacion.objects.get(nombre='core', proyecto=proyecto)
    except:
        aplicacion = Aplicacion()
        aplicacion.proyecto = proyecto
        aplicacion.nombre = 'core'
        aplicacion.descripcion = 'Aplicacion de soporte'
        aplicacion.save()
        
    # Crear en la base de datos la aplicacion registration
    try:
        Aplicacion.objects.get(nombre='registration', proyecto=proyecto)
    except:
        aplicacion = Aplicacion()
        aplicacion.proyecto = proyecto
        aplicacion.nombre = 'registration'
        aplicacion.descripcion = 'Aplicacion de seguridad'
        aplicacion.save()
        
    # Variable para la lista de aplicaciones para settings.py
    strLa = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        try:

            # verificar si la aplicacion tiene modelos y estos tienen propiedades
            flgCrear = AplicacionTienePropiedades(aplicacion)
            flgCrear = True
            if flgCrear or aplicacion.nombre == 'core' or aplicacion.nombre == 'registration':

                # No se incluye la aplicacion registration pues esa va primero
                if aplicacion.nombre != 'registration':
                    strLa += "\t'" + aplicacion.nombre + "'," + '\n'

                # Crear el directorio de la aplicacion
                CrearDirectorio(directorio + nombre + "/" + aplicacion.nombre,etapa,nombre,usuario,True)
                # Crear el directorio migrations debajo del directorio de la aplicacion
                CrearDirectorio(directorio + nombre + "/" + aplicacion.nombre + "/migrations",etapa,nombre,usuario,True)
                # Crear directorio  __pycache debajo de migrations para cada aplicacion
                CrearDirectorio(directorio + nombre + "/" + aplicacion.nombre + "/migrations/__pycache__",etapa,nombre,usuario,True)
                # Crear el archivo __init__.py debajo de migrations
                CopiarArchivos(dt + "__init__.py", directorio + nombre + "/" + aplicacion.nombre + "/migrations/__init__.py",etapa,nombre, usuario,True)
                # Crear directorio  templates debajo de cada aplicacion
                CrearDirectorio(directorio + nombre + "/" + aplicacion.nombre + "/templates",etapa,nombre,usuario,True)
                # Crear directorio  con el nombre de la aplicacion debajo de templates
                CrearDirectorio(directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre,etapa,nombre,usuario,True)
                if aplicacion.nombre == 'core':
                    # Crear directorio includes debajo de la aplicacion core
                    CrearDirectorio(directorio + nombre + "/core/templates/core/includes",etapa,nombre,usuario,True)
                    # Copiar en core/includes los dos archivos html para importar los css y js de bootstarp
                    stri = TextFiles.objects.get(file = "css_general.html").texto
                    # stri = LeerArchivo(dt + "css_general.html",etapa,nombre,usuario)

                    ProcesoPersonalizacion(proyecto,aplicacion.nombre,'css_general.html',directorio + nombre + "/core/templates/core/includes/",stri,nombre,etapa,usuario)

                    # stri = EscribePersonalizacion(proyecto,aplicacion,'css_general.html',stri)
                    # #Sin lineas de personalizacion
                    # if not proyecto.conetiquetaspersonalizacion:
                    #     stri = QuitaLineasPersonalizacion(stri)                    
                    # EscribirArchivo(directorio + nombre + "/core/templates/core/includes/css_general.html",etapa,nombre,stri,True)

                    stri = TextFiles.objects.get(file = "js_general.html").texto
                    # stri = LeerArchivo(dt + "js_general.html",etapa,nombre,usuario)

                    ProcesoPersonalizacion(proyecto,aplicacion.nombre,'js_general.html',directorio + nombre + "/core/templates/core/includes/",stri,nombre,etapa,usuario)

                    # stri = EscribePersonalizacion(proyecto,aplicacion,'js_general.html',stri)
                    # #Sin lineas de personalizacion
                    # if not proyecto.conetiquetaspersonalizacion:
                    #     stri = QuitaLineasPersonalizacion(stri)                    
                    # EscribirArchivo(directorio + nombre + "/core/templates/core/includes/js_general.html",etapa,nombre,stri,True)

                    # Crear directorio static debajo de la aplicacion core
                    CrearDirectorio(directorio + nombre + "/core/static",etapa,nombre,usuario,True)
                    # Crear directorio core debajo de la static en core
                    CrearDirectorio(directorio + nombre + "/core/static/core",etapa,nombre,usuario,True)
                    # Crear directorio css debajo de la static/core en core
                    CrearDirectorio(directorio + nombre + "/core/static/core/css",etapa,nombre,usuario,True)
                    # Crear directorio img debajo de la static/core en core
                    CrearDirectorio(directorio + nombre + "/core/static/core/img",etapa,nombre,usuario,True)
                    # Crear directorio js debajo de la static/core en core
                    CrearDirectorio(directorio + nombre + "/core/static/core/js",etapa,nombre,usuario,True)
                    # Copiar los archivos css de bootstrap y animations en css de core/static/css
                    CopiarArchivos(dt + "animation.css", directorio + nombre + "/core/static/core/css/animation.css",etapa,nombre, usuario,True)
                    CopiarArchivos(dt + "bootstrap.css", directorio + nombre + "/core/static/core/css/bootstrap.css",etapa,nombre, usuario,True)
                    CopiarArchivos(dt + "bootstrap.min.css", directorio + nombre + "/core/static/core/css/bootstrap.min.css",etapa,nombre, usuario,True)
                    # Copiar los archivos js de bootstrap, jquery y popper core/static/js
                    CopiarArchivos(dt + "bootstrap.min.js", directorio + nombre + "/core/static/core/js/Bootstrap.min.js",etapa,nombre, usuario,True)
                    CopiarArchivos(dt + "jquery-3.4.1.min.js", directorio + nombre + "/core/static/core/js/jquery-3.4.1.min.js",etapa,nombre, usuario,True)
                    CopiarArchivos(dt + "popper.min.js", directorio + nombre + "/core/static/core/js/popper.min.js",etapa,nombre, usuario,True)
                    CopiarArchivos(dt + "js_propios.js", directorio + nombre + "/core/static/core/js/js_propios.js",etapa,nombre, usuario,True)

        except Exception as e:
            errores = ErroresCreacion()
            errores.etapa = etapa
            errores.paso = "Crear las aplicaciones: "
            errores.proyecto = nombre
            errores.usuario = usuario
            errores.descripcion = e
            errores.save()            

    # Leer el archivo settings.py
    stri = TextFiles.objects.get(file = "settings.py").texto
    # stri = LeerArchivo(dt + "settings.py",etapa,nombre,usuario)
    # modificar archivo settings.py  del proyecto con la lista de los nombres de las aplicaciones
    stri = stri.replace('#@registration', "'" + 'registration' + "',")
    stri = stri.replace('#@aplicaciones', strLa)
    stri = stri.replace('@proyecto', proyecto.nombre)
    # Borrar el archivo settings del directorio proyecto del proyecto
    # BorrarArchivo(directorio + "/" + nombre + "/" + nombre + "/settings.py" ,etapa,nombre)
    # Grabar el nuevo archivo settings
    EscribirArchivo(directorio +"/" + nombre + "/" + nombre + "/settings.py",etapa,nombre,stri,usuario,True)
    # EscribirEnArchivo(directorio +"/" + nombre + "/" + nombre + "/settings.py",stri,etapa,nombre)

    # Crear archivos de aplicaciones
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        # verificar si la aplicacion tiene modelos y estos tienen propiedades
        flgCrear = AplicacionTienePropiedades(aplicacion)
        flgCrear = True
        if flgCrear or aplicacion.nombre == 'core' or aplicacion.nombre == 'registration':
            # Copiar el archivo __init__.py de text files en el directorio de la aplicacion
            CopiarArchivos(dt + "__init__.py",directorio + nombre + "/" + aplicacion.nombre + "/__init__.py",etapa,nombre,usuario,True)

            # Copiar el archivo admin.py de text files en el directorio de la aplicacion
            stri = TextFiles.objects.get(file = "admin.py").texto
            # stri = LeerArchivo(dt + "admin.py",etapa,nombre,usuario)

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'admin.py',directorio + nombre + "/" + aplicacion.nombre + "/",stri,nombre,etapa,usuario)

            # stri = EscribePersonalizacion(proyecto,aplicacion,'admin.py',stri)
            # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     stri = QuitaLineasPersonalizacion(stri)                    
            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/admin.py",etapa,nombre,stri,True)

            # Copiar el archivo apps.py de text files en el directorio de la aplicacion
            CopiarArchivos(dt + "apps.py",directorio + nombre + "/" + aplicacion.nombre + "/apps.py",etapa,nombre,usuario,True)
            # Copiar el archivo models.py de text files en el directorio de la aplicacion
            CopiarArchivos(dt + "models.py",directorio + nombre + "/" + aplicacion.nombre + "/models.py",etapa,nombre,usuario,True)
            # Copiar el archivo test.py de text files en el directorio de la aplicacion
            CopiarArchivos(dt + "tests.py",directorio + nombre + "/" + aplicacion.nombre + "/tests.py",etapa,nombre,usuario,True)
            # # Copiar el archivo views.py de text files en el directorio de la aplicacion
            # CopiarArchivos(dt + "views.py",directorio + nombre + "/" + aplicacion.nombre + "/views.py",etapa,nombre,True)
            # # Copiar el archivo forms.py de text files en el directorio de la aplicacion
            # CopiarArchivos(dt + "forms.py",directorio + nombre + "/" + aplicacion.nombre + "/forms.py",etapa,nombre,True)
            # # Copiar el archivo urls.py de text files en el directorio de la aplicacion
            # CopiarArchivos(dt + "urls.py",directorio + nombre + "/" + aplicacion.nombre + "/urls.py",etapa,nombre,True)

def CrearModelos(proyecto,directorio,dt,usuario):

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()

    nombre = proyecto.nombre
    etapa = "CrearModelos"

    # leer el archivo js
    strjs = TextFiles.objects.get(file = "js_propios.js").texto
    # strjs = LeerArchivo(dt + "js_propios.js",etapa,nombre,usuario)
    # variable para el manejo de los js
    strfjs = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto).order_by('ordengeneracion'):

        # Leer archivo modelo.py de core/text_files
        strTexto = TextFiles.objects.get(file = "modelo.py").texto
        # strTexto = LeerArchivo(dt + "modelo.py",etapa,nombre,usuario)

        # Para cada modelo crear toda su estructura
        strt = ''
        # Variable para los import de los padres de los modelos
        strmf = '' 
        for modelo in Modelo.objects.filter(aplicacion=aplicacion).order_by('ordengeneracion'):

            # actualiza el archivo js

            if modelo.buscadorlista:
                if modelo.padre == 'nada':
                    strfjs +=  '// Funcion que se ejecuta cuando se acciona el boton' + '\n'
                    strfjs +=  '// de busqueda en el html del modelo @modelo' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_01] //' + '\n'
                    strfjs += '$(function(){' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_02] //' + '\n'
                    strfjs += '\tvar enlace = $(' + "'" + '#link-busqueda_@modelo' + "'" + ');' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_03] //' + '\n'
                    strfjs += '\tenlace.on(' + "'" + 'click' + "'" + ',function(){' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_04] //' + '\n'
                    strfjs += '\tvar texto = $(' + "'" + '#textob@modelo' + "'" + ');' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_05] //' + '\n'
                    strfjs += '\tenlace.attr(' + "'" + 'href' + "'" + ',' + "'" + 'http://127.0.0.1:8001/@aplicacion/listar_@modelo?duplica=0&criterio=' + "'" + ' + ' + 'texto.val());' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_06] //' + '\n'
                    strfjs += '});' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_07] //' + '\n'
                    strfjs += '}())' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_08] //' + '\n'

                    strfjs = strfjs.replace('@modelo', modelo.nombre)
                    strfjs = strfjs.replace('@aplicacion', aplicacion.nombre)

            # Varibale para el recorrido de las propiedades del modelo
            strp = ''
            # Variable para el valor inicial de la propiedad
            pi = ''
            # Variable para la primera propiedad de retorno

            # ver si el modelo tiene padre
            if modelo.padre != 'nada':
                if Modelo.objects.get(nombre=modelo.padre,proyecto=proyecto).aplicacion != modelo.aplicacion:

                    modelo_padre = Modelo.objects.get(nombre=modelo.padre,proyecto=proyecto)

                    if strmf.find('from ' + modelo_padre.aplicacion.nombre + '.models import ' +  modelo.padre) == -1:
                        strmf += 'from ' + modelo_padre.aplicacion.nombre + '.models import ' +  modelo.padre + '\n'              

            # recorrer propiedades
            # Definir el estado previo a propiedad usuario
            for propiedad in Propiedad.objects.filter(modelo=modelo):
                if propiedad.tipo == 'u':
                    strp += '\t' + propiedad.nombre + ' =  models.ForeignKey(User,on_delete=models.CASCADE)' + '\n'
                    modelo.crearlogin = True
                    modelo.save()
                    proyecto.conseguridad = True
                    proyecto.save()
                if propiedad.tipo == 's':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = ',default=' + "''"
                        else:
                            pi = ',default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    # strp += '\t' + propiedad.nombre + ' = ' + 'models.CharField(max_length=' + str(propiedad.largostring) + ',default=' + pi + ')' + '\n'
                    strp += '\t' + propiedad.nombre + ' = ' + 'models.CharField(max_length=' + str(propiedad.largostring) + pi + ')' + '\n'
                if propiedad.tipo == 'x':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default =' + "''"
                        else:
                            pi = 'default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' = ' + 'models.TextField(' + pi + ')' + '\n'
                if propiedad.tipo == 'm':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + '0'
                        else:
                            pi = 'default=' + propiedad.valorinicial
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' =  models.SmallIntegerField(' + pi  + ')' + '\n'
                if propiedad.tipo == 'i':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + '0'
                        else:
                            pi = 'default=' + propiedad.valorinicial
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' =  models.IntegerField(' + pi + ')' + '\n'
                if propiedad.tipo == 'l':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + '0'
                        else:
                            pi = 'default=' + propiedad.valorinicial
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' =  models.BigIntegerField(' + pi + ')' + '\n'
                if propiedad.tipo == 'd':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + '0,'
                        else:
                            pi = 'default=' + propiedad.valorinicial + ','
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' =  models.DecimalField(' + pi + 'decimal_places=2,max_digits=10)' + '\n'
                if propiedad.tipo == 'f':
                    strp += '\t' + propiedad.nombre + ' =  models.ForeignKey(' +  propiedad.foranea + ', on_delete=models.CASCADE,' + ' related_name=' + "'" + '%(class)s_@related' + "'" + ')' + '\n'
                    strp = strp.replace('@related', propiedad.nombre)
                    # llenar la variable de modelos foraneos
                    try:
                        modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea , proyecto=proyecto)
                        # print('modelo foraneo ', modelo_foraneo.aplicacion)
                        # print('modelo ', modelo.aplicacion)
                        if modelo_foraneo.aplicacion != modelo.aplicacion:
                            if strmf.find('from ' + modelo_foraneo.aplicacion.nombre + '.models import ' +  propiedad.foranea) == -1:
                                strmf += 'from ' + modelo_foraneo.aplicacion.nombre + '.models import ' +  propiedad.foranea + '\n'  
                        # print('strmf ',strmf)
                    except:
                        pass
                if propiedad.tipo == 't':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + 'timezone.now'
                        else:
                            pi = 'default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' =  models.DateTimeField(' + pi + ')' + '\n'
                if propiedad.tipo == 'e': #TimeField
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + "'00:00'"
                        else:
                            pi = 'default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' = ' + 'models.TimeField(' + pi + ')' + '\n'
                    # strp += '\t' + propiedad.nombre + ' =  models.TimeField(' + pi + ')' + '\n'
                if propiedad.tipo == 'n': #DateField
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + 'timezone.now'
                        else:
                            pi = 'default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' = ' + 'models.DateField(' + pi + ')' + '\n'
                    # strp += '\t' + propiedad.nombre + ' =  models.TimeField(' + pi + ')' + '\n'
                if propiedad.tipo == 'b':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + 'False'
                        else:
                            pi = 'default=' + propiedad.valorinicial
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' =  models.BooleanField(' + pi + ')' + '\n'
                if propiedad.tipo == 'r':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + "''"
                        else:
                            pi = 'default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' = ' + 'models.CharField(max_length=' + str(propiedad.largostring) + ',' + pi + ')' + '\n'
                if propiedad.tipo == 'a':
                    if propiedad.mandatoria == False:
                        if propiedad.valorinicial == '':
                            pi = 'default=' + "''"
                        else:
                            pi = 'default=' + "'" + propiedad.valorinicial + "'"
                    else:
                        pi = ''
                    strp += '\t' + propiedad.nombre + ' = ' + 'models.CharField(max_length=' + str(propiedad.largostring) + ',' + pi + ')' + '\n'
                if propiedad.tipo == 'h':
                    strp += '\t' + propiedad.nombre + ' = ' + 'RichTextField()' + '\n'
                if propiedad.tipo == 'p':
                    strp += '\t' + propiedad.nombre + ' = models.ImageField(upload_to=' + "'" + modelo.nombre + "'" + ',blank=True,null=True)' + '\n'

            if strp != '':
                #ver si el modelo es dependiente
                if modelo.padre != 'nada':
                    strp += '\t' + modelo.padre + ' =  models.ForeignKey(' +  modelo.padre + ', on_delete=models.CASCADE' + ')' + '\n'

                strmodelo = 'class @nombremodelo(models.Model):' + '\n\n'
                strmodelo += '#@[p_propiedades_@nombremodelo_01]' + '\n\n'
                strmodelo += '@propiedades' + '\n'
                strmodelo += '#@[p_propiedades_@nombremodelo_02]' + '\n'
                strmodelo += '\n'
                strmodelo += '\tdef __str__(self):' + '\n'
                strmodelo += '#@[p_self_@nombremodelo_01]' + '\n'
                strmodelo += '\t\treturn @paraself' + '\n' 
                strmodelo += '#@[p_self_@nombremodelo_02]' + '\n'

                strmodelo = strmodelo.replace('@nombremodelo', modelo.nombre)

                strmodelo = strmodelo.replace('@propiedades', strp)
                if modelo.nombreself != '':
                    strmodelo = strmodelo.replace('@paraself', modelo.nombreself)
                else:
                    strself = ''
                    for prop in Propiedad.objects.filter(modelo=modelo):
                        strmodelo = strmodelo.replace('@paraself', 'self.' + prop.nombre)
                        modelo.nombreself = 'self.' + prop.nombre
                        modelo.save()
                        break

                strp = ''

                strt += strmodelo + '\n'

        strTexto = strTexto.replace('@foraneos',  strmf)
        strTexto = strTexto.replace('@modelos', strt)

        # Grabar el modelo si su aplicacion tiene modelos con propiedades

        if AplicacionTienePropiedades(aplicacion):            

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'models.py',directorio + nombre + "/" + aplicacion.nombre + "/",strTexto,nombre,etapa,usuario)

            # strt = EscribePersonalizacion(proyecto,aplicacion,'models.py',strt)
            # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     strTexto = QuitaLineasPersonalizacion(strTexto)

            # # Borrar y escribe el archivo models.py de la aplicacion
            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/models.py",etapa,nombre,strTexto,True)

        # actualiza el archivo js
        strjs = strjs.replace('@busqueda', strfjs)
        # EscribirArchivo(directorio +"/" + nombre + "/core/static/core/js/js_propios.js",etapa,nombre,strjs,usuario,True)

def CrearVistas(proyecto,directorio,dt,usuario):

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()

    nombre = proyecto.nombre
    etapa = "CrearVistas"

    # Para cada modelo
    # strim = ''
    # strif = ''
    strlh = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        if aplicacion.nombre == 'core':
            # Preparar el archivo core_view.py de text files en el directorio de la aplicacion core
            stri = TextFiles.objects.get(file = "core_view.py").texto
            # stri = LeerArchivo(dt + 'core_view.py',etapa,nombre,usuario)
            # Ver las aplicaciones y los modelos
            strap = ''
            for app in Aplicacion.objects.filter(proyecto = proyecto):
                if app.nombre != 'core' and app.nombre != 'registration':
                    strap += "if self.request.GET['aplicacion'] == '@aplicacion':" + "\n"
                    strap = strap.replace('@aplicacion', app.nombre)    
                    for modelo in Modelo.objects.filter(aplicacion = app):
                        strap += "  lista_modelos.append(" + modelo.nombre + ")" + "\n"
            stri = stri.replace('@lista_modelos', strap)

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'views.py',directorio + nombre + "/" + aplicacion.nombre + "/",stri,nombre,etapa,usuario)
            
            # stri = EscribePersonalizacion(proyecto,aplicacion,'views.py',stri)
            # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     stri = QuitaLineasPersonalizacion(stri)     

            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/views.py",etapa,nombre,stri,True)

        strif = ''
        strim = ''
        strmp = ''
        strmh = ''

        # # Copiar el archivo views.py de text files en el directorio de la aplicacion
        # CopiarArchivos(dt + "views.py",directorio + nombre + "/" + aplicacion.nombre + "/views.py",etapa,nombre,True)

        # leer archivo vistas.py de core/text_files
        stri = TextFiles.objects.get(file = "vistas.py").texto
        # stri = LeerArchivo(dt + 'vistas.py',etapa,nombre,usuario)

        strmp = 'class HomeView(TemplateView):' + '\n'
        strmp += '\ttemplate_name = ' + "'" + aplicacion.nombre + '/home.html' + "'" + '\n'
        strmp += '\n'                

        for modelo in Modelo.objects.filter(aplicacion=aplicacion,proyecto=proyecto):

            if modelo.sinbasedatos == False:

                if Propiedad.objects.filter(modelo=modelo).count() > 0:
                    # Lista de import de formularios
                    if strif.find('from .forms import ' + modelo.nombre + 'Form') == -1:
                        strif += 'from .forms import ' + modelo.nombre + 'Form' + '\n'                    #importa modelos
                    if strim.find('from ' +  Aplicacion.objects.get(id=modelo.aplicacion.id).nombre + '.models import ' + modelo.nombre) == -1:
                        strim += 'from ' +  Aplicacion.objects.get(id=modelo.aplicacion.id).nombre + '.models import ' + modelo.nombre + '\n'  

                    if modelo.padre != 'nada': 
                        
                        # Editar modelo hijo
                        strv = '# Este modelo es dependiente de ' + modelo.padre + '\n'
                        strv += '# Vista que es utilizada para la edicion del' + '\n'
                        strv += '# modelo @modelo cuyos registros y se encuentran' + '\n'
                        strv += '# grabados en la Base de Datos' + '\n'
                        strv += 'class Editar@modeloView(UpdateView):' + '\n'
                        strv += '#@[p_editar_' + modelo.nombre + '_01]' + '\n'
                        strv += '\t# El modelo que se edita' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '#@[p_editar_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t# El formulario para la edicion' +'\n'
                        strv += '\tform_class = @modeloForm' + '\n'
                        # strv += '\ttemplate_name_suffix = ' + "'" + '_update_form' + "'"  + '\n'
                        strv += '#@[p_editar_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\t# El HTML que se despliega ante el usuario' + '\n' 
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_update_form.html' + "'"  + '\n'
                        strv += '\n'                
                        strv += '#@[p_editar_' + modelo.nombre + '_04]' + '\n' 
                        strv += '\t# El procedimiento de salida de la edicion' + '\n'
                        strv += '\tdef get_success_url(self):' + '\n'

                        # success de la edicion del modelo hijo o nieto
                        modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada': # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            strv += '\t\t# El modelo @modelo es dependiente' + '\n'
                            strv += '#@[p_editar_success_' + modelo.nombre + '_01]' + '\n' 
                            strv += '\t\t# Despues de editar el modelo se vuelve al HTML de edicion' + '\n' 
                            strv += '\t\t# con el mensaje de actualizacion correcta del registro' + '\n'
                            strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ', args=[self.request.GET[' + "'" +'@modelopadre_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + ' + ' + "'" + '&@modeloabuelo_id=' + "'" + ' + str(self.request.GET[' + "'" + '@modeloabuelo_id' + "'" + '])' + '\n'
                            strv += '#@[p_editar_success_' + modelo.nombre + '_02]' + '\n' 
                            strv = strv.replace('@modeloabuelo', modelo_abuelo.nombre)
                        else: # modelo hijo
                            strv += '\t\t# El modelo @modelo es independiente' + '\n'
                            strv += '#@[p_editar_success_' + modelo.nombre + '_03]' + '\n' 
                            strv += '\t\t# Despues de editar el modelo se vuelve al HTML de edicion' + '\n' 
                            strv += '\t\t# con el mensaje de actualizacion correcta del registro' + '\n'
                            strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ', args=[self.request.GET[' + "'" + '@modelopadre_id' + "'" + ']]) + ' + "'" + '?correcto' + "'"  + '\n'

                        strv += '\n'                
                        strv += '\t# Se preparan los context para enviarlos al HTML de edicion' + '\n'
                        strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        strv += '\t\tcontext = super(Editar@modeloView, self).get_context_data(**kwargs)' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Se recupera el registro de @modelo que se edita' + '\n'
                        strv += '\t\t@modelo = (self.object)' + '\n'
                        strv += '\t\tmodelo = (self.object)' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t\t# Se envian al HTML el id del modelo y su campo que lo identifica' + '\n' 
                        strv += '\t\t# Este campo fue el que se definio como identificador de borrado del modelo' + '\n'
                        strv += '\t\tcontext[' + "'" + '@modelo_id' + "'" + '] = self.object.id' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_03]' + '\n' 
                        # strv += '\t\tcontext[' + "'" + 'nombre' + "'" + '] = @modelo.@paraborrar' + '\n'
                        strv += '\t\tcontext[' + "'" + 'nombre' + "'" + '] = @paraborrar' + '\n'
                        strv += '@listahijos' + '\n'
                        strv += '@idsuperior' + '\n'
                        strv += '@numerohijos' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_04]' + '\n' 
                        # strv += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                        strv += '\t\treturn context' + '\n'

                        # define si existe un numero de registros para los hijos
                        strnh = ''
                        for hijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                            strnh += '# Se envia al HTML el numero de modelos dependientes de @modelo' + '\n' 
                            strnh += '\t\tcontext[' + "'" + 'numero' + hijo.nombre + "'" + '] = ' + hijo.nombre + '.objects.filter(@modelo=@modelo).count()' + '\n'

                        strv = strv.replace('@numerohijos', strnh)

                        strv += '\n'

                        # Crear modelo hijo
                        strv += '# Este modelo es dependiente de ' + modelo.padre + '\n'
                        strv += '# Esta vista es utilizada para el registro de nuevos' + '\n'
                        strv += '# registros del modelo @modelo' + '\n'
                        strv += 'class Crear@modeloView(CreateView):' + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t# Se define el modelo cuyo registro de inserta' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t# El formulario para el nuevo registro' + '\n'
                        strv += '\tform_class = @modeloForm' + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\t# El HTML para el nuevo registro' + '\n'
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_form.html' + "'"  + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_04]' + '\n' 
                        strv += '\n'                
                        strv += '\t# El procedimiento de salida de la insercion' + '\n'
                        strv += '\tdef get_success_url(self):' + '\n'
                        strv += '#@[p_crear_success_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Despues de la insercion del registro, el control' + '\n'
                        strv += '\t\t# retorna al HTML de edicion del modelo padre' + '\n'
                        if modelo_padre.padre != 'nada': # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ', args=[self.request.GET[' + "'" +'@modelopadre_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + ' + ' + "'" + '&@modeloabuelo_id=' + "'" + ' + str(self.request.GET[' + "'" + '@modeloabuelo_id' + "'" + '])' + '\n'
                            strv = strv.replace('@modeloabuelo', modelo_abuelo.nombre)
                        else:
                            strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ', args=[self.request.GET[' + "'" + '@modelopadre_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + '\n'
                        strv += '\n'                
                        strv += '\t# Procedimiento para el clik de insercion' + '\n'
                        strv += '\tdef post(self,request,*args,**kwargs):' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Se recupera el formulario con los controles ya llenos' + '\n'
                        strv += '\t\tform = self.form_class(request.POST)' + '\n'
                        strv += '\t\t# Se recupera el registro del modelo padre ' + '\n'
                        strv += '\t\t@modelopadre_post = @modelopadre.objects.get(id = request.GET[' + "'" + '@modelopadre_id' + "'" + '])' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t\tif form.is_valid():' + '\n'
                        strv += '\t\t# El formulario es valido, no existen incongruencias' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\t\t# Se graba el registro en la base de datos pero ' + '\n'
                        strv += '\t\t# la grabacion se mantiene pendiente, sin commit ' + '\n'
                        strv += '\t\t\t@modelo= form.save(commit=False)' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_03_A]' + '\n' 
                        strv += '\t\t\t# Se asigna a @modelo la dependencia con el modelo padre' + '\n'
                        strv += '\t\t\t@modelo.@modelopadre = @modelopadre_post' + '\n'

                        # Ver si existe una propiedad de tipo usuario
                        prop = ModeloConPropiedadUsuario(modelo)
                        if prop != None:
                            if proyecto.conseguridad:
                                strv += '\t\t\tuser = request.user' + '\n'
                                strv += '#@[p_crear_post_' + modelo.nombre + '_03_B]' + '\n' 
                                strv += '\t\t\t# Se graba en @modelo a propietario del proyecto ' + '\n'
                                strv += '\t\t\t# ya que el modelo se tienen seguridad ' + '\n'
                                strv += '\t\t\t@modelo.' + prop.nombre + ' = user' + '\n'
                                strv += '#@[p_crear_post_' + modelo.nombre + '_03_C]' + '\n' 

                        strv += '\t\t\t# Se graba el registro definitivamente en la base de datos ' + '\n'
                        strv += '\t\t\t@modelo.save()' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_04]' + '\n' 
                        strv += '\t\t\t# Se leva el control al procedimiento de salida por grabacion exitosa' + '\n'
                        strv += '\t\t\treturn HttpResponseRedirect(self.get_success_url())' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_05]' + '\n' 
                        strv += '\t\telse:' + '\n'
                        strv += '#@[p_crear_post_' + modelo.nombre + '_06]' + '\n' 
                        strv += '\t\t\t# Se leva el control al HTML de insercion grabacion no exitosa' + '\n'
                        strv += '\t\t\treturn self.render_to_response(self.get_context_data(form=form))' + '\n'
                        strv += '\n'    

                        # codigo para get_context en Crear
                        strv += '@getcontext'
                        strgc = ''
                        modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada':  # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            strgc = '\t# Se preparan los context para enviarlos al HTML de insercion' + '\n'
                            strgc += '\tdef get_context_data(self,**kwargs):' + '\n'
                            strgc += '#@[p_crear_context_' + modelo.nombre + '_01]' + '\n' 
                            strgc += '\t\tcontext = super(Crear@modeloView, self).get_context_data(**kwargs)' + '\n'
                            strgc += '\t\t# Se recupera el objeto padre y se envia su id' + '\n'
                            strgc += '\t\tobj = @modelopadre.objects.get(id=self.request.GET[' + "'" + '@modelopadre_id' + "'" + '])' + '\n'
                            strgc += '\t\tcontext[' + "'" + '@modelopadre_id' + "'" + '] = obj.id' + '\n'
                            strgc += '\t\t# Se recupera el modelo abuelo y se envia su id' + '\n'
                            strgc += '\t\t@modeloabuelo_@modeloabuelo = @modeloabuelo.objects.get(id=obj.@modeloabuelo.id)' + '\n'
                            strgc += '\t\tcontext[' + "'" + '@modeloabuelo_id' + "'" + '] = @modeloabuelo_@modeloabuelo.id' + '\n'
                            strgc += '#@[p_crear_context_' + modelo.nombre + '_02]' + '\n' 
                            # strgc += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                            strgc += '\t\treturn context' + '\n'
                            strgc = strgc.replace('@modeloabuelo', modelo_abuelo.nombre)
                            if strim.find('from ' +  Aplicacion.objects.get(id=modelo_abuelo.aplicacion.id).nombre + '.models import ' + modelo_abuelo.nombre) == -1:                            
                                strim += 'from ' +  Aplicacion.objects.get(id=modelo_abuelo.aplicacion.id).nombre + '.models import ' + modelo_abuelo.nombre + '\n'  
                        else:
                            strgc += '\tdef get_context_data(self,**kwargs):' + '\n'
                            strgc += '\t\tcontext = super(Crear@modeloView, self).get_context_data(**kwargs)' + '\n'
                            strgc += '#@[p_crear_context_' + modelo.nombre + '_01]' + '\n' 
                            strgc += '\t\t# Se recupera el objeto padre y se envia su id' + '\n'
                            strgc += '\t\tcontext[' + "'" + '@modelopadre_id' + "'" + '] = self.request.GET[' + "'" + '@modelopadre_id' + "'" + ']' + '\n'
                            strgc += '#@[p_crear_context_' + modelo.nombre + '_02]' + '\n' 
                            # strgc += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                            strgc += '\t\treturn context' + '\n'


                        strgc = strgc.replace('@modelopadre', modelo_padre.nombre)

                        strv = strv.replace('@getcontext', strgc)

                        if strim.find('from ' +  Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre + '.models import ' + modelo_padre.nombre) == -1:
                            strim += 'from ' +  Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre + '.models import ' + modelo_padre.nombre + '\n'  
            
                        strv += '\n'            

                        # Borrar modelo hijo
                        strv += '# Este modelo es dependiente de ' + modelo.padre + '\n'
                        strv += '# Esta vista es utilizada para el borrado de' + '\n'
                        strv += '# registros del modelo @modelo' + '\n'
                        strv += 'class Borrar@modeloView(DeleteView):' + '\n'
                        strv += '#@[p_borrar_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t# Se define el modelo a borrar' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '#@[p_borrar_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t# El template HTML para desplegar la opcion de borrado' + '\n'
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_confirm_delete.html' + "'"  + '\n'
                        strv += '#@[p_borrar_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\n'                
                        strv += '\t# El procedimiento de salida del borrado' + '\n'
                        strv += '\tdef get_success_url(self):' + '\n'
                        strv += '#@[p_borrar_success_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# El control vuelve a la edicion del modelo padre' + '\n'
                        strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ', args=[self.request.GET[' + "'" + '@modelopadre_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + '\n'
                        strv += '#@[p_borrar_success_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\n'                
                        strv += '\t# Se preparan los contextos para el HTML de borrado' + '\n'
                        strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        strv += '\t\tcontext = super(Borrar@modeloView, self).get_context_data(**kwargs)' + '\n'
                        strv += '#@[p_borrar_context_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Se recupera el modelo y se envia el nombre definido para el borrado' + '\n'
                        # strv += '\t\t@modelo_borra_@modelo_borra = @modelo.objects.get(id=self.object.id)' + '\n'
                        strv += '\t\t@modelo = @modelo.objects.get(id=self.object.id)' + '\n'
                        # strv += '\t\tcontext[' + "'" + 'nombreborrar' + "'" + '] = @modelo_borra_@modelo_borra.@paraborrar' + '\n'
                        strv += '\t\tcontext[' + "'" + 'nombreborrar' + "'" + '] = @paraborrar' + '\n'
                        strv += '@idsuperior' + '\n'
                        strv += '#@[p_borrar_context_' + modelo.nombre + '_02]' + '\n' 
                        # strv += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                        strv += '\t\treturn context' + '\n'

                        # modelo padre
                        # modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        strv = strv.replace('@modelopadre', modelo_padre.nombre)
                        strv = strv.replace('@modelopadre', modelo_padre.nombre)

                        strv = strv.replace('@modelo', modelo.nombre)
                        strv = strv.replace('@paraself', modelo.nombre + '.' + modelo.nombreself)

                        # aplicacion
                        strv = strv.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)

                        # lista hijos
                        for model in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                            strlh += '\t\t# Se envia al HTML la lista de los modelos dependientes de @modelo' + '\n'
                            strlh += '\t\t' + model.nombre + '_' + model.nombre + ' = ' + model.nombre + '.objects.filter(' + modelo.nombre + ' = ' + modelo.nombre + ')' + '\n'
                            strlh += '#@[p_editar_context_lista_hijos' + modelo.nombre + '_01]' + '\n' 
                            strlh += '\t\t' + 'context[' + "'" + 'lista' + model.nombre + "'" + '] =  ' + model.nombre  + '_' + model.nombre + '\n'
                            strlh += '#@[p_editar_context_lista_hijos' + modelo.nombre + '_02]' + '\n' 
                        strv = strv.replace('@listahijos', strlh)
                        strlh = ''    

                        # define los id superiores
                        stris = ''
                        modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada':  # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            stris += '#@[p_editar_context_padre' + modelo.nombre + '_01]' + '\n' 
                            stris += '\t\tcontext[' + "'" + '@modelopadre_id' + "'" + '] = self.object.@modelopadre.id' + '\n'
                            stris += '\t\t# Se recupera el modelo abuelo y se envia su id' + '\n'
                            stris += '\t\t@modelopadre_@modelopadre = @modelopadre.objects.get(id=self.object.@modelopadre.id)' + '\n'
                            stris += '#@[p_editar_context_padre' + modelo.nombre + '_02]' + '\n' 
                            stris += '\t\tcontext[' + "'" + '@modeloabuelo_id' + "'" + '] = @modelopadre_@modelopadre.@modeloabuelo.id' + '\n'
                            stris = stris.replace('@modeloabuelo', modelo_abuelo.nombre)
                            stris += '#@[p_editar_context_padre' + modelo.nombre + '_03]' + '\n' 
                        else: # modelo hijo
                            stris += '#@[p_editar_context_padre' + modelo.nombre + '_01]' + '\n' 
                            stris += '\t\t# Se recupera el modelo padre y se envia su id' + '\n'
                            stris += '\t\tcontext[' + "'" + '@modelopadre_id' + "'" + '] = self.object.@modelopadre.id' + '\n'
                            stris += '#@[p_editar_context_padre' + modelo.nombre + '_02]' + '\n' 
                        stris = stris.replace('@modelopadre', modelo_padre.nombre)

                        strv = strv.replace('@idsuperior', stris)

                        # Forma la estructura para borrar
                        strv = strv.replace('@paraborrar', ParaBorrar(modelo))
                        # if modelo.nombreborrar != '':
                        #     # separa los componentes
                        #     strpb = modelo.nombreborrar.split("+ '-' + ")
                        #     strpbt = ''
                        #     for strc in strpb:
                        #         if strpbt == '':
                        #             strpbt = 'modelo.' + strc
                        #         else:
                        #             strpbt = '+ ' + "-" + '+' + 'modelo.' + strc
                        #     # strv = strv.replace('@paraborrar', modelo.nombreborrar)
                        #     strv = strv.replace('@paraborrar', strpbt)
                        # else:
                        #     for prop in Propiedad.objects.filter(modelo=modelo):
                        #         strv = strv.replace('@paraborrar', 'modelo.' + prop.nombre)
                        #         modelo.nombreborrar = prop.nombre
                        #         modelo.save()
                        #         break


                        # Encuentra la aplicacion real
                        strv = AplicacionReal(modelo,strv,proyecto)

                        strmh += strv + '\n'
                        strv = ''

                        #importa modelos de padres y abuelos
                        if strim.find('from ' +  Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre + '.models import ' + modelo_padre.nombre) == -1:
                            strim += 'from ' +  Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre + '.models import ' + modelo_padre.nombre + '\n'  

                        if modelo_padre.padre != 'nada': # tiene abuelo
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            if strim.find('from ' +  Aplicacion.objects.get(id=modelo_abuelo.aplicacion.id).nombre + '.models import ' + modelo_abuelo.nombre) == -1:
                                strim += 'from ' +  Aplicacion.objects.get(id=modelo_abuelo.aplicacion.id).nombre + '.models import ' + modelo_abuelo.nombre + '\n'  

                        #importa modelos de hijos
                        for modelo_hijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                            if strim.find('from ' +  Aplicacion.objects.get(id=modelo_hijo.aplicacion.id).nombre + '.models import ' + modelo_hijo.nombre) == -1:
                                strim += 'from ' +  Aplicacion.objects.get(id=modelo_hijo.aplicacion.id).nombre + '.models import ' + modelo_hijo.nombre + '\n'  

                    else: 

                        # modelo padre
                        # strv = 'def Home@modeloView(request):' + '\n'
                        # strv += '\treturn render(request,' + "'" + '@aplicacion/home.html' + "'" + ')' + '\n'
                        # strv += '\n'                
                        # strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        # strv += '#@[p_home_context_' + modelo.nombre + ']' + '\n'
                        # strv += '\t\tcontext = super(Home@modeloView, self).get_context_data(**kwargs)' + '\n'
                        # # strv += '\t\tcontext[' + "'" + 'plantilla' + "'" + '] = ' + "'" + 'encabezado' + "'" + '\n'
                        # strv += '\t\treturn context' + '\n'
                        # strv += '\n'

                        # Listar Modelos Raiz 
                        strv = '# Este modelo es independiente por lo que' + '\n'
                        strv += '# se elabora una lista de sus registros' + '\n'

                        strv += 'class Listar@modeloView(ListView):' + '\n'
                        strv += '#@[p_listar_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t# Definir el modelo a utilizar' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '#@[p_listar_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t# Especificar el template HTML' + '\n'
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_list.html' + "'"  + '\n'
                        strv += '#@[p_listar_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\n'                
                        strv += '\t# Prepara los context para el HTML' + '\n'
                        strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        strv += '#@[p_listar_context_' + modelo.nombre + '_01' + ']' + '\n'
                        strv += '\t\tcontext = super(Listar@modeloView, self).get_context_data(**kwargs)' + '\n'

                        if modelo.buscadorlista:
                            strv += '\t\ttry:' + '\n'
                            strv += '\t\t# La lista tiene un buscador para seleccionar los registros' + '\n'
                            strv += '\t\t# a traves del parametro GET criterio' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_01' + ']' + '\n'
                            strv += '\t\t\tcontext[' + "'" + 'criterio' + "'" + '] = self.request.GET[' + "'" + 'criterio' + "'" + ']' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_02' + ']' + '\n'
                            strv += '\t\t\t# Si criterio es * se buscan todos los registros' + '\n'
                            strv += '\t\t\tif context[' + "'" + 'criterio' + "'" + '] ==' + "'" + '*' + "'" + ':' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_03' + ']' + '\n'
                            strv += '\t\t\t\tcontext[' + "'" + 'lista' + "'" + '] = @modelo.objects.all()' + '\n'
                            strv += '\t\t\t# Si criterio es blaco no se buscan registros' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_04' + ']' + '\n'
                            strv += '\t\t\telif context[' + "'" + 'criterio' + "'" + '] ==' + "'" + "'" + ':' + '\n'
                            strv += '\t\t\t\tcontext[' + "'" + 'lista' + "'" +'] = None' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_05' + ']' + '\n'
                            strv += '\t\t\telse:' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_06' + ']' + '\n'

                            # ver que propiedades se buscan
                            pb = ''
                            for pr in Propiedad.objects.filter(modelo=modelo):
                                if pr.participabusquedalista:
                                    if pb == '':
                                        pb = modelo.nombre + '.objects.filter(' + pr.nombre + '__icontains = context[' + "'" + 'criterio' + "'" + '])' 
                                    else:
                                        pb += '|' + modelo.nombre + '.objects.filter(' + pr.nombre + '__icontains = context[' + "'" + 'criterio' + "'" + '])'
                            strv += '\t\t\t\t# Se busca el criterio en todas las propiedades marcadas para ese fin' + '\n'
                            strv += '\t\t\t\tcontext[' + "'" + 'lista' + "'" + '] = ' + pb + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_07' + ']' + '\n'
                            strv += '\t\texcept:' '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_08' + ']' + '\n'
                            strv += '\t\t\t# En caso de error no se buscan registros' + '\n'
                            strv += '\t\t\tcontext[' + "'" + 'criterio' + "'" + '] = ' + "'" + "'" + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_09' + ']' + '\n'
                        else:
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_10' + ']' + '\n'
                            strv += '\t\tcontext[' + "'" + 'lista' + "'" + '] = @modelo.objects.all()' + '\n'
                            strv += '#@[p_buscador_lista_' + modelo.nombre + '_11' + ']' + '\n'


                        # strv += '\t\tcontext[' + "'" + 'plantilla' + "'" + '] = ' + "'" + 'lista' + "'" + '\n'
                        strv += '#@[p_listar_context_' + modelo.nombre + '_02' + ']' + '\n'
                        # strv += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                        strv += '\t\treturn context' + '\n'
                        strv += '\n'         

                        # Editar Modelos Raiz
                        strv += '# Este modelo es independiente y esta vista' + '\n'
                        strv += '# es la utilizada para la edicion de un registro' + '\n'
                        strv += '# ya grabado en la Base de Datos' + '\n'

                        strv += 'class Editar@modeloView(UpdateView):' + '\n'
                        strv += '#@[p_editar_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t# Define el modelo' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '\t# Define el formulario' + '\n'
                        strv += '\tform_class = @modeloForm' + '\n'
                        # strv += '\ttemplate_name_suffix = ' + "'" + '_update_form' + "'"  + '\n'
                        strv += '#@[p_editar_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t# Define el HTML de edicion' + '\n'
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_update_form.html' + "'"  + '\n'
                        strv += '#@[p_editar_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\n'                
                        strv += '\t# Procedimiento de salida despues de actualizacion exitosa' + '\n'
                        strv += '\tdef get_success_url(self):' + '\n'
                        strv += '#@[p_editar_success_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Retorna al HTML de edicion con la comunicacion de correcta actualizacion' + '\n'
                        strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacion:editar_@modelo' + "'" + ', args=[self.object.id]) + ' + "'" + '?correcto' + "'"  + '\n'
                        strv += '\n'                
                        strv += '\t# Prepara los context para el HTML de edicion' + '\n'
                        strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\tcontext = super(Editar@modeloView, self).get_context_data(**kwargs)' + '\n'
                        strv += '\t\t# Recupera el modelo a ser editado y envia su id' + '\n'
                        strv += '\t\t@modelo = (self.object)' + '\n'
                        strv += '\t\tmodelo = (self.object)' + '\n'
                        strv += '\t\tcontext[' + "'" + '@modelo_id' + "'" + '] = self.object.id' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_02]' + '\n' 
                        strv += '@listahijos' + '\n'
                        strv += '#@[p_editar_context_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\t\t# Envia el context con la identificacion que se dio al borrado' + '\n'
                        # strv += '\t\tcontext[' + "'" + 'nombre' + "'" + '] = @modelo.@paraborrar' + '\n'
                        strv += '\t\tcontext[' + "'" + 'nombre' + "'" + '] = @paraborrar' + '\n'
                        # strv += '\t\tcontext[' + "'" + 'plantilla' + "'" + '] = ' + "'" + 'update' + "'" + '\n'

                        # define si existe un numero de registros para los hijos
                        for hijo in Modelo.objects.filter(padre=modelo.nombre, proyecto=proyecto ):
                            strv += '\t\t# Envia el cotext con el numero de modelos dependientes' + '\n'
                            strv += '\t\tcontext[' + "'" + 'numero' + hijo.nombre + "'" + '] = ' + hijo.nombre + '.objects.filter(@modelo=@modelo).count()' + '\n'

                        # strv += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                        strv += '\t\treturn context' + '\n'
                        strv += '\n'         

                        # Crear Modelos Raiz 
                        strv += '# Este modelo es independiente y esta vista' + '\n'
                        strv += '# es la utilizada para la insercion de un nuevo registro' + '\n'
                        strv += '# en la Base de Datos' + '\n'
                        strv += 'class Crear@modeloView(CreateView):' + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t# Define el modelo cuyo registro se inserta' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '\t# Define el formulario de controles' + '\n'
                        strv += '\tform_class = @modeloForm' + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t# Define el HTML de insercion' + '\n'
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_form.html' + "'"  + '\n'
                        strv += '#@[p_crear_' + modelo.nombre + '_03]' + '\n' 
                        # strv += '\tsuccess_url = reverse_lazy(' + "'" + '@aplicacion:listar_@modelo' + "'" + ')' + '\n'
                        strv += '\n'                
                        strv += '\t# Procedimiento de retorno por insercion exitosa' + '\n'
                        strv += '\tdef get_success_url(self):' + '\n'
                        strv += '#@[p_crear_success_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Retorna al HTML de la lista de registros del modelo' + '\n'
                        strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacion:listar_@modelo' + "'" + ') + ' + "'" + '?correcto' + "'"  + '\n'
                        strv += '\t# Prepara los context de insercion' + '\n'
                        strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        strv += '#@[p_crear_success' + modelo.nombre + '_02]' + '\n' 
                        strv += '\t\tcontext = super(Crear@modeloView, self).get_context_data(**kwargs)' + '\n'
                        # strv += '\t\tcontext[' + "'" + 'plantilla' + "'" + '] = ' + "'" + 'nuevo' + "'" + '\n'
                        strv += '#@[p_crear_success' + modelo.nombre + '_03]' + '\n' 
                        # strv += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                        strv += '\t\treturn context' + '\n'

                        # El modelo tiene una propiedad tipo usuario
                        strp = ''
                        prop = ModeloConPropiedadUsuario(modelo)
                        if prop != None:
                            if proyecto.conseguridad:
                                # strp = LeerArchivo(dt + 'post_usuario.html',etapa,nombre,usuario)
                                strp = '\t# El modelo fue definido con la opcion de seguridad' + '\n'
                                strp += '\tdef post(self,request,*args,**kwargs):' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_01]' + '\n' 
                                strp += '\t\t# Recupera el formulario con el nuevo registro del modelo' + '\n'
                                strp += '\t\tform = self.form_class(request.POST,request.FILES)' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_02]' + '\n' 
                                strp += '\t\t# Recupera el usuario' + '\n'
                                strp += '\t\tuser = request.user' + '\n'

                                strp += '#@[p_crear_post_' + modelo.nombre + '_03]' + '\n' 
                                strp += '\t\tif form.is_valid():' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_04]' + '\n' 
                                strp += '\t\t\t# Prepara al modelo para grabacion pero sin commit' + '\n'
                                strp += '\t\t\t@modelo = form.save(commit=False)' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_05]' + '\n' 
                                strp += '\t\t\t# Asigna al registro el campo de usuario' + '\n'
                                strp += '\t\t\t@modelo.@propiedad = user' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_06]' + '\n' 
                                strp += '\t\t\t# Graba el registro definitivamente en la base de datos' + '\n'
                                strp += '\t\t\t@modelo.save()' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_07]' + '\n' 
                                strp += '\t\t\t# Envia el control al procedimiento de inserecion exitosa' + '\n'
                                strp += '\t\t\treturn HttpResponseRedirect(self.get_success_url())' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_08]' + '\n' 
                                strp += '\t\t# Envia el control nuevamente al HTML de insercion' + '\n'
                                strp += '\t\treturn render(request, ' + "'" + '@aplicacion/@modelo_form.html' + "'" + ', {' + "'" + 'form' + "'" + ': form})' + '\n'
                                strp += '#@[p_crear_post_' + modelo.nombre + '_09]' + '\n' 

                                strp = strp.replace('@modelo',modelo.nombre)
                                strp = strp.replace('@aplicacion',aplicacion.nombre)
                                strp = strp.replace('@propiedad',prop.nombre)
                        strv += strp

                        strv += '\n'        

                        # Borrar Modelos Raiz 
                        strv += '# Este modelo es independiente y esta vista' + '\n'
                        strv += '# es la utilizada para el borrado de un registro' + '\n'
                        strv += '# ya grabado en la Base de Datos' + '\n'
                        strv += 'class Borrar@modeloView(DeleteView):' + '\n'
                        strv += '#@[p_borrar_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t# Define le modelo a borrar' + '\n'
                        strv += '\tmodel = @modelo' + '\n'
                        strv += '#@[p_borrar_' + modelo.nombre + '_02]' + '\n' 
                        # strv += '\tsuccess_url = reverse_lazy(' + "'" + '@aplicacion:listar_@modelo' + "'" + ')' + '\n'
                        strv += '\t# Define el HTML de borrado' + '\n'
                        strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_confirm_delete.html' + "'"  + '\n'
                        strv += '#@[p_borrar_' + modelo.nombre + '_03]' + '\n' 
                        strv += '\n'                
                        strv += '\t# Procedimiento de retorno por borrado exitoso' + '\n'
                        strv += '\tdef get_success_url(self):' + '\n'
                        strv += '#@[p_borrar_success_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\t# Retorna al HTML de lista de registros del modelo' + '\n'
                        strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacion:listar_@modelo' + "'" + ') + ' + "'" + '?correcto' + "'"  + '\n'
                        strv += '\t# Prepara los context de borrado' + '\n'
                        strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                        strv += '#@[p_borrar_context_' + modelo.nombre + '_01]' + '\n' 
                        strv += '\t\tcontext = super(Borrar@modeloView, self).get_context_data(**kwargs)' + '\n'
                        strv += '\t\t# Recupera el modelo a borrar y envia su id' + '\n'
                        # strv += '\t\t@modelo_borra_@modelo_borra = @modelo.objects.get(id=self.object.id)' + '\n'
                        strv += '\t\tmodelo = @modelo.objects.get(id=self.object.id)' + '\n'
                        # strv += '\t\tcontext[' + "'" + 'nombreborrar' + "'" + '] = @modelo_borra_@modelo_borra.@paraborrar' + '\n'
                        strv += '\t\tcontext[' + "'" + 'nombreborrar' + "'" + '] = @paraborrar' + '\n'
                        strv += '#@[p_borrar_context_' + modelo.nombre + '_02]' + '\n' 
                        # strv += '\t\tcontext[' + "'" + 'opcion_menu' + "'" + '] = self.request.GET[' + "'" + 'opcion_menu' + "'" + ']' + '\n'
                        strv += '\t\treturn context' + '\n\n'

# Reporte antiguo

                        # # Impresion de la lista
                        # strr = LeerArchivo(dt + 'modelo_reporte_antiguo.py',etapa,nombre,usuario)
                        # strr = strr.replace("@modelo",modelo.nombre)
                        # strr = strr.replace("@aplicacion",aplicacion.nombre)
                        # strr = strr.replace("@proyecto",proyecto.nombre)
                        # strr = strr.replace("@titulolista",modelo.titulolista)

                        # if modelo.reportsize == 'L':
                        #     strr = strr.replace("@size",'letter')
                        # else:
                        #     strr = strr.replace("@size",'A4')
                            
                        # if modelo.reportorientation == 'L':
                        #     strr = strr.replace("@orientacion",'landscape')
                        # else:
                        #     strr = strr.replace("@orientacion",'portrait')
                            
                        # # lee la configuarcion del reporte
                        # reporte = Reporte.objects.get(reportesize=modelo.reportsize,orientacion=modelo.reportorientation)

                        # strr = strr.replace("@logox",str(reporte.logox))
                        # strr = strr.replace("@logoy",str(reporte.logoy))
                        # strr = strr.replace("@nombrex",str(reporte.nombrex))
                        # strr = strr.replace("@nombrey",str(reporte.nombrey))
                        # strr = strr.replace("@lineaencabezadox",str(reporte.lineaencabezadox))
                        # strr = strr.replace("@lineaencabezadoy",str(reporte.lineaencabezadoy))
                        # strr = strr.replace("@titulox",str(reporte.titulox))
                        # strr = strr.replace("@tituloy",str(reporte.tituloy))
                        # strr = strr.replace("@fechax",str(reporte.fechax))
                        # strr = strr.replace("@fechay",str(reporte.fechay))
                        # strr = strr.replace("@lineacolumnasx",str(reporte.lineacolumnasx))
                        # strr = strr.replace("@lineacolumnasy",str(reporte.lineacolumnasy))
                        # strr = strr.replace("@lineacolumnaix",str(reporte.lineacolumnaix))
                        # strr = strr.replace("@lineacolumnaiy",str(reporte.lineacolumnaiy))
                        # # strr = strr.replace("@nombrecolumnay",str(reporte.nombrecolumnay))
                        # strr = strr.replace("@lineapiex",str(reporte.lineapiex))
                        # strr = strr.replace("@lineapiey",str(reporte.lineapiey))
                        # strr = strr.replace("@pagenumberx",str(reporte.pagenumberx))
                        # strr = strr.replace("@pagenumbery",str(reporte.pagenumbery))
                        # strr = strr.replace("@numerolineaspp",str(reporte.numerolineaspp))
                        # strr = strr.replace("@numerolineassp",str(reporte.numerolineassp))
                        # strr = strr.replace("@primeralineapp",str(reporte.primeralineapp))
                        # strr = strr.replace("@primeralineasp",str(reporte.primeralineasp))

                        # # campos y columnas
                        # campos = ''
                        # columnas = ''
                        # posi = 1.5
                        # delta = 0
                        # for pr in Propiedad.objects.filter(modelo=modelo):
                        #     if pr.enreporte:
                        #         columnas += '        self.canvas.drawString(@pos*cm,@nombrey*cm,"@nombre")' + '\n'
                        #         campos += '            self.canvas.drawString(@pos*cm,primeralinea*cm-salto*cm,str(obj.@pr))' + '\n'
                        #         columnas = columnas.replace('@pos',str(posi + delta))
                        #         campos = campos.replace('@pos',str(posi + delta))
                        #         campos = campos.replace('@pr',pr.nombre)
                        #         columnas = columnas.replace('@nombrey',str(reporte.nombrecolumnasy))
                        #         columnas = columnas.replace('@nombre',str(pr.textocolumna))
                        #         delta += pr.anchoenreporte
                        # strr = strr.replace('@campos',campos)
                        # strr = strr.replace('@columnas',columnas)

                        # strv += strr

                        # strv += '# Vista para la creacion del listado en PDF de los registros del modelo' + '\n'
                        # strv += 'def Reporte@modeloView(request):' + '\n'
                        # strv += '\tplan = Reporte@modelo("@modelo.pdf")' + '\n'
                        # strv += '\tplan.encabezado()' + '\n'
                        # strv += '\tplan.columnas()' + '\n'
                        # strv += '\tplan.pie()' + '\n'
                        # strv += '\tplan.detalle()' + '\n'
                        # strv += '\tplan.grabar()' + '\n'
                        # strv += '\treturn HttpResponseRedirect(' + "'" + '/@aplicacion/listar_@modelo' + "'" + ')' + '\n'

                        # strv = strv.replace('@aplicacionreal',aplicacion.nombre)
                        # strv = strv.replace('@aplicacion', aplicacion.nombre)
                        # strv = strv.replace('@modelo', modelo.nombre)
# Reporte antiguo 

# Reporte nuevo

                        # Reporte escalonado
                        # print('reporte1',reporte)
                        strr = TextFiles.objects.get(file = "modelo_reporte_escalonado.py").texto
                        # strr = LeerArchivo(dt + 'modelo_reporte_escalonado.py',etapa,nombre,usuario)
                        strr = strr.replace("@modelo",modelo.nombre)
                        strr = strr.replace("@aplicacion",aplicacion.nombre)

                        if modelo.reportsize == 'L':
                            strr = strr.replace("@size",'letter')
                        else:
                            strr = strr.replace("@size",'A4')
                        # print('reporte2',reporte)
                            
                        if modelo.reportorientation == 'L':
                            strr = strr.replace("@orientacion",'landscape')
                        else:
                            strr = strr.replace("@orientacion",'portrait')

                        # # lee la configuarcion del reporte
                        reporte = ReporteNuevo.objects.get(reportesize=modelo.reportsize,orientacion=modelo.reportorientation)
                        # # lee la configuarcion del reporte
                        # reporte = Reporte.objects.get(reportesize=modelo.reportsize,orientacion=modelo.reportorientation)
                        lista = []
                        listatitulos = []
                        listatotales = []
                        RecursivoReporte(lista,listatitulos,listatotales,modelo,1,proyecto,reporte)
                        strRec = ''
                        for txt in listatitulos:
                            strRec += txt
                        strr = strr.replace('@controltitulos',strRec)
                        strRec = ''
                        for txt in lista:
                            strRec += txt
                        strr = strr.replace('@recorrido',strRec)
                        strRec = ''
                        for txt in listatotales:
                            strRec += txt
                        strr = strr.replace('@totales',strRec)
                        # Impresion de la lista
                        # strr = LeerArchivo(dt + 'modelo_reporte_list.py',etapa,nombre,usuario)
                        strr = strr.replace("@primeralinea",str(reporte.primeralinea))
                        strr = strr.replace("@maxlineas",str(reporte.maxlineas))

                        # strr = strr.replace("@modelo",modelo.nombre)
                        # strr = strr.replace("@aplicacion",aplicacion.nombre)
                        # strr = strr.replace("@proyecto",proyecto.nombre)
                        # strr = strr.replace("@titulo",modelo.titulolista)
                        # strr = strr.replace("@titulox",modelo.titulox)
                        # strr = strr.replace("@lineaix",modelo.lineaix)
                        # strr = strr.replace("@lineafx",modelo.lineafx)
                        # strr = strr.replace("@grosorlineacolumna",modelo.grosorlinea)

                        # if modelo.reportsize == 'L':
                        #     strr = strr.replace("@size",'letter')
                        # else:
                        #     strr = strr.replace("@size",'A4')
                            
                        # if modelo.reportorientation == 'L':
                        #     strr = strr.replace("@orientacion",'landscape')
                        # else:
                        #     strr = strr.replace("@orientacion",'portrait')
                            
                        # lee la configuarcion del reporte
                        # reporte = Reporte.objects.get(reportesize=modelo.reportsize,orientacion=modelo.reportorientation)

                        # strr = strr.replace("@logox",str(reporte.logox))
                        # strr = strr.replace("@logoy",str(reporte.logoy))
                        # strr = strr.replace("@nombrex",str(reporte.nombrex))
                        # strr = strr.replace("@nombrey",str(reporte.nombrey))
                        # strr = strr.replace("@lineaencabezadox",str(reporte.lineaencabezadox))
                        # strr = strr.replace("@lineaencabezadoy",str(reporte.lineaencabezadoy))
                        # strr = strr.replace("@titulox",str(reporte.titulox))
                        # strr = strr.replace("@tituloy",str(reporte.tituloy))
                        # strr = strr.replace("@fechax",str(reporte.fechax))
                        # strr = strr.replace("@fechay",str(reporte.fechay))
                        # strr = strr.replace("@lineacolumnasx",str(reporte.lineacolumnasx))
                        # strr = strr.replace("@lineacolumnasy",str(reporte.lineacolumnasy))
                        # strr = strr.replace("@lineacolumnaix",str(reporte.lineacolumnaix))
                        # strr = strr.replace("@lineacolumnaiy",str(reporte.lineacolumnaiy))
                        # # strr = strr.replace("@nombrecolumnay",str(reporte.nombrecolumnay))
                        # strr = strr.replace("@lineapiex",str(reporte.lineapiex))
                        # strr = strr.replace("@lineapiey",str(reporte.lineapiey))
                        # strr = strr.replace("@pagenumberx",str(reporte.pagenumberx))
                        # strr = strr.replace("@pagenumbery",str(reporte.pagenumbery))
                        # strr = strr.replace("@numerolineaspp",str(reporte.numerolineaspp))
                        # strr = strr.replace("@numerolineassp",str(reporte.numerolineassp))
                        # strr = strr.replace("@primeralineapp",str(reporte.primeralineapp))
                        # strr = strr.replace("@primeralineasp",str(reporte.primeralineasp))

                        # # campos y columnas
                        # campos = ''
                        # columnas = ''
                        # posi = 1.5
                        # delta = 0
                        # for pr in Propiedad.objects.filter(modelo=modelo):
                        #     if pr.enreporte:
                        #         columnas += '        self.canvas.drawString(@pos*cm,@nombrey*cm,"@nombre")' + '\n'
                        #         campos += '            self.canvas.drawString(@pos*cm,primeralinea*cm-salto*cm,str(obj.@pr))' + '\n'
                        #         columnas = columnas.replace('@pos',str(posi + delta))
                        #         campos = campos.replace('@pos',str(posi + delta))
                        #         campos = campos.replace('@pr',pr.nombre)
                        #         columnas = columnas.replace('@nombrey',str(reporte.nombrecolumnasy))
                        #         columnas = columnas.replace('@nombre',str(pr.textocolumna))
                        #         delta += pr.anchoenreporte
                        # strr = strr.replace('@campos',campos)
                        # strr = strr.replace('@columnas',columnas)

                        strv += strr

                        # strv += '# Vista para la creacion del listado en PDF de los registros del modelo' + '\n'
                        # strv += 'def Reporte@modeloView(request):' + '\n'
                        # strv += '\tplan = Reporte@modelo("@modelo.pdf")' + '\n'
                        # strv += '\tplan.encabezado()' + '\n'
                        # strv += '\tplan.columnas()' + '\n'
                        # strv += '\tplan.pie()' + '\n'
                        # strv += '\tplan.detalle()' + '\n'
                        # strv += '\tplan.grabar()' + '\n'
                        # strv += '\treturn HttpResponseRedirect(' + "'" + '/@aplicacion/listar_@modelo' + "'" + ')' + '\n'

                        strv = strv.replace('@aplicacionreal',aplicacion.nombre)
                        strv = strv.replace('@aplicacion', aplicacion.nombre)
                        strv = strv.replace('@modelo', modelo.nombre)

# Reporte nuevo

                        strv = strv.replace('@paraborrar', ParaBorrar(modelo))
                        
                        # if modelo.nombreborrar != '':
                        #     strv = strv.replace('@paraborrar', modelo.nombreborrar)
                        # else:
                        #     for prop in Propiedad.objects.filter(modelo=modelo):
                        #         strv = strv.replace('@paraborrar', prop.nombre)
                        #         modelo.nombreborrar = prop.nombre
                        #         modelo.save()
                        #         break

                        #importa modelos de hijos
                        for modelo_hijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                            if strim.find('from ' +  Aplicacion.objects.get(id=modelo_hijo.aplicacion.id).nombre + '.models import ' + modelo_hijo.nombre) == -1:
                                strim += 'from ' +  Aplicacion.objects.get(id=modelo_hijo.aplicacion.id).nombre + '.models import ' + modelo_hijo.nombre + '\n'  

                        # lista hijos
                        for model in Modelo.objects.filter(padre=modelo.nombre  , proyecto=proyecto):
                            strlh += '\t\t' + model.nombre + '_lista = ' + model.nombre + '.objects.filter(' + modelo.nombre + ' = ' + modelo.nombre + ')' + '\n'
                            strlh += '\t\t' + 'context[' + "'" + 'lista' + model.nombre + "'" + '] =  ' + model.nombre  + '_lista' + '\n'
                        strv = strv.replace('@listahijos', strlh)
                        strlh = ''    

                        strmp += strv + '\n'
                        strv = ''
            else:

                # Lista de import de formularios
                strif += '# Importa la libreria forms' + '\n'
                if strif.find('from .forms import ' + modelo.nombre + 'Form') == -1:
                    strif += 'from .forms import ' + modelo.nombre + 'Form' + '\n'

                strv += '#@[p_@modelo_sinbase_01]' + '\n'
                # strv+= 'class home@modeloView(TemplateView):' + '\n'
                # strv += '#@[p_@modelo_home_01]' + '\n'
                # strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_home.html' + "'"  + '\n'
                # strv += '#@[p_@modelo_home_02]' + '\n\n'
                strv += '# Define la unica vista para el modelo que no se graba en la Base de Datos' + '\n'
                strv += 'class @modeloView(FormView):' + '\n'
                strv += '#@[p_@modelo_view_01]' + '\n'
                strv += '\t# Define el HTML que despliega los controles' + '\n'
                strv += '\ttemplate_name = ' + "'" + '@aplicacion/@modelo_sinbase.html' + "'" + '\n'
                strv += '\t# Define el formulario de los controles' + '\n'
                strv += '\tform_class = @modeloForm' + '\n'
                strv += '#@[p_@modelo_view_02]' + '\n'
                strv += '\t# Procedimiento de retorno' + '\n'
                strv += '\tdef get_success_url(self):' + '\n'
                strv += '#@[p_@modelo_success_01]' + '\n'
                strv += '\t\t# Retorna al encabezado el proyecto' + '\n'
                strv += '\t\treturn reverse_lazy(' + "'" + 'core:home' + "'" + ')' + '\n'
                strv += '#@[p_@modelo_success_02]' + '\n'
                # strv += '\tdef post(self,request,*args,**kwargs):' + '\n'
                # strv += '#@[p_@modelo_post_01]' + '\n'
                # strv += '\t\tform = self.form_class(request.POST,request.FILES)' + '\n'
                # strv += '#@[p_@modelo_post_02]' + '\n'
                # strv += '\t\tif form.is_valid():' + '\n'
                # strv += '#@[p_@modelo_post_03]' + '\n'
                # strv += '\t\t\tcleaned_data = form.cleaned_data' + '\n'
                # strv += '#@[p_@modelo_post_04]' + '\n'
                # strv += '\t\treturn render(request, ' + "'" + '@aplicacion/@modelo_sinbase.html' + "'" + ', {' + "'" + 'form' + "'" + ': form})' + '\n'
                # strv += '#@[p_@modelo_sinbase_02]' + '\n'

                strv = strv.replace('@modelo', modelo.nombre)
                strv = strv.replace('@aplicacion',aplicacion.nombre)

                strmp += strv + '\n'
                strv = ''
            
        # reemplazar modeloshijo y padre

        strim = strim + '\n' + '#@[p_importmodelos_02]\n\n'
        strif = strif + '\n' + '#@[p_importforms_02]\n\n'
        strmp = strmp + '\n' + '#@[p_modelospadre_02]\n\n'
        strmh = strmh + '\n' + '#@[p_modeloshijo_02]\n\n'
        
        stri = stri.replace('@importmodelos', strim)
        stri = stri.replace('@importforms', strif)
        stri = stri.replace('@modelospadre', strmp)
        stri = stri.replace('@modeloshijo', strmh)
        stri = stri.replace('@aplicacion', aplicacion.nombre)

        # Reportes
        try:
            stri = stri.replace("@anchologo",str(reporte.anchologo))
            stri = stri.replace("@altologo",str(reporte.altologo))
            stri = stri.replace("@posxlogo",str(reporte.posxlogo))
            stri = stri.replace("@posylogo",str(reporte.posylogo))
            stri = stri.replace("@posxnombre",str(reporte.posxnombre))
            stri = stri.replace("@posynombre",str(reporte.posynombre))
            stri = stri.replace("@iniciolineax",str(reporte.iniciolineax))
            stri = stri.replace("@finallineax",str(reporte.finallineax))
            stri = stri.replace("@iniciolineay",str(reporte.iniciolineay))
            stri = stri.replace("@grosorlineaencabezado",str(reporte.grosorlinea))
            stri = stri.replace("@piex",str(reporte.piex))
            stri = stri.replace("@piey",str(reporte.piey))
            stri = stri.replace("@lineapiex",str(reporte.lineapiex))
            stri = stri.replace("@lineapiey",str(reporte.lineapiey))
            stri = stri.replace("@nombre",proyecto.nombre)

        except:
            pass

        strif = ''
        strmp = ''
        # stri = stri.split('\n')
        # strt= ''
        # for strl in stri:
        #     strt += strl + '\n'

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        if AplicacionTienePropiedades(aplicacion):

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'views.py',directorio + nombre + "/" + aplicacion.nombre + "/",stri,nombre,etapa,usuario)

            # stri = EscribePersonalizacion(proyecto,aplicacion,'views.py',stri)

            # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     stri = QuitaLineasPersonalizacion(stri)
            
            # # Grabar el archivo views.py para cada aplicacion
            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/views.py",etapa,nombre,stri,True)

    # Manejo de las vistas de los modelos hijos que son foreign en otros modelos select
    strVista = '#@[p_load_@modelos_01]' + '\n' 
    strVista += "def load_@modelos(request):" + '\n'
    strVista += "\tidp = request.GET.get('@padre')" + '\n'
    strVista += "\tpadre = @padre.objects.get(id=idp)" + '\n'
    strVista += "\t@modelos = @modelo.objects.filter(@padre=padre).order_by('@propiedad')" + '\n'
    strVista += "\treturn render(request, '@aplicacion/load_@modelo.html', {'@modelos': @modelos})" + '\n'
    strVista += '#@[p_load_@modelos_02]' + '\n' 

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        strLoadHijos = ''
        strForeign = ''
        strh = ''
        if aplicacion.nombre != 'core' and aplicacion.nombre != 'registration':# and aplicacion.nombre == 'generales':
            strh = LeerArchivoEnTexto(directorio + nombre + '/' + aplicacion.nombre + '/views.py',etapa,nombre,usuario)
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                for propiedad in Propiedad.objects.filter(modelo=modelo):
                    if propiedad.tipo == 'f':
                        modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea,proyecto=proyecto)
                        if strh.find('from ' + modelo_foraneo.aplicacion.nombre + '.models import ' + modelo_foraneo.nombre) == -1:
                            strForeign += 'from ' + modelo_foraneo.aplicacion.nombre + '.models import ' + modelo_foraneo.nombre + '\n'
                        if modelo_foraneo.padre !='nada':
                            # Ver si el padre esta en el mismo modelo
                            for modelo_padre in Modelo.objects.filter(proyecto=proyecto):
                                if modelo_padre.nombre == modelo_foraneo.padre:
                                    # Existe el modelo padre la llave foranea
                                    # Crear el url para la lista de modelos hijo
                                    strLoadHijos += strVista
                                    strLoadHijos = strLoadHijos.replace('@modelo',modelo_foraneo.nombre)
                                    strLoadHijos = strLoadHijos.replace('@padre',modelo_padre.nombre)
                                    strLoadHijos = strLoadHijos.replace('@aplicacion',modelo.aplicacion.nombre)
                                    strLoadHijos = strLoadHijos.replace('@propiedad',modelo_foraneo.nombreborrar)
                                    break
        if AplicacionTienePropiedades(aplicacion):
            # Leer el html de insercion y update del modelo con llaves foraneas
            strh = strh.replace('@importforeign',strForeign)
            strh = strh.replace('@loadhijos',strLoadHijos)
            strForeign = ''
            strLoadHijos = ''
            EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + '/views.py',etapa,nombre,strh,usuario,True)

def ParaBorrar(modelo):
    if modelo.nombreborrar != '':
        # separa los componentes
        strpb = modelo.nombreborrar.split("+ '-' + ")
        strpbt = ''
        for strc in strpb:
            if strpbt == '':
                strpbt = 'str(modelo.' + strc + ')'
            else:
                strpbt += '+ ' + "'" + "-" + "'" + ' + ' + 'str(modelo.' + strc + ')'
        # strv = strv.replace('@paraborrar', modelo.nombreborrar)
    else:
        for prop in Propiedad.objects.filter(modelo=modelo):
            strpbt = 'modelo.' + prop.nombre
            modelo.nombreborrar = prop.nombre
            modelo.save()
            break
    return strpbt

def RecursivoReporte(lista,listatitulos,listatotales,modelo,nivel,proyecto,reporte,lineaix=0, datosix=0, titulox=0,padre=''):
    name = 'John'
    esp = ' ' * nivel

    if nivel == 1:
        lineaix = modelo.lineaix
        datosix = modelo.datoinicialx
        titulox = modelo.titulox

    tab = '    ' * nivel
    dostab = '    ' * (nivel+1)
    trestab = '    ' * (nivel+2)

    listatitulos.append('    primer_' + modelo.nombre + ' = True\n')

    strr = ''

    # Titulo
    strp = ''
    delta = 0
    pos = 1
    identa = 0

    if modelo.identacionautomatica and nivel>1:
        identa  = (nivel-1)

    if padre == '':
        padre = modelo.nombre
        strr += tab + 'for reg_@modelo in @modelo.objects.all():' + '\n'
    else:
        strr += tab + 'for reg_@modelo in @modelo.objects.filter(' + padre + '=' + 'reg_' + padre + '):' + '\n'
        padre = modelo.nombre

    strr += dostab + 'if primer_@modelo:' + '\n'
    strr += trestab + 'datos_titulo = []' + '\n'
    strr += trestab + 'datos_titulo.append([' + "'" + '@titulo' + "'" + ',@titulox])' + '\n'
    strr += trestab + 'datos_titulo.append([@fecha,@fechax])' + '\n'
    strr += trestab + 'datos_titulo.append(@iniciolineax)' + '\n'
    strr += trestab + 'datos_titulo.append(@finallineax)' + '\n'
    strr += trestab + 'datos_titulo.append(@grosor)' + '\n'

    if modelo.identacionautomatica and nivel>1:
        strr = strr.replace('@iniciolineax',str(lineaix+identa))
        strr = strr.replace('@titulox',str(titulox+identa))
    else:
        strr = strr.replace('@iniciolineax',str(modelo.lineaix))
        strr = strr.replace('@titulox',str(modelo.titulox))

    strr = strr.replace('@fechax',str(modelo.fechax))
    strr = strr.replace('@titulo',str(modelo.titulolista))
    strr = strr.replace('@grosor',str(modelo.grosorlinea))

    if nivel == 1:
        strr = strr.replace('@fecha','True')
    else:
        strr = strr.replace('@fecha','False')

    # Nombres de columnas
    for prop in Propiedad.objects.filter(modelo = modelo):
        if pos ==1:
            pos +=1
            if modelo.identacionautomatica and nivel>1:    
                strp += str(datosix + identa) + ',' + "'" + prop.nombre + "'"
            else:
                strp += str(modelo.datoinicialx + identa) + ',' + "'" + prop.nombre + "'"
        else:
            strp += ',' + str(delta + identa) + ',' + "'" + prop.nombre + "'"
        delta += modelo.datoinicialx + prop.anchoenreporte

    strr += trestab  + 'datos_titulo.append([' + strp + '])' + '\n'
    strr += trestab  + 'Acomoda(datos_detalle,datos_reporte,primeralinea,True,datos_titulo)' + '\n'
    strr += trestab  + 'primer_@modelo=False' + '\n'

    # Habilitar titulos de hijos

    for modhijo in Modelo.objects.filter(padre=modelo.nombre,proyecto=proyecto):
        strr += dostab  + 'primer_@modelohijo=True' + '\n'
        strr = strr.replace('@modelohijo',modhijo.nombre)
        
    strr += dostab + 'datos_reporte[0] += 1' + '\n'
    strr += dostab + 'Acomoda(datos_detalle,datos_reporte,primeralinea,False,datos_titulo)' + '\n'

    # Datos

    strp = ''
    delta = 0
    pos = 1
    identa = 0

    if modelo.identacionautomatica and nivel>1:
        identa  = (nivel-1)

    for prop in Propiedad.objects.filter(modelo = modelo):
        if prop.totaliza and (prop.tipo == 'd' or prop.tipo == 'i' or prop.tipo == 'l' or prop.tipo == 'm'):
            listatotales.append('    total_' + modelo.nombre + '_' + prop.nombre + ' = 0' + '\n')
            strr += dostab + 'nu_@propiedad = ' + "'" + '{:.2f}' + "'" + '.format(float(reg_@modelo.@propiedad))' + '\n'
            strr += dostab + 'total_@modelo_@propiedad += float(reg_@modelo.@propiedad)' + '\n'
            strr = strr.replace('@propiedad',prop.nombre)
            strr = strr.replace('@modelo',modelo.nombre)
            if pos ==1:
                pos +=1
                if modelo.identacionautomatica and nivel>1:        
                    strr += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(datosix + identa) + ',primeralinea-datos_reporte[1]],str(nu_' + prop.nombre + '),' + "'" + 'r' + "'" + '])' + '\n'
                else:
                    strr += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(modelo.datoinicialx + identa) + ',primeralinea-datos_reporte[1]],str(nu_' + prop.nombre + '),' + "'" + 'r' + "'" + '])' + '\n'
            else:
                strr += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(delta + identa) + ',primeralinea-datos_reporte[1]],str(nu_' + prop.nombre + '),' + "'" + 'r' + "'" + '])' + '\n'
        
            if modelo.identacionautomatica and nivel>1:            
                delta += datosix + prop.anchoenreporte
            else:
                delta += modelo.datoinicialx + prop.anchoenreporte
        elif prop.tipo == 'p':
            strr += dostab + 'try:' + '\n'
            strr += trestab + 'cd = os.getcwd()' + '\n'
            strr += trestab + 'img = cd + ' + "'" + '/' + "'" + ' + reg_cuenta.foto.url' + '\n'
            strr += dostab + 'except:' + '\n'
            strr += trestab + 'pass' + '\n'     
            if pos ==1:
                pos +=1
                if modelo.identacionautomatica and nivel>1:            
                    strr += dostab + 'datos_detalle.append([8,img,[' + str(datosix + identa) + ',primeralinea-datos_reporte[1]],[1/2.5,1/2.5]])' + '\n'
                else:
                    strr += dostab + 'datos_detalle.append([8,img,[' + str(modelo.datoinicialx + identa) + ',primeralinea-datos_reporte[1]],[1/2.5,1/2.5]])' + '\n'
            else:
                strr += dostab + 'datos_detalle.append([8,img,[' + str(delta + identa) + ',primeralinea-datos_reporte[1]],[1/2.5,1/2.5]])' + '\n'  
        else:
            if pos ==1:
                pos +=1
                if modelo.identacionautomatica and nivel>1:            
                    strr += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(datosix + identa) + ',primeralinea-datos_reporte[1]],str(reg_@modelo.' + prop.nombre + '),' + "'" + 'l' + "'" + '])' + '\n'
                else:
                    strr += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(modelo.datoinicialx + identa) + ',primeralinea-datos_reporte[1]],str(reg_@modelo.' + prop.nombre + '),' + "'" + 'l' + "'" + '])' + '\n'
            else:
                strr += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(delta + identa) + ',primeralinea-datos_reporte[1]],str(reg_@modelo.' + prop.nombre + '),' + "'" + 'l' + "'" + '])' + '\n'
        
            if modelo.identacionautomatica and nivel>1:            
                delta += datosix + prop.anchoenreporte
            else:
                delta += modelo.datoinicialx + prop.anchoenreporte

    strr += dostab + 'datos_reporte[1] += 0.4' + '\n'

    strr = strr.replace('@modelo',modelo.nombre)            

    lista.append(strr)

    for mod in Modelo.objects.filter(padre=modelo,proyecto=proyecto):
        RecursivoReporte(lista,listatitulos,listatotales,mod,nivel+1,proyecto,modelo.nombre,lineaix,datosix,titulox,padre)

    strp = ''
    delta = 0
    pos = 1
    identa = 0

    if modelo.identacionautomatica and nivel>1:
        identa  = (nivel-1)

    flgExisteTotaliza = False

    strexp = ''
    for prop in Propiedad.objects.filter(modelo = modelo):
        if prop.totaliza and (prop.tipo == 'd' or prop.tipo == 'i' or prop.tipo == 'l' or prop.tipo == 'm'):
            flgExisteTotaliza = True
            strexp += dostab + 'total = ' + "'" + '{:.2f}' + "'" + '.format(float(total_@modelo_@propiedad))' + '\n'
            strexp = strexp.replace('@propiedad',prop.nombre)
            strexp = strexp.replace('@modelo',modelo.nombre)
            if pos ==1:
                pos +=1
                if modelo.identacionautomatica and nivel>1:        
                    strexp += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(datosix + identa) + ',primeralinea-datos_reporte[1]],str(total),' + "'" + 'r' + "'" + '])' + '\n'
                else:
                    strexp += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(modelo.datoinicialx + identa) + ',primeralinea-datos_reporte[1]],str(total),' + "'" + 'r' + "'" + '])' + '\n'
            else:
                strexp += dostab + 'datos_detalle.append([1,[' + "'" + 'Helvetica' + "'" + ',9,colors.black],[' + str(delta + identa) + ',primeralinea-datos_reporte[1]],str(total),' + "'" + 'r' + "'" + '])' + '\n'
        
        else:
            if pos == 1:
                pos += 1

        if modelo.identacionautomatica and nivel>1:            
            delta += datosix + prop.anchoenreporte
        else:
            delta += modelo.datoinicialx + prop.anchoenreporte

    strs = tab + 'if not primer_@modelo:' + '\n'

    if flgExisteTotaliza:
        strs += dostab + 'datos_reporte[0] += 2' + '\n'
        strs += dostab + 'Acomoda(datos_detalle,datos_reporte,primeralinea,False,datos_titulo)' + '\n'
        if modelo.identacionautomatica and nivel>1:        
            strs += dostab + 'datos_detalle.append([4,[@iniciolineax,primeralinea-datos_reporte[1]+0.2,@finallineax,primeralinea-datos_reporte[1]+0.2,0.3]])' + '\n'
            strs = strs.replace('@iniciolineax',str(lineaix+identa))
        else:
            strs += dostab + 'datos_detalle.append([4,[@iniciolineax,primeralinea-datos_reporte[1]+0.2,@finallineax,primeralinea-datos_reporte[1]+0.2,0.3]])' + '\n'
            strs = strs.replace('@iniciolineax',str(modelo.lineaix+identa))

        strs += dostab + 'datos_reporte[1] += 0.13' + '\n'
        strs += strexp
        strs += dostab + 'datos_reporte[1] += 0.3' + '\n'
        strs += dostab + 'datos_detalle.append([4,[@iniciolineax,primeralinea-datos_reporte[1]+0.2,@finallineax,primeralinea-datos_reporte[1]+0.2,0.3]])' + '\n'
        strs += dostab + 'datos_detalle.append([4,[@iniciolineax,primeralinea-datos_reporte[1]+0.15,@finallineax,primeralinea-datos_reporte[1]+0.15,0.3]])' + '\n'
        if modelo.identacionautomatica and nivel>1:        
            strs = strs.replace('@iniciolineax',str(lineaix+identa))
        else:
            strs = strs.replace('@iniciolineax',str(modelo.lineaix+identa))        
        strs += dostab + 'datos_reporte[1] += 0.3' + '\n'
    else:
        strs += dostab + 'datos_reporte[0] += 2' + '\n'
        strs += dostab + 'Acomoda(datos_detalle,datos_reporte,primeralinea,False,datos_titulo)' + '\n'

        strs += dostab + 'datos_detalle.append([4,[@iniciolineax,primeralinea-datos_reporte[1]+0.2,@finallineax,primeralinea-datos_reporte[1]+0.2,0.3]])' + '\n'
        strs += dostab + 'datos_detalle.append([4,[@iniciolineax,primeralinea-datos_reporte[1]+0.15,@finallineax,primeralinea-datos_reporte[1]+0.15,0.3]])' + '\n'
        
        if modelo.identacionautomatica and nivel>1:        
            strs = strs.replace('@iniciolineax',str(lineaix+identa))
        else:
            strs = strs.replace('@iniciolineax',str(modelo.lineaix+identa))
        
        strs += dostab + 'datos_reporte[1] += 0.8' + '\n'

    strs = strs.replace('@modelo',modelo.nombre)

    lista.append(strs)

def CrearUrls(proyecto,directorio,dt,usuario):

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()

    nombre = proyecto.nombre
    etapa = "CrearUrls"

    # urls para el proyecto
    strlfp = ''
    strlpp = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        if AplicacionTienePropiedades(aplicacion) or aplicacion.nombre == 'core':
            # Preparar los patterns para urls del proyecto
            if strlfp.find('from @aplicacion.urls import @aplicacion_patterns') == -1:
                strlfp += 'from @aplicacion.urls import @aplicacion_patterns' + '\n'
            if aplicacion.nombre == 'core':
                strlpp += '\tpath(' + "'" + "'" + ',include(@aplicacion_patterns)),' + '\n'
            else:    
                strlpp += '\tpath(' + "'" + '@aplicacion/' + "'" + ',include(@aplicacion_patterns)),' + '\n'

            strlfp = strlfp.replace('@aplicacion', aplicacion.nombre)
            strlpp = strlpp.replace('@aplicacion', aplicacion.nombre)

    # Leer el archivo urls_proyecto.py de text files
    stri = TextFiles.objects.get(file = "urls_proyecto.py").texto
    # stri = LeerArchivo(dt + "urls_proyecto.py",etapa,nombre,usuario)

    stri = stri.replace('@listafrompatterns', strlfp)
    stri = stri.replace('@listapathpatterns', strlpp)

    ProcesoPersonalizacion(proyecto,nombre,'urls.py',directorio + nombre + "/" + nombre + "/",stri,nombre,etapa,usuario)

    # # Grabar el archivo urls.py en el proyecto
    # stri = EscribePersonalizacion(proyecto,None,'urls.py',stri)
    # #Sin lineas de personalizacion
    # if not proyecto.conetiquetaspersonalizacion:
    #     stri = QuitaLineasPersonalizacion(stri)

    # EscribirArchivo(directorio + nombre + "/" + nombre + "/urls.py",etapa,nombre,stri,True)

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Copiar el archivo urls.py de text files en el directorio de la aplicacion core
        if aplicacion.nombre == 'core':
            stri = TextFiles.objects.get(file = "core_urls.py").texto
            # stri = LeerArchivo(dt + "core_urls.py",etapa,nombre,usuario)

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'urls.py',directorio + nombre + "/" + aplicacion.nombre + "/",stri,nombre,etapa,usuario)

            # stri = EscribePersonalizacion(proyecto,aplicacion,'urls.py',stri)
            # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     stri = QuitaLineasPersonalizacion(stri)                    
            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/urls.py",etapa,nombre,stri,True)

        # leer archivo urls.py de core/text_files
        stri = TextFiles.objects.get(file = "urls_modelo.py").texto
        # stri = LeerArchivo(dt + "urls_modelo.py",etapa,nombre,usuario)

        # Para cada modelo
        strt = ''
        strp = ''
        strlv = ''

        if strlv.find('from .views import HomeView') == -1:
            strlv = 'from .views import HomeView' + '\n'

        strp = '\tpath(' + "''" + ',@required(HomeView.as_view()), name=' + "'" + 'home' + "'" + '),' + '\n'

        if proyecto.conseguridad:
            if aplicacion.homestaff:
                strp = strp.replace('@required', 'staff_member_required')
            elif aplicacion.homelogin:
                strp = strp.replace('@required', 'login_required')
            else:
                strp = strp.replace('@required', '')

        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if modelo.sinbasedatos == False:
                if Propiedad.objects.filter(modelo=modelo).count() > 0:
                    if modelo.padre == 'nada':
                        if strlv.find('from .views import Listar@moduloView, Crear@moduloView, Editar@moduloView, Borrar@moduloView, Reporte@moduloView') == -1:
                            strlv += 'from .views import Listar@moduloView, Crear@moduloView, Editar@moduloView, Borrar@moduloView, Reporte@moduloView' + '\n'
                    else:
                        if strlv.find('from .views import Crear@moduloView, Editar@moduloView, Borrar@moduloView') == -1:
                            strlv += 'from .views import Crear@moduloView, Editar@moduloView, Borrar@moduloView' + '\n'

                    strlv = strlv.replace('@modulo', modelo.nombre)

                    if modelo.padre == 'nada':
                        # strp += '\tpath(' + "''" + ', Home@moduloView.as_view(), name=' + "'" + 'home' + "'" + '),' + '\n'
                        # strp += '\tpath(' + "''" + ',@required(Home' + '@modulo' + 'View), name=' + "'" + 'home' + "'" + '),' + "\n"
                        # # seguridad home
                        # if proyecto.conseguridad:
                        #     if modelo.homestaff:
                        #         strp = strp.replace('@required', 'staff_member_required')
                        #     elif modelo.homelogin:
                        #         strp = strp.replace('@required', 'login_required')
                        #     else:
                        #         strp = strp.replace('@required', '')

                        strp += '\tpath(' + "'listar_" + '@modulom/' + "'" + ',@required(Listar@moduloView.as_view()), name=' + "'" + 'listar_@modulom' + "'" + '),' + '\n'
                        strp += '\tpath(' + "'reporte_" + '@modulom/' + "'" + ',Reporte@moduloView, name=' + "'" + 'reporte_@modulom' + "'" + '),' + '\n'

                        if proyecto.conseguridad:
                            # seguridad listar
                            if modelo.listastaff:
                                strp = strp.replace('@required', 'staff_member_required')
                            elif modelo.listalogin:
                                strp = strp.replace('@required', 'login_required')
                            else:
                                strp = strp.replace('@required', '')

                    strp += '\tpath(' + "'" + 'editar_@modulom/<int:pk>/' + "'" + ',@required(Editar@moduloView.as_view()), name=' + "'" + 'editar_@modulom' + "'" +'),' + '\n'
                    # seguridad editar
                    if proyecto.conseguridad:
                        if modelo.editarstaff:
                            strp = strp.replace('@required', 'staff_required')
                        elif modelo.editarlogin:
                            strp = strp.replace('@required', 'login_required')
                        else:
                            strp = strp.replace('@required', '')

                    strp += '\tpath(' + "'" + 'crear_@modulom/' + "'" + ',@required(Crear@moduloView.as_view()), name=' + "'" + 'crear_@modulom' + "'" + '),' + '\n'
                    # seguridad crear
                    if proyecto.conseguridad:
                        if modelo.crearstaff:
                            strp = strp.replace('@required', 'staff_member_required')
                        elif modelo.crearlogin:
                            strp = strp.replace('@required', 'login_required')
                        else:
                            strp = strp.replace('@required', '')

                    strp += '\tpath(' + "'" + 'borrar_@modulom/<int:pk>/' + "'" + ',@required(Borrar@moduloView.as_view()), name=' + "'" + 'borrar_@modulom' + "'" + '),' + '\n'
                    # seguridad borarr
                    if proyecto.conseguridad:
                        if modelo.borrarstaff:
                            strp = strp.replace('@required', 'staff_member_required')
                        elif modelo.borrarlogin:
                            strp = strp.replace('@required', 'login_required')
                        else:
                            strp = strp.replace('@required', '')

                    strp = strp.replace('@required', '')
                    strp = strp.replace('@modulom', modelo.nombre)
                    strp = strp.replace('@modulo', modelo.nombre)

                    strt += strp + '\n'
                    strp = ''
            else:
                if strlv.find('from .views import @moduloView') == -1:
                    strlv += 'from .views import @moduloView' + '\n'
                strlv = strlv.replace('@modulo', modelo.nombre)
                
                strp += '\tpath(' + "'" + '@modulo/' + "'" + ',@required(@moduloView.as_view()), name=' + "'" + '@modulo' + "'" +'),' + '\n'
                strp = strp.replace('@modulo', modelo.nombre)                # seguridad listar
                if modelo.listastaff:
                    strp = strp.replace('@required', 'staff_member_required')
                elif modelo.listalogin:
                    strp = strp.replace('@required', 'login_required')
                else:
                    strp = strp.replace('@required', '')
                strt += strp + '\n'
                strp = ''

        if strt != '':
            stri = stri.replace('@aplicacion', aplicacion.nombre)
            stri = stri.replace('@listaurls', strt)
            stri = stri.replace('@listaviews', strlv)



        # strt = EscribePersonalizacion(proyecto,aplicacion,'urls.py',strt)

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        if AplicacionTienePropiedades(aplicacion):

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'urls.py',directorio + nombre + "/" + aplicacion.nombre + "/",stri,nombre,etapa,usuario)

            # # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     stri = QuitaLineasPersonalizacion(stri)

            # # Grabar el archivo urls.py
            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/urls.py",etapa,nombre,stri,True)

    # Manejo de los urls de los modelos hijos que son foreign en otros modelos select
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        strUrls = ''
        strLoad = ''

        # Copiar el archivo urls.py de text files en el directorio de la aplicacion core
        if aplicacion.nombre != 'core' and aplicacion.nombre != 'registration':    
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                for propiedad in Propiedad.objects.filter(modelo=modelo):
                    if propiedad.tipo == 'f':
                        modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea,proyecto=proyecto)
                        if modelo_foraneo.padre !='nada':
                            # Ver si el padre esta en el mismo modelo
                            for modelo_padre in Modelo.objects.filter(proyecto=proyecto):
                                if modelo_padre.nombre == modelo_foraneo.padre:
                                    # Existe el modelo padre la llave foranea
                                    # Crear el url para la lista de modelos hijo
                                    strUrls += "\tpath('ajax/load-@modelos/', load_@modelos, name='ajax_load_@modelos')," + '\n'
                                    if strLoad.find("from .views import load_@modelos") == -1:
                                        strLoad += "from .views import load_@modelos" + '\n'
                                    strUrls = strUrls.replace('@modelo',modelo_foraneo.nombre)
                                    strLoad = strLoad.replace('@modelo',modelo_foraneo.nombre)
                                    break
        if AplicacionTienePropiedades(aplicacion):                                    
            # Leer el html de insercion y update del modelo con llaves foraneas
            strh = LeerArchivoEnTexto(directorio + nombre + '/' + aplicacion.nombre + '/urls.py',etapa,nombre,usuario)
            strh = strh.replace('@urlshijos',strUrls)
            strh = strh.replace('@loadhijos',strLoad)
            EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + '/urls.py',etapa,nombre,strh,usuario,True)

def CrearTemplates(proyecto,directorio,directoriogenesis,dt,usuario):

    # Leer la aplicacion core
    appCore = Aplicacion.objects.get(proyecto=proyecto,nombre='core')

    # Actualizar las alturas del medio
    proyecto.altofilamedio = -100
    proyecto.altocolumnamedioizquierda = -100
    proyecto.altocolumnamedioderecha = -100
    proyecto.altocolumnamediocentro = -100
    proyecto.save()

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()

    nombre = proyecto.nombre
    etapa = "CrearTemplates"
    dc = "\""

# Crear los archivos js

    # leer el archivo js
    strjs = TextFiles.objects.get(file = "js_propios.js").texto
    # strjs = LeerArchivo(dt + "js_propios.js",etapa,nombre,usuario)
    # variable para el manejo de los js
    strfjs = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto).order_by('ordengeneracion'):

        for modelo in Modelo.objects.filter(aplicacion=aplicacion).order_by('ordengeneracion'):

            # actualiza el archivo js

            if modelo.buscadorlista:
                if modelo.padre == 'nada':
                    strfjs +=  '// Funcion que se ejecuta cuando se acciona el boton' + '\n'
                    strfjs +=  '// de busqueda en el html del modelo @modelo' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_01] //' + '\n'
                    strfjs += '$(function(){' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_02] //' + '\n'
                    strfjs += '\tvar enlace = $(' + "'" + '#link-busqueda_@modelo' + "'" + ');' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_03] //' + '\n'
                    strfjs += '\tenlace.on(' + "'" + 'click' + "'" + ',function(){' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_04] //' + '\n'
                    strfjs += '\tvar texto = $(' + "'" + '#textob@modelo' + "'" + ');' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_05] //' + '\n'
                    strfjs += '\tenlace.attr(' + "'" + 'href' + "'" + ',' + "'" + 'http://127.0.0.1:8001/@aplicacion/listar_@modelo?duplica=0&criterio=' + "'" + ' + ' + 'texto.val());' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_06] //' + '\n'
                    strfjs += '});' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_07] //' + '\n'
                    strfjs += '}())' + '\n'
                    strfjs +=  '// #@[p_js_busqueda_@modelo_08] //' + '\n'

                    strfjs = strfjs.replace('@modelo', modelo.nombre)
                    strfjs = strfjs.replace('@aplicacion', aplicacion.nombre)

    # actualiza el archivo js
    strjs = strjs.replace('@busqueda', strfjs)
    EscribirArchivo(directorio +"/" + nombre + "/core/static/core/js/js_propios.js",etapa,nombre,strjs,usuario,True)

    # Leer el archivo base.html desde textfiles
    if proyecto.menuscontiguos:
        stri = TextFiles.objects.get(file = "base_contiguo.html").texto
    else:
        stri = TextFiles.objects.get(file = "base.html").texto
    # stri = LeerArchivoEnTexto(dt + "base.html",etapa,nombre,usuario)

    # Ver si existe un fondo de la pagina principal
    strBody = ''
    if proyecto.imagenpaginaprincipal:
        strBody = "background: url({% static " + "'" + "core/img/imagen-fondo-pagina-principal.png" + "'" + " %}) no-repeat center center fixed;"
        strBody += "background-size: cover;"
        strBody += "-moz-background-size: cover;"
        strBody += "-webkit-background-size: cover;"
        strBody +="-o-background-size: cover;"
        strBody +="background-color: transparent;"    
    stri = stri.replace('@estilo',strBody)

    # Copiar fondo de la pagina principal a core/img
    if proyecto.imagenpaginaprincipal:
        CopiaImagenes(directorio + nombre + "/core/static/core/img/imagen-fondo-pagina-principal.png", 'proyectos', proyecto.imagenpaginaprincipal.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )

    # Copiar imagen primera pagina
    if proyecto.imagenmedio:
        CopiaImagenes(directorio + nombre + "/core/static/core/img/imagen-medio.png", 'proyectos', proyecto.imagenmedio.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )

    # LOGO
    strAvatar = ''
    # Copiar el logo del proyecto a la direccion core/img

    if proyecto.avatar:
        strAvatar = "<img alt=" + dc + dc + " src=" + dc + "{% static 'core/img/logo.png' %}" + dc + ">" + "\n"
        # Copiar el logo del Proyecto en el directorio core/img
        CopiaImagenes(directorio + nombre + "/core/static/core/img/logo.png", 'proyectos', proyecto.avatar.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )

    stri = stri.replace("@logo",strAvatar)
    # if proyecto.avatar:
    #     stri = stri.replace("@avatarwidth",str(proyecto.avatarwidth))
    #     stri = stri.replace("@avatarheight",str(proyecto.avatarheight))

    # Justificacion del logo
    stri = AsignaJustificacion('h',proyecto.justificacionhorizontallogo,'@justificacionlogohorizontal',stri)
    stri = AsignaJustificacion('v',proyecto.justificacionverticallogo,'@justificacionlogovertical',stri)

        
    # TITULO
    strTitulo = ''
    
    if proyecto.imagentitulo:
        strTitulo = "<img alt=" + dc + dc + " src=" + dc + "{% static 'core/img/imagentitulo.png' %}" + dc + " width=" + dc + "@imagentitulowidthpx" + dc + " height=" + dc + "@imagentituloheightpx" + dc + " >"
        # Copiar el logo del titulo en el directorio core/img
        CopiaImagenes(directorio + nombre + "/core/static/core/img/imagentitulo.png", 'proyectos', proyecto.imagentitulo.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )
    else:
        strTitulo = proyecto.titulo

    stri = stri.replace("@titulo",strTitulo)

    if proyecto.imagentitulo:
        stri = stri.replace("@imagentitulowidth",str(proyecto.imagentitulowidth))
        stri = stri.replace("@imagentituloheight",str(proyecto.imagentituloheight))

    # Justificacion del titulo
    stri = AsignaJustificacion('h',proyecto.justificacionhorizontaltitulo,'@justificaciontitulohorizontal',stri)
    stri = AsignaJustificacion('v',proyecto.justificacionverticaltitulo,'@justificaciontitulovertical',stri)
    
    # Dimensiones del columnas

    if proyecto.numerocolumnaenizquierda > 0:
        stri = stri.replace("@12numerocolumnaenizquierda",str(12))
    if proyecto.numerocolumnaenderecha > 0:
        stri = stri.replace("@12numerocolumnaenderecha",str(12))
    if proyecto.numerocolumnamenu > 0:
        stri = stri.replace("@12numerocolumnamenu",str(12))
    if proyecto.numerocolumnalogo > 0:
        stri = stri.replace("@12numerocolumnalogo",str(12))
    if proyecto.numerocolumnatitulo > 0:
        stri = stri.replace("@12numerocolumnatitulo",str(12))
    if proyecto.numerocolumnalogin > 0:
        stri = stri.replace("@12numerocolumnalogin",str(12))
    if proyecto.numerocolumnamedioizquierda > 0:
        stri = stri.replace("@12numerocolumnamedioizquierda",str(12))
    if proyecto.numerocolumnamediocentro > 0:
        stri = stri.replace("@12numerocolumnamediocentro",str(12))
    if proyecto.numerocolumnamedioderecha > 0:
        stri = stri.replace("@12numerocolumnamedioderecha",str(12))
    if proyecto.numerocolumnabumederecha > 0:
        stri = stri.replace("@12numerocolumnabumederecha",str(12))
    if proyecto.numerocolumnabumeizquierda > 0:
        stri = stri.replace("@12numerocolumnabumeizquierda",str(12))

    stri = stri.replace("@12numerocolumnaenizquierda",str(0))
    stri = stri.replace("@12numerocolumnaenderecha",str(0))
    stri = stri.replace("@12numerocolumnamenu",str(0))
    stri = stri.replace("@12numerocolumnalogo",str(0))
    stri = stri.replace("@12numerocolumnatitulo",str(0))
    stri = stri.replace("@12numerocolumnalogin",str(0))
    stri = stri.replace("@12numerocolumnamedioizquierda",str(0))
    stri = stri.replace("@12numerocolumnamediocentro",str(0))
    stri = stri.replace("@12numerocolumnamedioderecha",str(0))
    stri = stri.replace("@12numerocolumnabumederecha",str(0))
    stri = stri.replace("@12numerocolumnabumeizquierda",str(0))

    stri = stri.replace("@numerocolumnaenizquierda",str(proyecto.numerocolumnaenizquierda))
    stri = stri.replace("@numerocolumnaenderecha",str(proyecto.numerocolumnaenderecha))
    if proyecto.menuscontiguos:
        stri = stri.replace("@numerocolumnamenu",str(proyecto.numerocolumnamenu))
    else:
        stri = stri.replace("@numerocolumnamenu",str(int(proyecto.numerocolumnamenu/2)))
    stri = stri.replace("@numerocolumnalogo",str(proyecto.numerocolumnalogo))
    stri = stri.replace("@numerocolumnatitulo",str(proyecto.numerocolumnatitulo))
    stri = stri.replace("@numerocolumnalogin",str(proyecto.numerocolumnalogin))
    stri = stri.replace("@numerocolumnamedioizquierda",str(proyecto.numerocolumnamedioizquierda))
    stri = stri.replace("@numerocolumnamediocentro",str(proyecto.numerocolumnamediocentro))
    stri = stri.replace("@numerocolumnamedioderecha",str(proyecto.numerocolumnamedioderecha))
    stri = stri.replace("@numerocolumnabumederecha",str(proyecto.numerocolumnabumederecha))
    stri = stri.replace("@numerocolumnabumeizquierda",str(proyecto.numerocolumnabumeizquierda))

    # Copiar el menu de seguridad
    if proyecto.conseguridad:
        strMenu = TextFiles.objects.get(file = "menu_seguridad.html").texto
    else:
        strMenu = TextFiles.objects.get(file = "vacio").texto
    EscribirArchivo(directorio + nombre + '/core/templates/core/includes/menu_seguridad.html',etapa,nombre,strMenu,usuario,True)

    # Crear el menu_core.html
    strTemp=''
    if proyecto.menuscontiguos:
        strMenu = TextFiles.objects.get(file = "menu_core_contiguo.html").texto
        # strMenu = LeerArchivoEnTexto(dt + 'menu_core_contiguo.html',etapa,nombre,usuario)
    else:
        strMenu = TextFiles.objects.get(file = "menu_core_contiguo.html").texto
        # strMenu = LeerArchivoEnTexto(dt + 'menu_core.html',etapa,nombre,usuario)

    # Copiar las imagenes propuestas en opciones de seguridad
    CopiarArchivos(dt + "registration/loginSF.png", directorio + nombre + "/core/static/core/img/loginSF.png",etapa,nombre, usuario,True)
    CopiarArchivos(dt + "registration/logoutSF.png", directorio + nombre + "/core/static/core/img/logoutSF.png",etapa,nombre, usuario,True)
    CopiarArchivos(dt + "registration/registroSF.png", directorio + nombre + "/core/static/core/img/registroSF.png",etapa,nombre, usuario,True)
    CopiarArchivos(dt + "registration/perfilSF.png", directorio + nombre + "/core/static/core/img/perfilSF.png",etapa,nombre, usuario,True)
    CopiarArchivos(dt + "registration/homeSF.png", directorio + nombre + "/core/static/core/img/homeSF.png",etapa,nombre, usuario,True)

    if proyecto.conseguridad == True:
        strTemp = TextFiles.objects.get(file = "registration/conseguridad.html").texto
        # strTemp =  LeerArchivoEnTexto(dt + 'registration/conseguridad.html',etapa,nombre,usuario)
        if proyecto.menuscontiguos:
            strMenu = strMenu.replace('@columnas_opciones','col-12')
        else:
            strMenu = strMenu.replace('@columnas_opciones','col-12 col-sm-8 col-md-9')
            strMenu = strMenu.replace('@columnas_seguridad','col-12 col-sm-4 col-md-3')
    else:
        strMenu = strMenu.replace('@columnas_opciones','col-12')
        strMenu = strMenu.replace('@columnas_seguridad','col-0')

    strMenu = strMenu.replace('@seguridad',strTemp)
    strMenu = AsignaJustificacion('h',proyecto.justificacionmenu,'@justificacion',strMenu)

    # Lista de aplicaciones
    strApp = ''
    strMod = ''
    strVolver = ''
    strOpcionAplicacion = ''
    strOpcionModelo = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        if aplicacion.nombre != 'core' and aplicacion.nombre != 'registration':
            # Ver si la aplicacion tiene modelos que no son dependientes
            for msp in Modelo.objects.filter(aplicacion=aplicacion):
                if msp.padre == 'nada':
                    # Leer el archivo opcion_aplicacion.html de textfiles
                    strApp += TextFiles.objects.get(file = "opcion_aplicacion.html").texto
                    # strApp += LeerArchivoEnTexto(dt + 'opcion_aplicacion.html',etapa,nombre,usuario)
                    strApp = strApp.replace("@aplicacion",aplicacion.nombre)
                    strApp = strApp.replace("@tooltip",aplicacion.tooltip)
                    break
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if modelo.padre == 'nada':
                    # Leer el archivo opcion_modelo.html de textfiles
                    strMod += TextFiles.objects.get(file = "opcion_modelo.html").texto
                    # strMod += LeerArchivoEnTexto(dt + 'opcion_modelo.html',etapa,nombre,usuario)
                    strMod = strMod.replace("@modelo",modelo.nombre)
                    strMod = strMod.replace("@aplicacion",aplicacion.nombre)
                    strApp = strApp.replace("@tooltip",modelo.tooltip)
            # if proyecto.conseguridad:
            #     # Leer el archivo seguridad.html de textfiles
            #     strMod += LeerArchivoEnTexto(dt + "registration/conseguridad.html",etapa,nombre)
            #     strMod = strMod.replace("@aplicacion",aplicacion.nombre)
            # Leer el archivo volver_aplicacion.html de textfiles
            strVolver += TextFiles.objects.get(file = "opcion_volver_aplicacion.html").texto
            # strVolver += LeerArchivoEnTexto(dt + 'opcion_volver_aplicacion.html',etapa,nombre,usuario) + '\n'
            strVolver = strVolver.replace("@aplicacion",aplicacion.nombre)
            strVolver = strVolver.replace("@modelos",strMod)
            if proyecto.imagenvolver:
                strVolver = strVolver.replace("@hidden",'')
            else:
                h= "hidden=" + '"' + "true" + '"'
                strVolver = strVolver.replace("@hidden",h)

            strMod = ''

            # Crear el home para cada aplicacion
            strHome = TextFiles.objects.get(file = "home_aplicacion.html").texto
            # strHome = LeerArchivoEnTexto(dt + 'home_aplicacion.html',etapa,nombre,usuario)
            strHome = strHome.replace('@aplicacion',aplicacion.nombre)
            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'home.html',directorio + nombre + '/' + aplicacion.nombre + '/templates/' + aplicacion.nombre +'/',strHome,nombre,etapa,usuario)
            # EscribirArchivo(directorio + nombre + '/' + aplicacion.nombre + '/templates/' + aplicacion.nombre +'/home.html' ,etapa,nombre,strHome,True)

            # Acumular el listado de aplicaciones
            if AplicacionConObjetoRaiz(aplicacion):
                strOpcionAplicacion += TextFiles.objects.get(file = "opcion_aplicacion.html").texto
                # strOpcionAplicacion += LeerArchivoEnTexto(dt + 'opcion_aplicacion.html',etapa,nombre,usuario)
                strOpcionAplicacion = strOpcionAplicacion.replace('@aplicacion',aplicacion.nombre)
                strOpcionAplicacion = strOpcionAplicacion.replace('@tooltip',aplicacion.tooltip)
                try:
                    if aplicacion.imagenmenu:
                        strOpcionAplicacion = strOpcionAplicacion.replace("@avatar",aplicacion.nombre + '.png')
                        strOpcionAplicacion = strOpcionAplicacion.replace("@hidden",'')
                        CopiaImagenes(directorio + nombre + "/core/static/core/img/" + aplicacion.nombre + '.png', 'proyectos', aplicacion.imagenmenu.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )
                    else:
                        h= "hidden=" + '"' + "true" + '"'
                        strOpcionAplicacion = strOpcionAplicacion.replace("@avatar",'')
                        strOpcionAplicacion = strOpcionAplicacion.replace("@hidden",h)
                except:
                    pass
                if aplicacion.textoenmenu == '':
                    aplicacion.textoenmenu = aplicacion.nombre
                    aplicacion.save()
                strOpcionAplicacion = strOpcionAplicacion.replace('@opcionaplicacion',aplicacion.textoenmenu)

            # Crear el menu por cada aplicacion
            strTemp=''
            if proyecto.menuscontiguos:
                strMenuModelo = TextFiles.objects.get(file = "menu_aplicacion_contiguo.html").texto
                # strMenuModelo = LeerArchivoEnTexto(dt + 'menu_aplicacion_contiguo.html',etapa,nombre,usuario)
            else:
                strMenuModelo = TextFiles.objects.get(file = "menu_aplicacion.html").texto
                # strMenuModelo = LeerArchivoEnTexto(dt + 'menu_aplicacion.html',etapa,nombre,usuario)

            strMenuModelo = strMenuModelo.replace('@aplicacion',aplicacion.nombre)
            if proyecto.imagenvolver:
                strMenuModelo = strMenuModelo.replace("@hidden",'')
            else:
                h= "hidden=" + '"' + "true" + '"'
                strMenuModelo = strMenuModelo.replace("@hidden",h)

            if proyecto.conseguridad == True:
                strTemp = TextFiles.objects.get(file = "registration/conseguridad.html").texto
                # strTemp =  LeerArchivoEnTexto(dt + 'registration/conseguridad.html',etapa,nombre,usuario)
                if proyecto.menuscontiguos:
                    strMenuModelo = strMenuModelo.replace('@columnas_opciones','col-12')
                else:
                    strMenuModelo = strMenuModelo.replace('@columnas_opciones','col-12 col-sm-8 col-md-9')
                    strMenuModelo = strMenuModelo.replace('@columnas_seguridad','col-12 col-sm-4 col-md-3')
                
                # strMenuModelo = strMenuModelo.replace('@columnas_opciones','8')
                # strMenuModelo = strMenuModelo.replace('@columnas_seguridad','4')
            else:
                strMenuModelo = strMenuModelo.replace('@columnas_opciones','col-12')
                strMenuModelo = strMenuModelo.replace('@columnas_seguridad','col-0')

            strMenuModelo = strMenuModelo.replace('@seguridad',strTemp)
            strMenuModelo = AsignaJustificacion('h',proyecto.justificacionmenu,'@justificacion',strMenuModelo)

            # Crear cada opcion de modelo
            strOpcionModelo = ''
            for mod in Modelo.objects.filter(aplicacion = aplicacion,padre ='nada'):
                if mod.modeloenmenu:
                    if mod.sinbasedatos == False:
                        strOpcionModelo += TextFiles.objects.get(file = "opcion_modelo.html").texto
                        # strOpcionModelo += LeerArchivoEnTexto(dt + 'opcion_modelo.html',etapa,nombre,usuario)
                    else:
                        strOpcionModelo += TextFiles.objects.get(file = "opcion_modelosinbase.html").texto
                        # strOpcionModelo += LeerArchivoEnTexto(dt + 'opcion_modelosinbase.html',etapa,nombre,usuario)
                    strOpcionModelo = strOpcionModelo.replace('@aplicacion',aplicacion.nombre)
                    strOpcionModelo = strOpcionModelo.replace('@modelo',mod.nombre)
                    strOpcionModelo = strOpcionModelo.replace("@tooltip",mod.tooltip)
                    try:
                        if mod.imagenmenu:
                            strOpcionModelo = strOpcionModelo.replace("@avatar",mod.nombre + '.png')
                            strOpcionModelo = strOpcionModelo.replace("@hidden",'')
                            CopiaImagenes(directorio + nombre + "/core/static/core/img/" + mod.nombre + '.png', 'proyectos', mod.imagenmenu.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )
                        else:
                            h= "hidden=" + '"' + "true" + '"'
                            strOpcionModelo = strOpcionModelo.replace("@avatar",'')
                            strOpcionModelo = strOpcionModelo.replace("@hidden",h)
                    except:
                        pass
                    if mod.textoopcionmenu == '':
                        mod.textoopcionmenu = mod.nombre
                        mod.save()
                    strOpcionModelo = strOpcionModelo.replace('@opcionmodelo',mod.textoopcionmenu)
            strMenuModelo = strMenuModelo.replace('@opciones',strOpcionModelo)

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'menu_' + aplicacion.nombre + '.html',directorio + nombre + '/core/templates/core/includes/',strMenuModelo,nombre,etapa,usuario)

            # EscribirArchivo(directorio + nombre + '/core/templates/core/includes/menu_' + aplicacion.nombre + '.html' ,etapa,nombre,strMenuModelo,True)

    # Grabar el menu core
    strMenu = strMenu.replace('@opciones',strOpcionAplicacion)

    ProcesoPersonalizacion(proyecto,appCore.nombre,'menu_core.html',directorio + nombre + '/core/templates/core/includes/',strMenu,nombre,etapa,usuario)

    # EscribirArchivo(directorio + nombre + '/core/templates/core/includes/menu_core.html',etapa,nombre,strMenu,True)

    # if proyecto.conseguridad:
    #     # Leer el archivo seguridad.html de textfiles
    #     strApp += LeerArchivoEnTexto(dt + "registration/conseguridad.html",etapa,nombre)
    #     strApp = strApp.replace("@aplicacion",'aplicaciones')

    stri = stri.replace("@menu_aplicaciones",strApp)
    stri = stri.replace("@menu_modelos",strVolver)

    # Crear la seguridad en base.html
    strseg = ''
    if proyecto.conseguridad:
        # Leer el archivo seguridad.html de textfiles
        strseg = TextFiles.objects.get(file = "registration/conseguridad.html").texto
        # strseg = LeerArchivoEnTexto(dt + "registration/conseguridad.html",etapa,nombre,usuario)
    stri = stri.replace('@seguridad',strseg)

    # Crear la busqueda en base.html
    strseg = ''
    if proyecto.conbusqueda:
        # Leer el archivo seguridad.html de textfiles
        if proyecto.menuscontiguos:
            strseg = TextFiles.objects.get(file = "conbusqueda_contiguo.html").texto
        else:
            strseg = TextFiles.objects.get(file = "conbusqueda.html").texto
        # strseg = LeerArchivoEnTexto(dt + "conbusqueda.html",etapa,nombre,usuario)
    stri = stri.replace('@busqueda',strseg)

    stri = stri.replace("@numerocolumnabusqueda",str(proyecto.numerocolumnabusqueda))

    if proyecto.numerocolumnabusqueda > 0:
        stri = stri.replace("@12numerocolumnabusqueda",str(12))

    stri = stri.replace("@12numerocolumnabusqueda",str(0))

    # separacion secciones
    stri = stri.replace("@separacion",str(proyecto.separacionsecciones))

    # Grabar el archivo base.html
    ProcesoPersonalizacion(proyecto,appCore.nombre,'base.html',directorio + nombre + "/core/templates/core/",stri,nombre,etapa,usuario)

    # EscribirArchivo(directorio + nombre + "/core/templates/core/base.html",etapa,nombre, stri,True)

    # HOME
    # Copiar el archivo home.html
    stri = TextFiles.objects.get(file = "home.html").texto
    # stri = LeerArchivoEnTexto(dt + "home.html",etapa,nombre,usuario)
    stra= ''
    if proyecto.imagenmedio:
        stra = "<img src=" + '"' + "{% static 'core/img/imagen-medio.png' %}" + '"' + " alt=" + '"' + '"' + " style=" + '"' + "width: 100%;height: 100%;" + '"' + ">" + "\n"
        stri = stri.replace("@imagenmedio",stra)
    else:
        stra = "<span class=" + '"' + "textomedio" + '"' + ">@textomedio</span>" + "\n"
        stra=stra.replace("@textomedio",proyecto.textomedio)
        stri = stri.replace("@imagenmedio",stra)

    ProcesoPersonalizacion(proyecto,appCore.nombre,'home.html',directorio + nombre + "/core/templates/core/",stri,nombre,etapa,usuario)

    # EscribirArchivo(directorio + nombre + "/core/templates/core/home.html",etapa,nombre, stri,True)

    # CSS
    # Leer el archivo estilos.css
    stri = TextFiles.objects.get(file = "estilos.css").texto
    # stri = LeerArchivoEnTexto(dt + "estilos.css",etapa,nombre,usuario)

    # Color de la pagina principal
    stri = stri.replace("@colorpaginaprincipal",str(proyecto.colorpaginaprincipal))

    # Tamanio del logo del proyecto
    stri = stri.replace("@alto-logo",str(proyecto.avatarheight))
    stri = stri.replace("@ancho-logo",str(proyecto.avatarwidth))
    # stri = stri.replace("@horizontallogo",str(proyecto.justificacionhorizontallogo))
    # stri = stri.replace("@verticallogo",str(proyecto.justificacionverticallogo))

    # font del menu
    stri = AsignaFonts(proyecto.fontmenu,'menu',stri)
    stri = stri.replace('@coloropcionmenu',proyecto.colormenu)

    # Font del titulo
    stri = AsignaFonts(proyecto.fonttitulo,'titulo',stri)
    stri = stri.replace('@colortitulo',proyecto.colortitulo)
    # stri = stri.replace("@horizontaltitulo",str(proyecto.justificacionhorizontaltitulo))
    # stri = stri.replace("@verticaltitulo",str(proyecto.justificacionverticaltitulo))

    # Alto de filas y columnas
    # stri = stri.replace("@alto-fila-encabezado", str(proyecto.altofilaencabezado))
    # stri = stri.replace("@alto-columna-encabezado", str(proyecto.altocolumnaencabezado))
    stri = NumeroPorcentaje('@alto-fila-enizcede',proyecto.altofilaenizcede,stri)
    stri = NumeroPorcentaje('@alto-columna-enizquierda',proyecto.altocolumnaenizquierda,stri)
    # stri = stri.replace("@alto-fila-enizcede", str(proyecto.altofilaenizcede))
    # stri = stri.replace("@alto-columna-enizquierda", str(proyecto.altocolumnaenizquierda))
    # stri = stri.replace("@alto-columna-encentro", str(proyecto.altocolumnaencentro))
    # stri = stri.replace("@alto-fila-lotilo", str(proyecto.altofilalotilo))
    stri = NumeroPorcentaje('@alto-columna-logo',proyecto.altocolumnalogo,stri)
    # stri = stri.replace("@alto-columna-logo", str(proyecto.altocolumnalogo))
    stri = NumeroPorcentaje("@alto-columna-titulo", proyecto.altocolumnatitulo,stri)
    # stri = stri.replace("@alto-columna-titulo", str(proyecto.altocolumnatitulo))
    stri = NumeroPorcentaje("@alto-columna-login", proyecto.altocolumnalogin,stri)
    # stri = stri.replace("@alto-columna-login", str(proyecto.altocolumnalogin))
    stri = NumeroPorcentaje("@alto-columna-enderecha", proyecto.altocolumnaenderecha,stri)
    # stri = stri.replace("@alto-columna-enderecha", str(proyecto.altocolumnaenderecha))
    stri = NumeroPorcentaje("@alto-fila-bume", proyecto.altofilabume,stri)
    # stri = stri.replace("@alto-fila-bume", str(proyecto.altofilabume))
    stri = NumeroPorcentaje("@alto-columna-busqueda", proyecto.altocolumnabusqueda,stri)
    # stri = stri.replace("@alto-columna-busqueda", str(proyecto.altocolumnabusqueda))
    stri = NumeroPorcentaje("@alto-columna-menu", proyecto.altocolumnamenu,stri)
    # stri = stri.replace("@alto-columna-menu", str(proyecto.altocolumnamenu))
    stri = NumeroPorcentaje("@alto-fila-medio", proyecto.altofilamedio,stri)
    # stri = stri.replace("@alto-fila-medio", str(proyecto.altofilamedio))
    stri = NumeroPorcentaje("@alto-columna-medio-izquierda", proyecto.altocolumnamedioizquierda,stri)
    # stri = stri.replace("@alto-columna-medio-izquierda", str(proyecto.altocolumnamedioizquierda))
    stri = NumeroPorcentaje("@alto-columna-medio-centro", proyecto.altocolumnamediocentro,stri)
    # stri = stri.replace("@alto-columna-medio-centro", str(proyecto.altocolumnamediocentro))
    stri = NumeroPorcentaje("@alto-columna-medio-derecha", proyecto.altocolumnamedioderecha,stri)
    # stri = stri.replace("@alto-columna-medio-derecha", str(proyecto.altocolumnamedioderecha))
    stri = NumeroPorcentaje("@alto-fila-pie", proyecto.altofilapie,stri)
    # stri = stri.replace("@alto-fila-pie", str(proyecto.altofilapie))
    stri = NumeroPorcentaje("@alto-columna-pie", proyecto.altocolumnapie,stri)
    # stri = stri.replace("@alto-columna-pie", str(proyecto.altocolumnapie))
    stri = NumeroPorcentaje("@alto-columna-bume-derecha",proyecto.altocolumnabumederecha,stri)
    stri = NumeroPorcentaje("@alto-columna-bume-izquierda", proyecto.altocolumnabumeizquierda,stri)
    # stri = stri.replace("@alto-columna-bume-derecha", str(proyecto.altocolumnabumederecha))
    # stri = stri.replace("@alto-columna-bume-izquierda", str(proyecto.altocolumnabumeizquierda))


    # Color de fondo de la columna principal del encabezado
    # stri = stri.replace("@color-fila-encabezado", proyecto.colorfilaencabezado)
    # stri = stri.replace("@color-columna-encabezado", proyecto.colorcolumnaencabezado)
    stri = stri.replace("@color-fila-enizcede", proyecto.colorfilaenizcede)
    stri = stri.replace("@color-columna-enizquierda", proyecto.colorcolumnaenizquierda)
    # stri = stri.replace("@color-columna-encentro", proyecto.colorcolumnaencentro)
    # stri = stri.replace("@color-fila-lotilo", proyecto.colorfilalotilo)
    stri = stri.replace("@color-columna-logo", proyecto.colorcolumnalogo)
    stri = stri.replace("@color-columna-titulo", proyecto.colorcolumnatitulo)
    stri = stri.replace("@color-columna-login", proyecto.colorcolumnalogin)
    stri = stri.replace("@color-columna-enderecha", proyecto.colorcolumnaenderecha)
    stri = stri.replace("@color-fila-bume", proyecto.colorfilabume)
    stri = stri.replace("@color-columna-busqueda", proyecto.colorcolumnabusqueda)
    stri = stri.replace("@color-columna-menu", proyecto.colorcolumnamenu)
    stri = stri.replace("@color-menu", proyecto.colormenu)
    stri = stri.replace("@color-fila-medio", proyecto.colorfilamedio)
    stri = stri.replace("@color-columna-medio-izquierda", proyecto.colorcolumnamedioizquierda)
    stri = stri.replace("@color-columna-medio-centro", proyecto.colorcolumnamediocentro)
    stri = stri.replace("@color-columna-medio-derecha", proyecto.colorcolumnamedioderecha)
    stri = stri.replace("@color-fila-pie", proyecto.colorfilapie)
    stri = stri.replace("@color-columna-pie", proyecto.colorcolumnapie)
    stri = stri.replace("@color-columna-bume-izquierda", proyecto.colorcolumnabumeizquierda)
    stri = stri.replace("@color-columna-bume-derecha", proyecto.colorcolumnabumederecha)

    # Bordes
    strBorde = str(proyecto.enanchoborde) + 'pt solid ' + proyecto.encolorborde
    if (proyecto.enborde and proyecto.numerocolumnaenizquierda == 0) or not proyecto.enborde:
        stri = stri.replace("@enbordei", 'none')
    stri = stri.replace("@enbordei", strBorde)

    if (proyecto.enborde and proyecto.numerocolumnaenderecha == 0) or not proyecto.enborde:
        stri = stri.replace("@enborded", 'none')
    stri = stri.replace("@enborded", strBorde)

    if (proyecto.enborde and proyecto.numerocolumnalogo == 0) or not proyecto.enborde:
        stri = stri.replace("@enbordel", 'none')
    stri = stri.replace("@enbordel", strBorde)

    if (proyecto.enborde and proyecto.numerocolumnatitulo == 0) or not proyecto.enborde:
        stri = stri.replace("@enbordet", 'none')
    stri = stri.replace("@enbordet", strBorde)

    if (proyecto.enborde and proyecto.numerocolumnalogin == 0) or not proyecto.enborde:
        stri = stri.replace("@enbordea", 'none')
    stri = stri.replace("@enbordea", strBorde)

    strBorde = str(proyecto.bumeanchoborde) + 'pt solid ' + proyecto.bumecolorborde
    if (proyecto.bumeborde and proyecto.numerocolumnabumeizquierda == 0) or not proyecto.bumeborde:
        stri = stri.replace("@bumebordei", 'none')
    stri = stri.replace("@bumebordei", strBorde)

    if (proyecto.bumeborde and proyecto.numerocolumnabumederecha == 0) or not proyecto.bumeborde:
        stri = stri.replace("@bumeborded", 'none')
    stri = stri.replace("@bumeborded", strBorde)

    if (proyecto.bumeborde and proyecto.numerocolumnabusqueda == 0) or not proyecto.bumeborde:
        stri = stri.replace("@bumebordeb", 'none')
    stri = stri.replace("@bumebordeb", strBorde)

    if (proyecto.bumeborde and proyecto.numerocolumnamenu == 0) or not proyecto.bumeborde:
        stri = stri.replace("@bumebordem", 'none')
    stri = stri.replace("@bumebordem", strBorde)

    strBorde = str(proyecto.cenanchoborde) + 'pt solid ' + proyecto.cencolorborde
    if (proyecto.cenborde and proyecto.numerocolumnamedioizquierda == 0) or not proyecto.cenborde:
        stri = stri.replace("@cenbordei", 'none')
    stri = stri.replace("@cenbordei", strBorde)

    if (proyecto.cenborde and proyecto.numerocolumnamediocentro == 0) or not proyecto.cenborde:
        stri = stri.replace("@cenbordec", 'none')
    stri = stri.replace("@cenbordec", strBorde)

    if (proyecto.cenborde and proyecto.numerocolumnamedioderecha == 0) or not proyecto.cenborde:
        stri = stri.replace("@cenborded", 'none')
    stri = stri.replace("@cenborded", strBorde)

    
    # Dimensiones img logo y titulo
    stri = stri.replace("@avatarheight", str(proyecto.avatarwidth))
    stri = stri.replace("@imagentitulowidth", str(proyecto.imagentitulowidth))
    stri = stri.replace("@avatarheight", str(proyecto.avatarheight))
    stri = stri.replace("@imagentituloheight", str(proyecto.imagentituloheight))

    # Opcion de Busqueda
    # Copiar el archivo lupa.png
    CopiarArchivos(dt + "lupa.png",directorio + nombre + "/core/static/core/img/lupa.png",etapa,nombre,usuario,True)

    # Regularizar la posicion del texto de busqueda y del menu
    # stri = stri.replace('@posYfila-bume', str(int(proyecto.altofilabume/2 - 25/2)))
    stri = stri.replace('@posYfila-bume', str(0))

    # Texto medio
    stri = AsignaFonts(proyecto.fonttextomedio,'textomedio',stri)
    stri = stri.replace("@color-texto-medio", str(proyecto.colortextomedio))
    
    # Imagen o texto de volver en pantallas de update
    strTextoVolver = proyecto.textovolver
    if proyecto.imagenvolver:
        strTextoVolver = "<img height=" + '"' + "25px" + '"' + " widht=" + '"' + "25px" + '"' + "alt=" + dc + dc + " src=" + dc + "{% static 'core/img/volver.png' %}" + dc + ">" + "\n"
        CopiaImagenes(directorio + nombre + "/core/static/core/img/volver.png", 'proyectos', proyecto.imagenvolver.url,directoriogenesis + 'media/proyectos/',nombre,etapa,usuario,True )
    else:
        strTextoVolver = "<span class=" + '"' + "volver" + '"' + ">" + proyecto.textovolver + "</span>"
    stri = AsignaFonts(proyecto.fonttextovolver,'volver',stri)
    stri = stri.replace("@color-volver",proyecto.colortextovolver)

    # css para ckeditor de todas las propiedades RichTextBox
    strckeditor = ".django-ckeditor-widget, .cke_editor_id_@control {" + "\n"
    strckeditor += "width: 100% !important;" + "\n"
    strckeditor += "max-width: 821px !important;" "\n"
    strckeditor += "}" + "\n"
    strcss = ''
    for md in Modelo.objects.filter(proyecto=proyecto):
        for pr in Propiedad.objects.filter(modelo=md):
            if pr.tipo == 'h':
                strcss += strckeditor
                strcss = strcss.replace('@control', pr.nombre )
    stri = stri.replace('@ckeditor', strcss)
    
    ProcesoPersonalizacion(proyecto,appCore.nombre,'estilos.css',directorio + nombre + "/core/static/core/css/",stri,nombre,etapa,usuario)

    # EscribirArchivo(directorio + nombre + "/core/static/core/css/estilos.css",etapa,nombre, stri,True)

    # TEMPLATE DE MODELOS SINBASE
    strSinBasecss = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        if aplicacion.nombre != 'core' and aplicacion.nombre != 'registration':
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if modelo.sinbasedatos != False:
                    strSinBase = TextFiles.objects.get(file = "modelo_sinbase.html").texto
                    # strSinBase = LeerArchivoEnTexto(dt + 'modelo_sinbase.html',etapa,nombre,usuario)
                    strcss = TextFiles.objects.get(file = "modelo_sinbase.css").texto
                    # strcss = LeerArchivoEnTexto(dt + 'modelo_sinbase.css',etapa,nombre,usuario)
                    strSinBase = strSinBase.replace('@aplicacion',aplicacion.nombre)
                    strcss = strcss.replace('@modelo',modelo.nombre)
                    strSinBasecss += strcss
                    strcss = ''
                    ProcesoPersonalizacion(proyecto,aplicacion.nombre,modelo.nombre + "_sinbase.html",directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/",strSinBase,nombre,etapa,usuario)
    ProcesoPersonalizacion(proyecto,appCore.nombre,'modelo_sinbase.css',directorio + nombre + "/core/static/core/css/",strSinBasecss,nombre,etapa,usuario)

    # LISTA DE MODELO RAIZ
    strcssTotal = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        if AplicacionTienePropiedades(aplicacion):                
            if aplicacion.nombre != 'core' and aplicacion.nombre != 'registration':
                for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                    if modelo.sinbasedatos == False:
                        strlr = ''
                        strlt = ''
                        columnashijos = 0
                        if modelo.padre == 'nada':
                            # Leer el archivo modelo_lista.html de tet files
                            strModeloList = TextFiles.objects.get(file = "modelo_list.html").texto
                            # strModeloList = LeerArchivoEnTexto(dt + 'modelo_list.html',etapa,nombre,usuario)
                            strModeloListBusqueda = TextFiles.objects.get(file = "modelo_list_busqueda.html").texto
                            # strModeloListBusqueda=LeerArchivoEnTexto(dt + 'modelo_list_busqueda.html',etapa,nombre,usuario)
                            if modelo.buscadorlista:
                                strModeloList=strModeloList.replace('@busqueda',strModeloListBusqueda)
                            else:
                                strModeloList=strModeloList.replace('@busqueda','')

                            # Lee el archivo css para cada modelo
                            strcss = TextFiles.objects.get(file = "modelo_list.css").texto
                            # strcss = LeerArchivoEnTexto(dt + 'modelo_list.css',etapa,nombre,usuario)
                            # Define el margin top del modelo_list

                            lista = PropiedadesEnLista(modelo,Propiedad)
                            strlt = lista[0]
                            strlr = lista[1]
                            columnashijos = lista[2]

                            # for propiedad in Propiedad.objects.filter(modelo=modelo):
                            #     num = 1
                            #     if propiedad.enlista:
                            #         columnashijos += propiedad.numerocolumnas
                            #         if propiedad.enmobile:
                            #             strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlt += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-flex @justificaciontextocolumna align-self-center @uppercase columna-@nombrecolumnapropiedad">' + '\n'
                            #             strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #         else:
                            #             strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlt += '\t\t\t<div class="d-none col-md-@numerocolumnas d-flex @justificaciontextocolumna align-self-center @uppercase columna-@nombrecolumnapropiedad">' + '\n'
                            #             strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #         strlt += '\t\t\t\t@textocolumnapropiedad' + '\n'
                            #         strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #         num += 1
                            #         strlt += '\t\t\t</div>' + '\n'
                            #         strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #         num += 1

                            #         if propiedad.enmobile:
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-flex @justificaciontextocolumna dato-@nombrecolumnapropiedad">' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #         else:
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-none col-@numerocolumnas d-flex @justificaciontextocolumna dato-@nombrecolumnapropiedad">' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1


                            #         if propiedad.tipo == 'r':
                            #             strlb = propiedad.textobotones.split(';')
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             for txc in strlb:
                            #                 tx = txc.split(',')
                            #                 strlr += '{% if obj.' + propiedad.nombre + ' == ' + "'" + tx[0] + "'" + ' %}' + tx[1] + '{% endif %}' + '\n'
                            #             strlr += '\t\t\t</div>' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #         elif propiedad.tipo != 'p':
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t\t{{obj.@nombrepropiedad@formatofecha}}' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t</div>' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #         else:
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t\t{% if obj.@nombrepropiedad %}' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t\t\t<img src="{{obj.@nombrepropiedad.url}}" width="20px" height="20px" alt="">' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t\t{% endif %}' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                            #             strlr += '\t\t\t</div>' + '\n'
                            #             strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                            #             num += 1
                                        
                            #         strlr = strlr.replace('@formatofecha', propiedad.formatofecha)
                            #         strlt = strlt.replace('@numerocolumnas', str(propiedad.numerocolumnas))
                            #         strlr = strlr.replace('@numerocolumnas', str(propiedad.numerocolumnas))
                            #         strlr = strlr.replace('@nombrepropiedad', propiedad.nombre)

                            #         # Textos de columna
                            #         if propiedad.textocolumna != '':
                            #             strlt = strlt.replace('@textocolumnapropiedad', propiedad.textocolumna)
                            #         else:
                            #             strlt = strlt.replace('@textocolumnapropiedad', propiedad.nombre)
                            #         strlt = strlt.replace('@nombrecolumnapropiedad', propiedad.nombre)
                            #         strlr = strlr.replace('@nombrecolumnapropiedad', propiedad.nombre)

                            #         # Mayusculas columna
                            #         strlt = UpperLower(modelo.mayusculascolumnas,'@uppercase',strlt)
                            #         # if modelo.mayusculascolumnas:
                            #         #     strlt = strlt.replace('@uppercase', 'text-uppercase')
                            #         # else:
                            #         #     strlt = strlt.replace('@uppercase', '')

                            #         #justificacion columnas
                            #         strlt = AsignaJustificacion('h',propiedad.justificaciontextocolumna,'@justificaciontextocolumna',strlt)
                            #         strlr = AsignaJustificacion('h',propiedad.justificaciontextocolumna,'@justificaciontextocolumna',strlr)

                            strModeloList = strModeloList.replace('@listatitulos', strlt)
                            strModeloList = strModeloList.replace('@listaregistros', strlr)

                            # resto de columnas
                            strModeloList = strModeloList.replace('@restocolumnas', str(10-columnashijos))

                            # TITULO DE LA LISTA
                            try:
                                strcss = AsignaFonts(modelo.fonttitulolista,'titulolista',strcss)
                            except:
                                strcss = AsignaFonts('Arial,10,normal','titulolista',strcss)

                            strcss = strcss.replace('@colortitulolista', modelo.colortitulolista)
                            strcss = strcss.replace('@colorfondotitulolista', modelo.colorfondotitulolista)
                            strcss = NumeroPorcentaje('@altotitulolista', modelo.altotitulolista,strcss)
                            # strcss = strcss.replace('@altotitulolista', str(modelo.altotitulolista))

                            strModeloList = strModeloList.replace('@titulolista', modelo.titulolista)
                            strModeloList = UpperLower(modelo.mayusculastitulolista,'@uppercasetitulo',strModeloList)
                            # if modelo.mayusculastitulolista:
                            #     strModeloList = strModeloList.replace('@uppercasetitulo', 'text-uppercase')
                            # else:
                            #     strModeloList = strModeloList.replace('@uppercasetitulo', '')

                            strModeloList = AsignaJustificacion('h', modelo.justificacionhorizontaltitulolista,'@justificacionhorizontaltitulolista',strModeloList)
                            strModeloList = AsignaJustificacion('v', modelo.justificacionverticaltitulolista,'@justificacionverticaltitulolista',strModeloList)

                            # COMENTARIO LISTA
                            strcss = strcss.replace('@colorfondocomentariolista', modelo.colorfondocomentariolista)
                            strcss = strcss.replace('@colorcomentariolista', modelo.colorcomentariolista)
                            strModeloList = strModeloList.replace('@comentariolista', modelo.comentariolista)

                            try:
                                strcss = AsignaFonts(modelo.fontcomentariolista,'comentariolista',strcss)
                            except:
                                strcss = AsignaFonts('Arial,10,normal','comentariolista',strcss)

                            #COLUMNAS DE LA LISTA
                            strcss = strcss.replace('@colorfondocolumnaslista', modelo.colorfondocolumnaslista)
                            strcss = strcss.replace('@colorcolumnaslista', modelo.colorcolumnaslista)
                            strcss = strcss.replace('@altocolumnaslista', str(modelo.altocolumnas))

                            try:
                                strcss = AsignaFonts(modelo.fontcolumnaslista,'columnaslista',strcss)
                            except:
                                strcss = AsignaFonts('Arial,10,normal','columnaslista',strcss)

                            if modelo.columnaslistaconborde:
                                strModeloList = strModeloList.replace('@conborde', 'border border-primary ')
                            else:
                                strModeloList = strModeloList.replace('@conborde', '')

                            # DATOS LISTA
                            try:
                                strcss = AsignaFonts(modelo.fonttextolista,'textolista',strcss)
                            except:
                                strcss = AsignaFonts('Arial,10,normal','textolista',strcss)

                            strcss = strcss.replace('@colortextolista', modelo.colortextolista)
                            strcss = strcss.replace('@colorfondotextolista', modelo.colorfondotextolista)

                            strModeloList = strModeloList.replace('@listacolumnas', strlt)
                            strModeloList = strModeloList.replace('@listadatos', strlr)
                            strModeloList = strModeloList.replace('@modelo', modelo.nombre)
                            strModeloList = strModeloList.replace('@aplicacion', aplicacion.nombre)

                            # EDITAR BORRAR
                            try:
                                strcss = AsignaFonts(modelo.fonteditarborrar,'editarborrar',strcss)
                            except:
                                strcss = AsignaFonts('Arial,10,normal','editarborrar',strcss)

                            strcss = strcss.replace('@coloreditarborrar', modelo.coloreditarborrar)
                            strModeloList = AsignaTexto(modelo.textoeditarborrar,"editar,borrar","@textoeditar,@textoborrar",strModeloList)

                            #link nuevo
                            try:
                                strcss = AsignaFonts(modelo.fontlinknuevomodelo,'nuevomodelo',strcss)
                            except:
                                strcss = AsignaFonts('Arial,10,normal','nuevomodelo',strcss)


                            strcss = strcss.replace('@colorlinknuevomodelo', modelo.colorlinknuevomodelo)
                            strModeloList = strModeloList.replace('@textolinknuevomodelo', modelo.textolinknuevomodelo)

                            #link boton
                            if modelo.linknuevomodelo:
                                strModeloList = strModeloList.replace('@linknuevomodelo', 'btn btn-block btn-' + modelo.colorbotonlinknuevomodelo)
                            else:
                                strModeloList = strModeloList.replace('@linknuevomodelo', '')

                            # Forma el css total del proyecto
                            strcss = strcss.replace('@modelo',modelo.nombre)
                            strcssTotal += strcss

                            # # Sin lineas de personalizacion
                            # if not proyecto.conetiquetaspersonalizacion:
                            #     strModeloList = QuitaLineasPersonalizacion(strModeloList)                
                            # strModeloList = EscribePersonalizacion(proyecto,aplicacion,modelo.nombre + '_list.html',strModeloList)

                            ProcesoPersonalizacion(proyecto,aplicacion.nombre,modelo.nombre + "_list.html",directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/",strModeloList,nombre,etapa,usuario)

                        # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/" + modelo.nombre + "_list.html" ,etapa,nombre, strModeloList,True)
    
    # Escribir el archivo css del proyecto correspondiente al modelo list
    ProcesoPersonalizacion(proyecto,appCore.nombre,'modelo_list.css',directorio + nombre + "/core/static/core/css/",strcssTotal,nombre,etapa,usuario)

    # EscribirArchivo(directorio + nombre + "/core/static/core/css/modelo_list.css",etapa, nombre,strcssTotal,True)

    # CREAR EL TEMPLATE DE INSERCION POR MODELOS
    strcssTotal = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        if AplicacionTienePropiedades(aplicacion) and aplicacion.nombre!= 'core' and aplicacion.nombre != 'registration':                
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if modelo.sinbasedatos == False:
                    # Leer el archivo modelo_lista.html de tet files
                    strModeloInserta = TextFiles.objects.get(file = "modelo_inserta.html").texto
                    # strModeloInserta = LeerArchivoEnTexto(dt + 'modelo_inserta.html',etapa,nombre,usuario)
                    # Lee el archivo css para cada modelo
                    strcss = TextFiles.objects.get(file = "modelo_inserta.css").texto
                    # strcss = LeerArchivoEnTexto(dt + 'modelo_inserta.css',etapa,nombre,usuario) 
                    strcss = strcss.replace('@modelo',modelo.nombre)
                    strModeloInserta = strModeloInserta.replace('@modelo', modelo.nombre)
                    strModeloInserta = strModeloInserta.replace('@aplicacion', aplicacion.nombre)
                    
                    # codigo para el Titulo del form
                    stra = ''
                    if modelo.padre == 'nada':
                        stra += modelo.tituloinserta + '\n'
                    else:    
                        modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada': # el modelo es nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            stra += '<div class="" style="float: left;">Nuevo modelo: &nbsp@modelo&nbsp&nbsp</div>' + '\n'
                            stra += '<div class=""><a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}?@modeloabuelo_id={{@modeloabuelo_id}}">(Volver)</a></div>' + '\n'
                            stra = stra.replace('@modeloabuelo', modelo_abuelo.nombre)        
                        else: # el modelo es hijo
                            stra += '<div class="" style="float: left">Nuevo modelo: &nbsp@modelo</div>' + '\n'
                            stra += '<div class="" >&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}">(Volver)</a></div>' + '\n'
                        stra = stra.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)        
                        stra = stra.replace('@modelopadre', modelo_padre.nombre)        
                    stra = stra.replace('@modelo', modelo.nombre)        
                    strModeloInserta = strModeloInserta.replace('@tituloinserta', stra)

                    #titulo pagina
                    strcss = AsignaFonts(modelo.fonttituloinserta,'tituloinserta',strcss)
                    strcss = strcss.replace('@colortituloinsertF2@a', modelo.colortituloinserta)
                    strcss = NumeroPorcentaje('@altofilatituloinserta', modelo.altofilatituloinserta,strcss)
                    # strcss = strcss.replace('@altofilatituloinserta', str(modelo.altofilatituloinserta))
                    strcss = strcss.replace('@colorfondofilatituloinserta', modelo.colorfondofilatituloinserta)
                    strcss = strcss.replace('@colorfondotituloinserta', modelo.colorfondotituloinserta)

                    # Justificacion titulo inserta
                    strModeloInserta = AsignaJustificacion('h', modelo.justificacionhorizontaltituloinserta,'@justificacionhorizontaltituloinserta',strModeloInserta)
                    strModeloInserta = AsignaJustificacion('v', modelo.justificacionverticaltituloinserta,'@justificacionverticaltituloinserta',strModeloInserta)

                    #comentario pagina
                    strcss = AsignaFonts(modelo.fontcomentarioinserta,'comentarioinserta',strcss)
                    strcss = strcss.replace('@colorcomentarioinserta', modelo.colorcomentarioinserta)
                    strcss = strcss.replace('@colorfondocomentarioinserta', modelo.colorfondocomentarioinserta)
                    strcss = strcss.replace('@colorlabel' + modelo.nombre, modelo.colorlabelmodelo)
                    strModeloInserta = strModeloInserta.replace('@comentarioinserta', modelo.comentarioinserta)

                    # columnas que organizan el cuerpo en insercion
                    strModeloInserta = strModeloInserta.replace('@numerocolumnasizquierdainserta', str(modelo.numerocolumnasizquierdainserta))
                    strModeloInserta = strModeloInserta.replace('@numerocolumnasmodeloinserta', str(modelo.numerocolumnasmodeloinserta))
                    strModeloInserta = strModeloInserta.replace('@numerocolumnasderechainserta', str(modelo.numerocolumnasderechainserta))

                    texto = Etiquetas(modelo,strModeloInserta,strcss)
                    strModeloInserta =  texto[0]
                    strcss = texto[1]

                    strcssTotal += strcss

                    # strModeloInserta = EscribePersonalizacion(proyecto,aplicacion,modelo.nombre + '_form.html',strModeloInserta)

                    #Sin lineas de personalizacion
                    if not proyecto.conetiquetaspersonalizacion:
                        strModeloInserta = QuitaLineasPersonalizacion(strModeloInserta)

                    # Graba el archivo
                    ProcesoPersonalizacion(proyecto,aplicacion.nombre,modelo.nombre + "_form.html",directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/",strModeloInserta,nombre,etapa,usuario)
                    # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/" + modelo.nombre + "_form.html" ,etapa,nombre, strModeloInserta,True)

    # Escribe css total
    ProcesoPersonalizacion(proyecto,appCore.nombre,'modelo_inserta.css',directorio + nombre + "/core/static/core/css/",strcssTotal,nombre,etapa,usuario)
    # EscribirArchivo(directorio + nombre + "/core/static/core/css/modelo_inserta.css",etapa, nombre,strcssTotal,True)

    strcssTotal = ''
    strcsshijototal = ''
    # TEMPLATE PARA EL UPDATE DE LOS MODELOS
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        if AplicacionTienePropiedades(aplicacion) and aplicacion.nombre!= 'core' and aplicacion.nombre != 'registration':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if modelo.sinbasedatos == False:
                    strModeloUpdate= ''
                    if modelo.hijoscontiguos:
                        strModeloUpdate = TextFiles.objects.get(file = "modelo_update_contiguo.html").texto
                        # strModeloUpdate = LeerArchivoEnTexto(dt + 'modelo_update_contiguo.html',etapa,nombre,usuario)
                        strhc = "@listahijos" + '\n'
                        strhc += "     </div>" + '\n'
                        strhc += "     <div class=" + '"' + "col-12 d-none col-md-@numerocolumnasderechaupdate" + '"' + "></div>" + '\n'
                        strhc += "   </div>" + '\n'
                        strhc += "   <div class=" + '"' + "row pie-lista" + '"' + "></div>" + '\n'
                        strhc += "  </div>" + '\n'
                        strModeloUpdate = strModeloUpdate.replace('@update', strhc)
                    else:
                        strModeloUpdate = TextFiles.objects.get(file = "modelo_update_abajo.html").texto
                        # strModeloUpdate = LeerArchivoEnTexto(dt + 'modelo_update_abajo.html',etapa,nombre,usuario)
                        strha  = "    </div>" + '\n'
                        strha += "    <div class=" + '"' + "row" + '"' + ">" + '\n'
                        strha += "       <div class=" + '"' + "col-12 rounded" + '"' + ">" + '\n'
                        strha += "@listahijos" + '\n'      
                        strha += "       </div>" + '\n'
                        strha += "     </div>" + '\n'
                        strha += "     <div class=" + '"' + "row pie-lista" + '"' + ">" + '\n'
                        strha += "     </div>" + '\n'
                        strha += "    </div>" + '\n'
                        strModeloUpdate = strModeloUpdate.replace('@update', strha)
                    # Lee el archivo css para cada modelo
                    strcss = TextFiles.objects.get(file = "modelo_update.css").texto
                    # strcss = LeerArchivoEnTexto(dt + 'modelo_update.css',etapa,nombre,usuario)
                    strcss = strcss.replace('@modelo',modelo.nombre)
                    
                    # for propiedad in Propiedad.objects.filter(modelo=modelo):
                    #     if propiedad.enlista:
                    #         strt = strt.replace('@nombre', modelo.nombre + '.' + propiedad.nombre)
                    #         break

                    # codigo para la referencia del form
                    stra = ''

                    if modelo.padre =='nada': # modelo padre
                        stra = modelo.tituloupdate + "&nbsp;<a href=" + '"' + "{% url '@aplicacion:listar_@modelo' %}" + '"' + "><span style=" + '"' + "color:green" + '"' + ">{{nombre}}</span></a>"
                        # stra = modelo.tituloupdate + '&nbsp;<span style=" + '"' + 'color:green" + '"' + '>{{nombre}}</span>' 
                        # stra = modelo.tituloupdate + '&nbsp;{{nombre}}' 
                    else:
                        modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada': # el modelo es nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            stra += '\t\t\t\t<div class="col">' + '\n'
                            stra += '\t\t\t\t\t<div class="" style="float: left">@modelohijo:&nbsp&nbsp</div>' +'\n'
                            stra += '\t\t\t\t\t<div class="" style="float: left; color:green;"><b>{{nombre}}</b>&nbsp&nbsp</div>' + '\n'
                            stra += '\t\t\t\t\t<div class="" style="float: left;"><a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}?@modeloabuelo_id={{@modeloabuelo_id}}">' + strTextoVolver + '</a></div>' + '\n'
                            stra += '\t\t\t\t</div>'
                            # stra =  modelo.nombre.upper() + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}?@modeloabuelo_id={{@modeloabuelo_id}}">(Volver)</a>'
                            stra = stra.replace('@modeloabuelo', modelo_abuelo.nombre)        
                        else: # el modelo es hijo
                            stra += '\t\t\t\t<div class="col text-center">' + '\n'
                            stra += '\t\t\t\t\t<div class="" style="float: left;">@modelohijo:&nbsp&nbsp</div>&nbsp' + '\n'
                            stra += '\t\t\t\t\t<div class="" style="float: left; color:green;"><b>{{nombre}}&nbsp&nbsp</b></div>' + '\n'
                            stra += '\t\t\t\t\t<div class="" style="float: left"><a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}">' + strTextoVolver + '</a></div>' + '\n'
                            stra += '\t\t\t\t</div>'
                        stra = AplicacionReal(modelo,stra,proyecto)
                        stra = stra.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)        
                        stra = stra.replace('@modelopadre', modelo_padre.nombre)        
                        stra = stra.replace('@modelohijo', modelo.nombre)        

                    stra = stra.replace('@tituloupdate', modelo.tituloupdate)        
                    stra = stra.replace('@modelo', modelo.nombre)        

                    strModeloUpdate = strModeloUpdate.replace('@tituloupdate', stra)

                    #titulo pagina update
                    strcss = AsignaFonts(modelo.fonttituloupdate,'tituloupdate',strcss)
                    strcss = strcss.replace('@colortituloupdate', modelo.colortituloupdate)
                    strcss = NumeroPorcentaje('@altofilatituloupdate', modelo.altofilatituloupdate,strcss)
                    # strcss = strcss.replace('@altofilatituloupdate', str(modelo.altofilatituloupdate))
                    strcss = strcss.replace('@colorfondotituloupdate', modelo.colorfondotituloupdate)
                    strcss = strcss.replace('@colorfondofilatituloupdate', modelo.colorfondofilatituloupdate)

                    # Justificacion titulo update
                    strModeloUpdate = AsignaJustificacion('h', modelo.justificacionhorizontaltituloupdate,'@justificacionhorizontaltituloupdate',strModeloUpdate)
                    strModeloUpdate = AsignaJustificacion('v', modelo.justificacionverticaltituloupdate,'@justificacionverticaltituloupdate',strModeloUpdate)

                    #comentario pagina update
                    strcss = AsignaFonts(modelo.fontcomentarioupdate,'comentarioupdate',strcss)
                    strcss = strcss.replace('@colorcomentarioupdate', modelo.colorcomentarioupdate)
                    strcss = strcss.replace('@colorfondocomentarioupdate', modelo.colorfondocomentarioupdate)
                    strModeloUpdate = strModeloUpdate.replace('@comentarioupdate', modelo.comentarioupdate)

                    # Numero de columnas para organizar la pagina
                    strModeloUpdate = strModeloUpdate.replace('@numerocolumnasizquierdaupdate', str(modelo.numerocolumnasizquierdaupdate))
                    strModeloUpdate = strModeloUpdate.replace('@numerocolumnasmodeloupdate', str(modelo.numerocolumnasmodeloupdate))
                    strModeloUpdate = strModeloUpdate.replace('@numerocolumnasderechaupdate', str(modelo.numerocolumnasderechaupdate))
                    strModeloUpdate = strModeloUpdate.replace('@numerocolumnashijosupdate', str(modelo.numerocolumnashijosupdate))

                    #etiquetas
                    texto = Etiquetas(modelo,strModeloUpdate,strcss)
                    strModeloUpdate =  texto[0]
                    strcss = texto[1]

                    strcssTotal += strcss
                    strcss = ''

                    #lista de modelos hijos
                    strh = ''
                    strBordeHijos = ''
                    strffc = ''
                    for modelohijo in Modelo.objects.filter(padre=modelo.nombre , proyecto = proyecto):
                        # Leer el css para la lista de hijos
                        strcsshijo = TextFiles.objects.get(file = "modelo_list_hijo.css").texto
                        # strcsshijo = LeerArchivoEnTexto(dt + 'modelo_list_hijo.css',etapa,nombre,usuario)
                        strcsshijo = strcsshijo.replace('@modelohijo',modelohijo.nombre)
                        strBordeHijos = 'border'

                        strlh = " \t\t\t<div class=" + '"' + "border rounded mb-3" + '"' + " style=" + '"' + "padding: 5px;" + '"' + ">" + "\n"
                        strlh += "<!-- #@[p_hijo_@hijo_01] -->" + "\n"
                        strlh += '\t\t\t\t<div class="container-fluid lista-@hijo mb-3">' + '\n'
                        strlh += '\t\t\t\t\t<div class="row mt-2 mb-2 fila-titulo-lista-@hijo ">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_02] -->" + "\n"
                        strlh += '\t\t\t\t\t\t<div class="col @justificacionverticaltitulolista @justificacionhorizontaltitulolista @uppercasetitulo">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_03] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t<span class="titulo-lista-@hijo">' + '\n'
                        strlh += '\t\t\t\t\t\t\t\t@titulolista</span>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_04] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t</span>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_05] -->" + "\n"
                        strlh += '\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_06] -->" + "\n"
                        strlh += '\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_07] -->" + "\n"
                        strlh += '\t\t\t\t\t<div class="row mt-2 mb-2 fila-comentario-lista-@hijo ">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_08] -->" + "\n"
                        strlh += '\t\t\t\t\t\t<div class="col @justificacionverticalcomentariolista @justificacionhorizontalcomentariolista @uppercasecomentario">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_09] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t<span class="comentario-lista-@hijo">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_10] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t\t@comentariolista' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_11] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t</span>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_12] -->" + "\n"
                        strlh += '\t\t\t\t\t\t</div>' + '\n'
                        strlh += '\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_13] -->" + "\n"
                        strlh += '\t\t\t\t\t<div class="row fila-columnas-@hijo @uppercasecolumnas" >' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_14] -->" + "\n"
                        strlh += '\t\t\t\t\t\t{% if numero' + modelohijo.nombre + ' > 0 %}' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_15] -->" + "\n"
                        strlh += '@columnashijo' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_16] -->" + "\n"
                        strlh += '\t\t\t\t\t\t{% endif %}' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_17] -->" + "\n"
                        strlh += '\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_18] -->" + "\n"
                        strlh += '\t\t\t\t\t{% for obj in lista@hijo %}' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_19] -->" + "\n"
                        strlh += '\t\t\t\t\t\t<div class="row  fila-datos-@hijo" >' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_20] -->" + "\n"
                        strlh += '@listaregistroshijo' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_21] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t<div class="col-@restocolumnas">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_22] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_23] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t<div class="col-12 col-md-1 mt-1 edita-@hijo">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_24] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t\t@editahijo' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_25] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_26] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t<div class="col-12 col-md-1 ml-2 mt-1 borra-@hijo">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_27] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t\t@borrahijo' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_28] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_29] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t<div class="col-1">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_30] -->" + "\n"
                        strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_31] -->" + "\n"
                        strlh += '\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_32] -->" + "\n"
                        strlh += '\t\t\t\t\t{% endfor %}' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_33] -->" + "\n"
                        strlh += '\t\t\t\t\t<div class="row mt-3 mb-3 fila-nuevo-@hijo">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_34] -->" + "\n"
                        strlh += '\t\t\t\t\t\t<div class="col">' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_35] -->" + "\n"
                        # Ver si tiene modelo abuelo
                        if modelo.padre != 'nada':
                            modelo_abuelo = Modelo.objects.get(nombre = modelo.padre,proyecto=proyecto)
                            strlh += '\t\t\t\t\t\t\t<a class="@linknuevomodelo mt-2" href="{% url ' + "'" + '@aplicacionhijo:crear_@hijo' + "'" + '%}?@modelopadre_id={{ @modelopadre.id }}&@modeloabuelo_id={{ @modeloabuelo_id }}">@textolinknuevomodelo</a>' + '\n' + '\n'
                            strlh = strlh.replace('@modeloabuelo',modelo_abuelo.nombre)
                        else:
                            strlh += '\t\t\t\t\t\t\t<a class="@linknuevomodelo mt-2" href="{% url ' + "'" + '@aplicacionhijo:crear_@hijo' + "'" + '%}?@modelopadre_id={{ @modelopadre.id }}">@textolinknuevomodelo</a>' + '\n' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_36] -->" + "\n"
                        strlh += '\t\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_37] -->" + "\n"
                        strlh += '\t\t\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_38] -->" + "\n"
                        strlh += '\t\t\t\t</div>' + '\n'
                        strlh += '\t\t\t</div>' + '\n'
                        strlh += "<!-- #@[p_hijo_@hijo_39] -->" + "\n"

                        # Titulo lista hijos
                        strcsshijo = AsignaFonts(modelohijo.fonttitulolista,'titulolista' + modelohijo.nombre, strcsshijo)
                        strcsshijo = strcsshijo.replace('@colortitulolista' + modelohijo.nombre, modelohijo.colortitulolista)
                        strcsshijo = strcsshijo.replace('@colorfondotitulolista' + modelohijo.nombre, modelohijo.colorfondotitulolista)
                        strcsshijo = NumeroPorcentaje('@altotitulolista' + modelohijo.nombre, modelohijo.altotitulolista,strcsshijo)
                        # strcsshijo = strcsshijo.replace('@altotitulolista' + modelohijo.nombre, str(modelohijo.altotitulolistahijos))

                        # justificacion vertical titulo lista hijos
                        strlh = AsignaJustificacion('v', modelohijo.justificacionverticaltitulolista, '@justificacionverticaltitulolista', strlh)
                        strlh = AsignaJustificacion('h', modelohijo.justificacionhorizontaltitulolista, '@justificacionhorizontaltitulolista', strlh)

                        strlh = strlh.replace('@titulolista', modelohijo.titulolista)
                        strlh = UpperLower(modelohijo.mayusculastitulolista,'@uppercasetitulo',strlh)

                        # COMENTARIO LISTA HIJOS
                        strcsshijo = strcsshijo.replace('@colorfondocomentariolista' + modelohijo.nombre, modelohijo.colorfondocomentariolista)
                        strcsshijo = strcsshijo.replace('@colorcomentariolista' + modelohijo.nombre, modelohijo.colorcomentariolista)
                        strlh = strlh.replace('@comentariolista', modelohijo.comentariolista)

                        try:
                            strcsshijo = AsignaFonts(modelohijo.fontcomentariolista,'comentariolista' + modelohijo.nombre,strcsshijo)
                        except:
                            strcsshijo = AsignaFonts('Arial,10,normal','comentariolista' + modelohijo.nombre,strcsshijo)

                        # strcsshijo = strcsshijo.replace('@altotitulolista' + modelohijo.nombre, str(modelohijo.altotitulolistahijos))

                        # justificacion vertical titulo lista hijos
                        strlh = AsignaJustificacion('v', modelohijo.justificacionverticaltitulolista, '@justificacionverticaltitulolista', strlh)
                        strlh = AsignaJustificacion('h', modelohijo.justificacionhorizontaltitulolista, '@justificacionhorizontaltitulolista', strlh)

                        strlh = strlh.replace('@titulolista', modelohijo.titulolista)

                        # if modelohijo.mayusculastitulolistahijos:
                        #     strlh = strlh.replace('@uppercase', 'text-uppercase')
                        # else:
                        #     strlh = strlh.replace('@uppercase', '')

                        lista = PropiedadesEnLista(modelohijo,Propiedad)
                        strlth = lista[0]
                        strlrh = lista[1]
                        columnashijos = lista[2]

                        # columnashijos = 0
                        # strlrh = ''
                        # strlth = ''
                        # for propiedadhijo in Propiedad.objects.filter(modelo=modelohijo):
                        #     num = 1
                        #     if propiedadhijo.enlista:
                        #         columnashijos += propiedadhijo.numerocolumnas
                        #         if propiedadhijo.enmobile:
                        #             strlth += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlth += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-flex @justificaciontextocolumna align-self-center @uppercase columna-@nombrecolumnapropiedad">' + '\n'
                        #             strlth += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #         else:
                        #             strlth += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlth += '\t\t\t<div class="col-12 d-none col-md-@numerocolumnas d-flex @justificaciontextocolumna align-self-center @uppercase columna-@nombrecolumnapropiedad">' + '\n'
                        #             strlth += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #         strlth += '\t\t\t\t@textocolumnapropiedad' + '\n'
                        #         strlth += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #         num += 1
                        #         strlth += '\t\t\t</div>' + '\n'
                        #         strlth += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #         num += 1

                        #         if propiedadhijo.enmobile:
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-flex @justificaciontextocolumna dato-@nombrecolumnapropiedad">' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #         else:
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-none col-@numerocolumnas d-flex @justificaciontextocolumna dato-@nombrecolumnapropiedad">' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1


                        #         if propiedadhijo.tipo == 'r':
                        #             strlb = propiedadhijo.textobotones.split(';')
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             for txc in strlb:
                        #                 tx = txc.split(',')
                        #                 strlrh += '{% if objeto.' + propiedadhijo.nombre + ' == ' + "'" + tx[0] + "'" + ' %}' + tx[1] + '{% endif %}' + '\n'
                        #             strlrh += '\t\t\t</div>' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #         elif propiedadhijo.tipo != 'p':
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t\t{{objeto.@nombrepropiedad@formatofecha}}' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t</div>' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #         else:
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t\t{% if objeto.@nombrepropiedad %}' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t\t\t<img src="{{objeto.@nombrepropiedad.url}}" width="20px" height="20px" alt="">' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t\t{% endif %}' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                        #             strlrh += '\t\t\t</div>' + '\n'
                        #             strlrh += '<!-- #@[p_modelo_edit_' + propiedadhijo.nombre + '_' + str(num) + '] -->' + '\n'
                        #             num += 1
                                    
                        #         strlrh = strlrh.replace('@formatofecha', propiedadhijo.formatofecha)
                        #         strlth = strlth.replace('@numerocolumnas', str(propiedadhijo.numerocolumnas))
                        #         strlrh = strlrh.replace('@numerocolumnas', str(propiedadhijo.numerocolumnas))
                        #         strlrh = strlrh.replace('@nombrepropiedad', propiedadhijo.nombre)

                        #         # Textos de columna
                        #         if propiedadhijo.textocolumna != '':
                        #             strlth = strlth.replace('@textocolumnapropiedad', propiedadhijo.textocolumna)
                        #         else:
                        #             strlth = strlth.replace('@textocolumnapropiedad', propiedadhijo.nombre)
                        #         strlth = strlth.replace('@nombrecolumnapropiedad', propiedadhijo.nombre)
                        #         strlrh = strlrh.replace('@nombrecolumnapropiedad', propiedadhijo.nombre)

                        #         # Mayusculas columna
                        #         strlth = UpperLower(modelohijo.mayusculascolumnas,'@uppercase',strlth)
                        #         # if modelo.mayusculascolumnas:
                        #         #     strlt = strlt.replace('@uppercase', 'text-uppercase')
                        #         # else:
                        #         #     strlt = strlt.replace('@uppercase', '')

                        #         #justificacion columnas
                        #         strlth = AsignaJustificacion('h',propiedadhijo.justificaciontextocolumna,'@justificaciontextocolumna',strlth)
                        #         strlrh = AsignaJustificacion('h',propiedadhijo.justificaciontextocolumna,'@justificaciontextocolumna',strlrh)



                        # # Columnas de lista hijos
                        # strlrh = ''
                        # strlth = ''

                        # columnashijos = 0
                        # for propiedadhijo in Propiedad.objects.filter(modelo=modelohijo):
                        #     if propiedadhijo.enlista:
                        #         columnashijos += propiedadhijo.numerocolumnas
                        #         strlth += '\t\t\t\t\t\t\t<div class="col-' + str(propiedadhijo.numerocolumnas) + ' d-flex @justificaciontextocolumna @uppercase align-self-center columna-@hijo-@nombrepropiedad">' + '\n'

                        #         # Textos de columna
                        #         if propiedadhijo.textocolumna != '':
                        #             strlth += '\t\t\t\t\t\t\t\t' + propiedadhijo.textocolumna + '\n'
                        #         else:
                        #             strlth += '\t\t\t\t\t\t\t\t' + propiedadhijo.nombre + '\n'

                        #         # if modelohijo.mayusculascolumnas:
                        #         #     strlth += '\t\t\t\t\t\t\t\t' + propiedadhijo.textocolumna.upper() + '\n'
                        #         # else:
                        #         #     strlth += '\t\t\t\t\t\t\t\t' + propiedadhijo.textocolumna + '\n'

                        #         strlth += '\t\t\t\t\t\t\t</div>' + '\n'

                        #         strlrh += '\t\t\t\t\t\t<div class="col-' + str(propiedadhijo.numerocolumnas) + ' d-flex @justificaciontextocolumna mt-1  datos-@hijo-@nombrepropiedad">' + '\n'
                        #         strlrh += '\t\t\t\t\t\t\t\t{{objeto.' + propiedadhijo.nombre + propiedadhijo.formatofecha + '}}' + '\n'
                        #         strlrh += '\t\t\t\t\t\t</div>' + '\n'

                        #         strlth = AsignaJustificacion('h', propiedadhijo.justificaciontextocolumna,'@justificaciontextocolumna',strlth)
                        #         strlrh = AsignaJustificacion('h', propiedadhijo.justificaciontextocolumna,'@justificaciontextocolumna',strlrh)

                        #         strlth = strlth.replace('@nombrepropiedad',propiedad.nombre)
                        #         strlrh = strlrh.replace('@nombrepropiedad',propiedad.nombre)

                        # Css de columnas lista hijos
                        strcsshijo = AsignaFonts(modelohijo.fontcolumnaslista,"columnaslista" + modelohijo.nombre,strcsshijo)                            
                        strcsshijo = strcsshijo.replace('@colorcolumnaslista' + modelohijo.nombre,modelohijo.colorcolumnaslista)
                        strcsshijo = strcsshijo.replace('@colorfondocolumnaslista' + modelohijo.nombre,modelohijo.colorfondocolumnaslista)
                        strcsshijo = strcsshijo.replace('@altocolumnaslista' + modelohijo.nombre,str(modelohijo.altocolumnas))
                        # Mayusculas columna
                        strlh = UpperLower(modelohijo.mayusculascolumnas,'@uppercasecolumnas',strlh)
                        # if modelo.mayusculascolumnaslistahijos:
                        #     strlth = strlth.replace('@uppercase', 'text-uppercase')
                        # else:
                        #     strlth = strlth.replace('@uppercase', '')

                        # Css de Datos de lista hijos
                        strcsshijo = AsignaFonts(modelohijo.fonttextolista,"textolista" + modelohijo.nombre,strcsshijo)                            
                        strcsshijo = strcsshijo.replace('@colortextolista' + modelohijo.nombre,modelohijo.colortextolista)
                        strcsshijo = strcsshijo.replace('@colorfondotextolista' + modelohijo.nombre,modelohijo.colorfondotextolista)

                        # editar y borrar hijos
                        streh = ''
                        strbh = ''
                        if modelohijo.padre != 'nada': # modelo hijo o nieto
                            modelo_padre = Modelo.objects.get(nombre=modelohijo.padre , proyecto=proyecto)
                            if modelo_padre.padre != 'nada': # modelo nieto
                                modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                                streh += '<a class="editar-borrar-lista-@hijo" href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' obj.id %}?@modelopadre_id={{ @modelopadre_id }}&@modeloabuelo_id={{@modeloabuelo_id}}">@textoeditar</a>' + '\n'
                                strbh += '<a class="editar-borrar-lista-@hijo" href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' obj.id %}?@modelopadre_id={{ @modelopadre_id }}&@modeloabuelo_id={{@modeloabuelo_id}}">@textoborrar</a>' + '\n'
                                streh = streh.replace('@modeloabuelo', modelo_abuelo.nombre)
                                strbh = strbh.replace('@modeloabuelo', modelo_abuelo.nombre)
                            else: # modelo hijo
                                streh += '<a class="editar-borrar-lista-@hijo" href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' obj.id %}?@modelopadre_id={{ @modelopadre_id }}">@textoeditar</a>' + '\n'
                                strbh += '<a class="editar-borrar-lista-@hijo" href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' obj.id %}?@modelopadre_id={{ @modelopadre_id }}">@textoborrar</a>' + '\n'
                            streh = streh.replace('@modelopadre', modelo_padre.nombre)
                            strbh = strbh.replace('@modelopadre', modelo_padre.nombre)
                        else: # modelo sin padre
                            streh += '<a class="font_editar_borrar_lista_hijos_@modelo" href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' obj.id %}?@modelo_id={{ @modelo.id }}">@textoeditar</a>' + '\n'
                            strbh += '<a class="font_editar_borrar_lista_hijos_@modelo" href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' obj.id %}?@modelo_id={{ @modelo.id }}">@textoborrar</a>' + '\n'
                            streh = streh.replace('@modelo', modelohijo.nombre)
                            strbh = strbh.replace('@modelo', modelohijo.nombre)

                        # Encuentra la aplicacion real
                        streh = AplicacionReal(modelohijo,streh,proyecto)
                        strbh = AplicacionReal(modelohijo,strbh,proyecto)

                        #editar borrar
                        strcsshijo = AsignaFonts(modelohijo.fonteditarborrar,'editarborrar' + modelohijo.nombre,strcsshijo)
                        strcsshijo = strcsshijo.replace('@coloreditarborrar' + modelohijo.nombre, modelohijo.coloreditarborrar)

                        #link nuevo
                        try:
                            strcsshijo = AsignaFonts(modelohijo.fontlinknuevomodelo,'nuevomodelo' + modelohijo.nombre,strcsshijo)
                        except:
                            strcsshijo = AsignaFonts('Arial,10,normal','nuevomodelo' + modelohijo.nombre,strcsshijo)

                        strcsshijo = strcsshijo.replace('@colorlinknuevomodelo' + modelohijo.nombre, modelohijo.colorlinknuevomodelo)
                        strlh = strlh.replace('@textolinknuevomodelo', modelohijo.textolinknuevomodelo)

                        #link boton
                        if modelohijo.linknuevomodelo:
                            strlh = strlh.replace('@linknuevomodelo', 'btn btn-block btn-' + modelohijo.colorbotonlinknuevomodelo)
                        else:
                            strlh = strlh.replace('@linknuevomodelo', '')

                        strcsshijototal += strcsshijo
                        strcsshijo = ''


                        streh = AsignaTexto(modelohijo.textoeditarborrar,"editar,borrar","@textoeditar,@textoborrar",streh)
                        strbh = AsignaTexto(modelohijo.textoeditarborrar,"editar,borrar","@textoeditar,@textoborrar",strbh)

                        strlh = strlh.replace('@editahijo', streh)
                        strlh = strlh.replace('@borrahijo', strbh)
                        strlh = strlh.replace('@modelopadre', modelo.nombre)
                        strlh = strlh.replace('@modelohijo', modelohijo.nombre)
                        strlh = strlh.replace('@modelo', modelohijo.nombre)
                        # strlh = strlh.replace('@modelo', modelohijo.nombre)
                        # strlh = strlh.replace('@modelohijo', modelohijo.nombre)
                        # strlh = strlh.replace('@modelopadre', modelo.nombre)
                        strlh = strlh.replace('@hijo', modelohijo.nombre)
                        strlh = strlh.replace('@aplicacionhijo', modelohijo.aplicacion.nombre)
                        strlh = strlh.replace('@columnashijo', strlth)
                        strlh = strlh.replace('@listaregistroshijo', strlrh)
                        strlh = strlh.replace('@restocolumnas', str(9-columnashijos))

                        strh += strlh

                    strModeloUpdate = strModeloUpdate.replace('@listahijos', strh)

                    # strt = EscribePersonalizacion(proyecto,aplicacion,modelo.nombre + '_update_form.html',strt)

                    # #Sin lineas de personalizacion
                    # if not proyecto.conetiquetaspersonalizacion:
                    #     strModeloUpdate = QuitaLineasPersonalizacion(strModeloUpdate)

                    # Reemplazos de modelo y aplicacion
                    strModeloUpdate = strModeloUpdate.replace('@aplicacion', aplicacion.nombre)
                    strModeloUpdate = strModeloUpdate.replace('@modelo', modelo.nombre)

                    # Grabar el html
                    ProcesoPersonalizacion(proyecto,aplicacion.nombre,modelo.nombre + "_update_form.html",directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/",strModeloUpdate,nombre,etapa,usuario)
                    # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/" + modelo.nombre + "_update_form.html" ,etapa,nombre, strModeloUpdate,True)

                # Escribir el css del modelo
                ProcesoPersonalizacion(proyecto,appCore.nombre,'modelo_update.css',directorio + nombre + "/core/static/core/css/",strcssTotal,nombre,etapa,usuario)
                # EscribirArchivo(directorio + nombre + "/core/static/core/css/modelo_update.css",etapa, nombre,strcssTotal,True)

    # Grabar los css de los hijos
    ProcesoPersonalizacion(proyecto,appCore.nombre,'modelo_hijo.css',directorio + nombre + "/core/static/core/css/",strcsshijototal,nombre,etapa,usuario)
    # EscribirArchivo(directorio + nombre + "/core/static/core/css/modelo_hijo.css",etapa, nombre,strcsshijototal,True)

    # DELETE POR CADA MODELO
    strcssTotal = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        if AplicacionTienePropiedades(aplicacion) and aplicacion.nombre!= 'core' and aplicacion.nombre != 'registration':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if modelo.sinbasedatos == False:
                    strcss = TextFiles.objects.get(file = "modelo_borra.css").texto
                    # strcss = LeerArchivoEnTexto(dt + "modelo_borra.css",etapa,nombre,usuario)
                    strcss =  strcss.replace('@modelo', modelo.nombre)
                    strModeloBorra = TextFiles.objects.get(file = "modelo_confirm_delete.html").texto
                    # strModeloBorra = LeerArchivoEnTexto(dt + "modelo_confirm_delete.html",etapa,nombre,usuario)
                    strModeloBorra =  strModeloBorra.replace('@modelo', modelo.nombre)
                    strModeloBorra =  strModeloBorra.replace('@numerocolumnasizquierdaborra', str(modelo.numerocolumnasizquierdaborra))
                    strModeloBorra =  strModeloBorra.replace('@numerocolumnasmodeloborra', str(modelo.numerocolumnasmodeloborra))
                    strModeloBorra =  strModeloBorra.replace('@numerocolumnasderechaborra', str(modelo.numerocolumnasderechaborra))

                    # Justificacion titulo inserta
                    strModeloBorra = AsignaJustificacion('h', modelo.justificacionhorizontaltituloborra,'@justificacionhorizontaltituloborra',strModeloBorra)
                    strModeloBorra = AsignaJustificacion('v', modelo.justificacionverticaltituloborra,'@justificacionverticaltituloborra',strModeloBorra)

                    # Titulo y texto de borrado
                    strModeloBorra =  strModeloBorra.replace('@tituloborra', modelo.tituloborra)
                    strModeloBorra =  strModeloBorra.replace('@textoborra', modelo.textoborra)

                    # cancelar el borrado
                    strcb = ''
                    if modelo.padre != 'nada': # modelo hijo o nieto
                        modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada': # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            strcb = '<a class="btn btn-danger" href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}?@modeloabuelo_id={{@modeloabuelo_id}}">Cancelar</a>'
                            strcb = strcb.replace('@modeloabuelo', modelo_abuelo.nombre)
                        else: # modelo hijo
                            strcb = '<a class="btn btn-danger" href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadre' + "'" + ' @modelopadre_id %}">Cancelar</a>'
                        strcb = strcb.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)
                        strcb = strcb.replace('@modelopadre', modelo_padre.nombre)
                        # Encuentra la aplicacion real
                        strcb = AplicacionReal(modelo,strcb,proyecto)
                    else: # modelo sin padre
                        strcb = '<a class="btn btn-danger" href="{% url ' + "'" + '@aplicacion:listar_@modelo' + "'" + ' %}">Cancelar</a>'
                        strcb = strcb.replace('@aplicacionreal',aplicacion.nombre)
                        strcb = strcb.replace('@aplicacion', Aplicacion.objects.get(id=modelo.aplicacion.id).nombre)

                    #titulo pagina borra
                    strcss = AsignaFonts(modelo.fonttituloborra,'tituloborra',strcss)
                    strcss = strcss.replace('@colortituloborra', modelo.colortituloborra)
                    strcss = NumeroPorcentaje('@altofilatituloborra', modelo.altofilatituloborra,strcss)
                    # strcss = strcss.replace('@altofilatituloborra', str(modelo.altofilatituloborra))
                    strcss = strcss.replace('@colorfondofilatituloborra', modelo.colorfondofilatituloborra)
                    strcss = strcss.replace('@colorfondotituloborra', modelo.colorfondotituloborra)

                    #comentario pagina borra
                    strcss = AsignaFonts(modelo.fontcomentarioborra,'comentarioborra',strcss)
                    strcss = strcss.replace('@colorcomentarioborra', modelo.colorcomentarioborra)
                    strcss = strcss.replace('@colorfondocomentarioborra', modelo.colorfondocomentarioborra)
                    strModeloBorra = strModeloBorra.replace('@comentarioborra', modelo.comentarioborra)

                    #texto pagina borra
                    strcss = AsignaFonts(modelo.fontcomentarioborra,'textoborra',strcss)
                    strcss = strcss.replace('@colortextoborra', modelo.colortextoborra)
                    strcss = strcss.replace('@colorfondotextoborra', modelo.colorfondotextoborra)
                    strModeloBorra = strModeloBorra.replace('@textoborra', modelo.textoborra)

                    strModeloBorra = strModeloBorra.replace('@cancelaborrado', strcb)
                    strModeloBorra = strModeloBorra.replace('@textobotonborrado', modelo.textobotonborra)
                    strModeloBorra = strModeloBorra.replace('@aplicacion', aplicacion.nombre)
                    strModeloBorra = strModeloBorra.replace('@modelo', modelo.nombre)

                    # Actualiza css
                    strcssTotal += strcss

                    # strModeloBorra = EscribePersonalizacion(proyecto,aplicacion,modelo.nombre + '_confirm_delete.html',strModeloBorra)

                    #Sin lineas de personalizacion
                    if not proyecto.conetiquetaspersonalizacion:
                        strModeloBorra = QuitaLineasPersonalizacion(strModeloBorra)

                    # Grabar archivos
                    ProcesoPersonalizacion(proyecto,aplicacion.nombre,modelo.nombre + "_confirm_delete.html",directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/",strModeloBorra,nombre,etapa,usuario)
                    # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/templates/" + aplicacion.nombre + "/" + modelo.nombre + "_confirm_delete.html" ,etapa,nombre, strModeloBorra,True)

    # Grabar los css para el borrado
    ProcesoPersonalizacion(proyecto,appCore.nombre,'modelo_borra.css',directorio + nombre + "/core/static/core/css/",strcssTotal,nombre,etapa,usuario)
    # EscribirArchivo(directorio + nombre + "/core/static/core/css/modelo_borra.css",etapa, nombre,strcssTotal,True)

    # Manejo de los templates de los modelos hijos que son foreign en otros modelos select
    strHtml = TextFiles.objects.get(file = "load_hijo.html").texto
    # strHtml = LeerArchivoEnTexto(dt + "load_hijo.html",etapa,nombre,usuario)
    strAjax = TextFiles.objects.get(file = "ajax_load_hijo.html").texto
    # strAjax = LeerArchivoEnTexto(dt + "ajax_load_hijo.html",etapa,nombre,usuario)
    strData = " data-@modelos-url=" + '"' + "{% url '@aplicacion:ajax_load_@modelos' %}" + '"'
    strTemplate = ''
    for modelo in Modelo.objects.filter(proyecto=proyecto):
        strAjaxForms = ''
        strLoadData = ''
        for propiedad in Propiedad.objects.filter(modelo=modelo):
            if propiedad.tipo == 'f':
                modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea,proyecto=proyecto)
                if modelo_foraneo.padre !='nada':
                    # Ver si el padre esta en el mismo modelo
                    for modelo_padre in Modelo.objects.filter(proyecto=proyecto):
                        if modelo_padre.nombre == modelo_foraneo.padre:
                            # Existe el modelo padre la llave foranea
                            # Crear el url para la lista de modelos hijo
                            strTemplate = strHtml
                            strTemplate = strTemplate.replace('@modelo',modelo_foraneo.nombre)
                            strTemplate = strTemplate.replace('@padre',modelo_padre.nombre)
                            strTemplate = strTemplate.replace('@aplicacion',modelo.aplicacion.nombre)
                            strTemplate = strTemplate.replace('@propiedad',modelo_foraneo.nombreborrar)
                            EscribirArchivo(directorio + nombre + "/" + modelo.aplicacion.nombre + "/templates/" + modelo.aplicacion.nombre + "/load_" + modelo_foraneo.nombre + '.html',etapa,nombre,strTemplate,usuario,True)
                            strAjaxForms += strAjax
                            strAjaxForms = strAjaxForms.replace('@modelo',modelo.nombre)
                            strAjaxForms = strAjaxForms.replace('@padre',modelo_padre.nombre)
                            strAjaxForms = strAjaxForms.replace('@foraneo',modelo_foraneo.nombre)
                            strLoadData += strData
                            strLoadData = strLoadData.replace('@modelo',modelo_foraneo.nombre)
                            strLoadData = strLoadData.replace('@aplicacion',modelo.aplicacion.nombre)
                            break

        # Leer el html de insercion y update del modelo con llaves foraneas
        strh = LeerArchivoEnTexto(directorio + nombre + '/' + modelo.aplicacion.nombre + '/templates/' + modelo.aplicacion.nombre + '/' + modelo.nombre + '_form' + '.html',etapa,nombre,usuario)
        strh = strh.replace('@ajaxhijo',strAjaxForms)
        strh = strh.replace('@loaddata',strLoadData)
        EscribirArchivo(directorio + nombre + "/" + modelo.aplicacion.nombre + "/templates/" + modelo.aplicacion.nombre + "/" + modelo.nombre + '_form.html',etapa,nombre,strh,usuario,True)
        strh = LeerArchivoEnTexto(directorio + nombre + '/' + modelo.aplicacion.nombre + '/templates/' + modelo.aplicacion.nombre + '/' + modelo.nombre + '_update_form' + '.html',etapa,nombre,usuario)
        strh = strh.replace('@ajaxhijo',strAjaxForms)
        strh = strh.replace('@loaddata',strLoadData)
        EscribirArchivo(directorio + nombre + "/" + modelo.aplicacion.nombre + "/templates/" + modelo.aplicacion.nombre + "/" + modelo.nombre + '_update_form.html',etapa,nombre,strh,usuario,True)

def PropiedadesEnLista(modelo,Propiedad):
    strlr = ''
    strlt = ''
    columnashijos = 0
    for propiedad in Propiedad.objects.filter(modelo=modelo):
        num = 1
        if propiedad.enlista:
            columnashijos += propiedad.numerocolumnas
            if propiedad.enmobile:
                strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlt += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-flex @justificaciontextocolumna align-self-center @uppercase columna-@nombrecolumnapropiedad">' + '\n'
                strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
            else:
                strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlt += '\t\t\t<div class="d-none d-md-block col-md-@numerocolumnas align-self-center @uppercase columna-@nombrecolumnapropiedad">' + '\n'
                strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
            strlt += '\t\t\t\t@textocolumnapropiedad' + '\n'
            strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
            num += 1
            strlt += '\t\t\t</div>' + '\n'
            strlt += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
            num += 1

            if propiedad.enmobile:
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t<div class="col-12 col-md-@numerocolumnas d-flex @justificaciontextocolumna dato-@nombrecolumnapropiedad">' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
            else:
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t<div class="d-none d-md-block col-md-@numerocolumnas dato-@nombrecolumnapropiedad">' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1


            if propiedad.tipo == 'r':
                strlb = propiedad.textobotones.split(';')
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                for txc in strlb:
                    tx = txc.split(',')
                    strlr += '{% if obj.' + propiedad.nombre + ' == ' + "'" + tx[0] + "'" + ' %}' + tx[1] + '{% endif %}' + '\n'
                strlr += '\t\t\t</div>' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
            elif propiedad.tipo != 'p':
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t\t{{obj.@nombrepropiedad@formatofecha}}' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t</div>' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
            else:
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t\t{% if obj.@nombrepropiedad %}' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t\t\t<img src="{{obj.@nombrepropiedad.url}}" width="20px" height="20px" alt="">' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t\t{% endif %}' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                strlr += '\t\t\t</div>' + '\n'
                strlr += '<!-- #@[p_modelo_list_' + propiedad.nombre + '_' + str(num) + '] -->' + '\n'
                num += 1
                
            strlr = strlr.replace('@formatofecha', propiedad.formatofecha)
            strlt = strlt.replace('@numerocolumnas', str(propiedad.numerocolumnas))
            strlr = strlr.replace('@numerocolumnas', str(propiedad.numerocolumnas))
            strlr = strlr.replace('@nombrepropiedad', propiedad.nombre)

            # Textos de columna
            if propiedad.textocolumna != '':
                strlt = strlt.replace('@textocolumnapropiedad', propiedad.textocolumna)
            else:
                strlt = strlt.replace('@textocolumnapropiedad', propiedad.nombre)
            strlt = strlt.replace('@nombrecolumnapropiedad', propiedad.nombre)
            strlr = strlr.replace('@nombrecolumnapropiedad', propiedad.nombre)

            # Mayusculas columna
            strlt = UpperLower(modelo.mayusculascolumnas,'@uppercase',strlt)
            # if modelo.mayusculascolumnas:
            #     strlt = strlt.replace('@uppercase', 'text-uppercase')
            # else:
            #     strlt = strlt.replace('@uppercase', '')

            #justificacion columnas
            strlt = AsignaJustificacion('h',propiedad.justificaciontextocolumna,'@justificaciontextocolumna',strlt)
            strlr = AsignaJustificacion('h',propiedad.justificaciontextocolumna,'@justificaciontextocolumna',strlr)

    return (strlt,strlr,columnashijos)

def CrearForms(proyecto,directorio,dt,usuario):

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()

    nombre = proyecto.nombre
    etapa = "CrearForms"

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Copiar el archivo forms.py de text files en el directorio de la aplicacion
        # CopiarArchivos(dt + "forms.py",directorio + nombre + "/" + aplicacion.nombre + "/forms.py",etapa,nombre,usuario,True)

        # Leer forms.py de text files
        stri = TextFiles.objects.get(file = "forms.py").texto
        # stri = LeerArchivo(dt + "forms.py",etapa,nombre,usuario)

        # Para cada modelo
        strt = ''
        strim = ''
        strc = ''
        strform = ''
        strcm = ''

        for modelo in Modelo.objects.filter(aplicacion=aplicacion):

            if modelo.sinbasedatos == False:
                if Propiedad.objects.filter(modelo=modelo).count() > 0:
                    if strim.find('from ' + Aplicacion.objects.get(id=modelo.aplicacion.id).nombre + ".models import " + modelo.nombre) == -1:
                        strim += 'from ' + Aplicacion.objects.get(id=modelo.aplicacion.id).nombre + ".models import " + modelo.nombre + '\n'

                # recorrer propiedades
                strw = ''
                strl = ''
                strf = ''
                strget = ''
                # variable para modelos foreaneos
                for propiedad in Propiedad.objects.filter(modelo=modelo):
                    if propiedad.noestaenformulario == False:
                        if propiedad.tipo == 's':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'x':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Textarea(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'm':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'i':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'l':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'd':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'f':
                            modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea , proyecto=proyecto)
                            if strim.find('from ' + Aplicacion.objects.get(id=modelo_foraneo.aplicacion.id).nombre + '.models import ' + modelo_foraneo.nombre) == -1:
                                strim += 'from ' + Aplicacion.objects.get(id=modelo_foraneo.aplicacion.id).nombre + '.models import ' + modelo_foraneo.nombre + '\n'
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Select(choices=' + modelo_foraneo.nombre + '.objects.all()),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Select(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + '},choices=' + modelo_foraneo.nombre + '.objects.all()),' + '\n'
                        # if propiedad.tipo == 't':
                        #     # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateInput(format="%m/%d/%Y"),' + '\n'
                        #     strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateTimeInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'datepicker form-control  font_control_@modelo mt-1' + "'" + '},format="%m/%d/%Y"),' + '\n'
                        if propiedad.tipo == 'e':
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateInput(format="%m/%d/%Y"),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TimeInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + '},format="%H:%M"),' + '\n'
                        if propiedad.tipo == 'n':
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateInput(format="%m/%d/%Y"),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'datepicker form-control  font_control_@modelo mt-1' + "'" + '},format="%m/%d/%Y"),' + '\n'
                        if propiedad.tipo == 't':
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateInput(format="%m/%d/%Y"),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateTimeInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + '},format="%m/%d/%Y %H:%M"),' + '\n'
                        if propiedad.tipo == 'b':
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.CheckboxInput(),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.CheckboxInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'p':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.ClearableFileInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control-file  font_control_@modelo mt-1' + "'" + '}),' + '\n'
                        if propiedad.tipo == 'r':
                            lista_botones = propiedad.textobotones.split(';')
                            strlb = ''
                            for texto in lista_botones:
                                lista_partes = texto.split(',')
                                strlb += '(' + "'" + lista_partes[0] + "'," + "'" + lista_partes[1] + "')" + ',' + '\n'
                            strc += propiedad.nombre + '_choices = (' + strlb + ')' + '\n'
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.RadioSelect(attrs={' + "'" + 'class' + "'" + ': ' + "'" + 'form-control' + "'" + '},choices=' + propiedad.nombre + '_choices),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.RadioSelect(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'mt-2' + "'" + '},choices=' + propiedad.nombre + '_choices),' + '\n'
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.RadioSelect(choices=' + propiedad.nombre + '_choices),' + '\n'
                        if propiedad.tipo == 'a':
                            lista_botones = propiedad.textobotones.split(';')
                            strlb = ''
                            for texto in lista_botones:
                                lista_partes = texto.split(',')
                                strlb += '(' + "'" + lista_partes[0] + "'," + "'" + lista_partes[1] + "')" + ',' + '\n'
                            strc += propiedad.nombre + '_choices = (' + strlb + ')' + '\n'
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.RadioSelect(attrs={' + "'" + 'class' + "'" + ': ' + "'" + 'form-control' + "'" + '},choices=' + propiedad.nombre + '_choices),' + '\n'
                            # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Select(choices=' + propiedad.nombre + '_choices),' + '\n'
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Select(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + '},choices=' + propiedad.nombre + '_choices),' + '\n'
                        if propiedad.tipo == 'h':
                            strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Textarea(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control  font_control_@modelo mt-1' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'

                        strw = strw.replace('@etiqueta', propiedad.nombre)
                        strw = strw.replace('@textoplaceholder', propiedad.textoplaceholder)
                        strw = strw.replace('@modelo', modelo.nombre)

                        if propiedad.tipo != 'u':
                            strf += "'" + propiedad.nombre + "'" + ','
                            strl += "'" + propiedad.nombre + "':" + "'" + propiedad.etiqueta + "'" + ','

                        # reglas
                        strcm = ''
                        for regla in Regla.objects.filter(propiedad=propiedad):
                            cc = ''
                            for lc in regla.codigo.split('\n'):
                                cc += '\t\t' + lc + '\n'
                            strcm += cc
                            strcm += '\t\t    raise forms.ValidationError(' + "'" + regla.mensaje + "'" + ')' + '\n'

                        if strcm != '':
                            strget = '\t\t' + propiedad.nombre + ' = self.cleaned_data[' + "'" + propiedad.nombre + "'" + ']' + '\n'
                            strget += strcm


                streg = ''
                if strget != '':
                    streg += '\tdef clean(self):' + '\n'
                    streg += strget


                if strw != '':
                    strt = 'class @modeloForm(forms.ModelForm):' + '\n'
                    strt += '#@[p_Meta_@modelo_01]' + '\n'
                    strt += '\tclass Meta:' + '\n'
                    strt += '#@[p_Meta_@modelo_02]' + '\n'
                    strt += '\t\tmodel = @modelo' + '\n'
                    strt += '#@[p_Meta_@modelo_03]' + '\n'
                    strt += '#@[p_fields_@modelo_01]' + '\n'
                    strt += '\t\tfields = (@listafields)' + '\n'
                    strt += '#@[p_fields_@modelo_02]' + '\n'
                    strt += '#@[p_widgets_@modelo_01]' + '\n'
                    strt += '\t\twidgets = {' + '\n'
                    strt += '#@[p_listawidgets_@modelo_01]' + '\n'
                    strt += '@listawidgets' + '\n'
                    strt += '#@[p_listawidgets_@modelo_02]' + '\n'
                    strt += '\t\t}' + '\n'
                    strt += '#@[p_widgets_@modelo_02]' + '\n'
                    strt += '#@[p_labels_@modelo_01]' + '\n'
                    strt += '\t\tlabels = {' + '\n'
                    strt += '#@[p_listalabels_@modelo_01]' + '\n'
                    strt += '\t\t@listalabels' + '\n'
                    strt += '#@[p_listalabels_@modelo_02]' + '\n'
                    strt += '\t\t}' + '\n'
                    strt += '#@[p_labels_@modelo_02]' + '\n'
                    strt += '#@[p_reglas_@modelo_01]' + '\n'
                    strt += '@reglas' + '\n'
                    strt += '#@[p_reglas_@modelo_02]' + '\n'

                    strt = strt.replace('@listafields', strf)
                    strt = strt.replace('@listalabels', strl)
                    strt = strt.replace('@listawidgets', strw)
                    strt = strt.replace('@reglas', streg)
                    strt = strt.replace('@modelo', modelo.nombre)

                    strform += strt + '\n'

                    strf = ''
                    strl = ''
                    strw = ''    

            else:

                strg = ''
                strp = ''
                strt += '#@[p__@modeloForm_01]' + '\n'
                strt += 'class @modeloForm(forms.Form):' + '\n'
                strt += '#@[p__@modeloForm_02]' + '\n'
                strt += '@fields' + '\n'
                strt += '#@[p__@modeloForm_03]' + '\n'
                strt += '@widgets' + '\n'
                strt += '#@[p__@modeloForm_04]' + '\n'
                strt += '\tdef clean(self):' + '\n'
                strt += '#@[p__@modeloForm_05]' + '\n'
                strt += '\t\tcleaned_data = super(@modeloForm, self).clean()' + '\n'
                strt += '#@[p__@modeloForm_06]' + '\n'

                for propiedad in Propiedad.objects.filter(modelo=modelo):
                    if propiedad.noestaenformulario == False:
                        if propiedad.tipo == 't' or propiedad.tipo == 'n':
                            strg += '\t' + propiedad.nombre + '.widget.attrs.update({' + "'" + 'class' + "'" + ': ' + "'" + 'datepicker form-control' + "'" + '})' + '\n'
                        else:
                            strg += '\t' + propiedad.nombre + '.widget.attrs.update({' + "'" + 'class' + "'" + ': ' + "'" + 'form-control' + "'" + '})' + '\n'
                        if propiedad.tipo == 's':
                            strp += '\t' + propiedad.nombre + ' = ' + 'forms.CharField(max_length=' + str(propiedad.largostring) + ')' + '\n'
                        if propiedad.tipo == 'x':
                            strp += '\t' + propiedad.nombre + ' = ' + 'forms.TextField('')' + '\n'
                        if propiedad.tipo == 'm':
                            strp += '\t' + propiedad.nombre + ' =  forms.IntegerField('')' + '\n'
                        if propiedad.tipo == 'i':
                            strp += '\t' + propiedad.nombre + ' =  forms.IntegerField('')' + '\n'
                        if propiedad.tipo == 'l':
                            strp += '\t' + propiedad.nombre + ' =  forms.IntegerField('')' + '\n'
                        if propiedad.tipo == 'd':
                            strp += '\t' + propiedad.nombre + ' =  forms.DecimalField(' + 'decimal_places=2,max_digits=10)' + '\n'
                        if propiedad.tipo == 't':
                            strp += '\t' + propiedad.nombre + ' =  forms.DateTimeField('')' + '\n'
                        if propiedad.tipo == 'e': #TimeField
                            strp += '\t' + propiedad.nombre + ' = ' + 'forms.TimeField('')' + '\n'
                        if propiedad.tipo == 'n': #DateField
                            strp += '\t' + propiedad.nombre + ' = ' + 'forms.DateField('')' + '\n'
                        if propiedad.tipo == 'b':
                            strp += '\t' + propiedad.nombre + ' =  forms.BooleanField('')' + '\n'
                        if propiedad.tipo == 'r':
                            strlb = ''
                            for texto in lista_botones:
                                lista_partes = texto.split(',')
                                strlb += '(' + "'" + lista_partes[0] + "'," + "'" + lista_partes[1] + "')" + ',' + '\n'
                            strc += propiedad.nombre + '_choices = (' + strlb + ')' + '\n'
                            strp += propiedad.nombre + ' = ' +  'forms.ChoiceField(choices=' + propiedad.nombre + '_choices' + ', widget=forms.RadioSelect)'
                        if propiedad.tipo == 'a':
                            strlb = ''
                            for texto in lista_botones:
                                lista_partes = texto.split(',')
                                strlb += '(' + "'" + lista_partes[0] + "'," + "'" + lista_partes[1] + "')" + ',' + '\n'
                            strc += propiedad.nombre + '_choices = (' + strlb + ')' + '\n'
                            strp += propiedad.nombre + ' = ' +  'forms.ChoiceField(choices=' + propiedad.nombre + '_choices' + ', widget=forms.Select)'
                        if propiedad.tipo == 'h':
                            strp += '\t' + propiedad.nombre + ' = ' + 'Textarea()' + '\n'
                        if propiedad.tipo == 'p':
                            strp += '\t' + propiedad.nombre + ' = models.ClearableFileInput()' + '\n'

                strt = strt.replace('@fields',strp)
                strt = strt.replace('@widgets',strg)
                strt = strt.replace('@modelo',modelo.nombre)
                strform += strt + '\n'
                strp = ''
                strg = ''


        stri = stri.replace('@listachoices', strc)
        stri = stri.replace('@importmodelos', strim)
        stri = stri.replace('@forms', strform)

        # strt = EscribePersonalizacion(proyecto,aplicacion,'forms.py',strt)

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        if AplicacionTienePropiedades(aplicacion):

            ProcesoPersonalizacion(proyecto,aplicacion.nombre,'forms.py',directorio + nombre + "/" + aplicacion.nombre + "/",stri,nombre,etapa,usuario)

            # # #Sin lineas de personalizacion
            # if not proyecto.conetiquetaspersonalizacion:
            #     stri = QuitaLineasPersonalizacion(stri)
            
            # Grabar el archivo forms.py
            # EscribirArchivo(directorio + nombre + "/" + aplicacion.nombre + "/forms.py",etapa,nombre,stri,True)

def CrearDirectorio(nombreDirectorio, etapa, nombreProyecto, usuario,borraPrevio):

    if borraPrevio:
        try:
            shutil.rmtree(nombreDirectorio)
        except:
            pass
            # print('no se borra el ',nombreDirectorio)

    try:
        os.mkdir(nombreDirectorio)
    except Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "Crear el directorio: " + nombreDirectorio
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()

def CrearSeguridad(proyecto,directorio,dt,usuario):

    # Borrar los errores de generacion
    ErroresCreacion.objects.filter(proyecto=proyecto.nombre).delete()
    # ErroresCreacion.objects.all().delete()

    nombre = proyecto.nombre
    etapa = "CrearSeguridad"

    # Aplicacion registration
    strApp = Aplicacion.objects.get(proyecto=proyecto,nombre='registration')
    # views.py seguridad
    if proyecto.conseguridad:
        # Copia el archivo views.py de text files en registratio
        stri = TextFiles.objects.get(file = "/registration/views.py").texto
        # stri = LeerArchivo(dt + "/registration/views.py",etapa,nombre,usuario)
        ProcesoPersonalizacion(proyecto,strApp.nombre,'views.py',directorio + nombre + "/registration/",stri,nombre,etapa,usuario)
        # CopiarArchivos(dt + "/registration/views.py",directorio + nombre + "/registration" + "/views.py",etapa,nombre,True)        

    # models.py seguridad
    if proyecto.conseguridad:
        stri = TextFiles.objects.get(file = "/registration/models.py").texto
        # stri = LeerArchivo(dt + "/registration/models.py",etapa,nombre,usuario)
        ProcesoPersonalizacion(proyecto,strApp.nombre,'models.py',directorio + nombre + "/registration/",stri,nombre,etapa,usuario)
        # CopiarArchivos(dt + "/registration/models.py",directorio + nombre + "/registration" + "/models.py",etapa,nombre,True)        

    # urls.py seguridad
    if proyecto.conseguridad:
        stri = TextFiles.objects.get(file = "/registration/urls.py").texto
        # stri = LeerArchivo(dt + "/registration/urls.py",etapa,nombre,usuario)
        ProcesoPersonalizacion(proyecto,strApp.nombre,'urls.py',directorio + nombre + "/registration/",stri,nombre,etapa,usuario)
        # CopiarArchivos(dt + "/registration/urls.py",directorio + nombre + "/registration" + "/urls.py",etapa,nombre,True)        

    # forms.py seguridad
    if proyecto.conseguridad:
        stri = TextFiles.objects.get(file = "/registration/forms.py").texto
        # stri = LeerArchivo(dt + "/registration/forms.py",etapa,nombre,usuario)
        ProcesoPersonalizacion(proyecto,strApp.nombre,'forms.py',directorio + nombre + "/registration/",stri,nombre,etapa,usuario)
        # CopiarArchivos(dt + "/registration/forms.py",directorio + nombre + "/registration" + "/forms.py",etapa,nombre,True)        

    # urls.py seguridad
    if proyecto.conseguridad:
        strlfp = 'from registration.urls import registration_patterns' + '\n'
        strlpp = '\tpath(' + "'" + 'accounts/' + "'" + ', include(' + "'" + 'django.contrib.auth.urls' + "'" + ')),' + '\n'
        strlpp += '\tpath(' + "'" + 'accounts/' + "'" + ', include(registration_patterns)),' + '\n'

        stri = LeerArchivo(directorio + nombre + "/" + nombre + "/urls.py",etapa,nombre,usuario)
        stri = stri.replace('#@patternsseguridad', strlfp)
        stri = stri.replace('#@pathseguridad', strlpp)

        EscribirArchivo(directorio + nombre + "/" + nombre + "/urls.py",etapa,nombre,stri,usuario,True)

    # seguridad templates
    if proyecto.conseguridad:

        CreaSeguridadHtml('login.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('password_change_done.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('password_change_form.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('password_reset_complete.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('password_reset_confirm.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('password_reset_done.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('password_reset_form.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('profile_form.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('profile_email_form.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)
        CreaSeguridadHtml('registro.html',etapa,nombre,directorio,dt,strApp,proyecto,usuario)

def CreaSeguridadHtml(nombre_archivo,etapa,nombre,directorio,dt,aplicacion,proyecto,usuario):
    # Copia el archivo de text files registration en la aplicacion registratio
    stri = TextFiles.objects.get(file = "/registration/" + nombre_archivo).texto
    # stri = LeerArchivo(dt + "/registration/" + nombre_archivo,etapa,nombre,usuario)
    ProcesoPersonalizacion(proyecto,aplicacion.nombre,nombre_archivo,directorio + nombre + "/registration/templates/registration/",stri,nombre,etapa,usuario)
    # CopiarArchivos(dt + "/registration/" + nombre_archivo,directorio + nombre + "/registration" + "/templates/registration/" + nombre_archivo,etapa,nombre,True)

def EscribirArchivo(nombreArchivo, etapa,nombreProyecto,texto,usuario,borraPrevio):

    if borraPrevio:
        try:
            os.remove(nombreArchivo)
        except:
            pass

    try:
        with open(nombreArchivo, 'w') as file_object:
            file_object.write(texto)
    except  Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "Escribir archivo: " + nombreArchivo
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()

def CopiarArchivos(origen,destino,etapa,nombreProyecto,usuario,borraPrevio):

    if borraPrevio:
        try:
            os.remove(destino)
        except:
            pass

    try:
        shutil.copy(origen, destino)
    except  Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "Copiar el archivo: " + origen + " en: " + destino
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()

def LeerArchivo(archivo, etapa, nombreProyecto,usuario):
    contents = ''
    try:
        with open(archivo) as file_object:
            contents = file_object.read()
    except  Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "Leer el archivo: " + archivo
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()
    return contents

def LeerArchivoEnTexto(archivo, etapa, nombreProyecto,usuario):
    strTexto = ''
    try:
        with open(archivo) as file_object:
            for line in file_object:
                strTexto += line 
    except Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "Leer el archivo: " + archivo
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()
    return strTexto

def BorrarArchivo(archivo,etapa,nombreProyecto,usuario):

    try:
        os.remove(archivo)
    except Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "Borrar el archivo: " + archivo
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()

def EscribirEnArchivo(archivo,texto,etapa,nombreProyecto,usuario):

    try:
        with open(archivo, 'w') as file_object:
            file_object.write(texto)
    except Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "No se escribio en el archivo: " + archivo
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()

def AplicacionTienePropiedades(aplicacion):
    flgCrear = False
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):
        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            flgCrear = True
            break
    return flgCrear

def QuitaLineasPersonalizacion(texto):
    strLineaNueva = ''
    lineas = texto.split('\n')
    for linea in lineas:
        if not '#@[' in linea:
            strLineaNueva += linea + '\n'

    return strLineaNueva

# reemplaza en los tag del archivo el codigo de la personalizacion
def EscribePersonalizacion(proyecto, nombre_aplicacion, archivo, texto):
    strLineaNueva = ''
    # Leer todas las personalizaciones
    # Ver si cada una de ellas esta en el texto
    # Si esta entonces leer el texto con Returns hasta encontrar el tag de personalizacion
    # Reemplazar en la linea los [] por ()
    # Incorporar la linea en el texto
    # Incorporar el codigo de personalizacion de la base en el texto
    # Incorporar en el texto #@()

    lista_perso = Personaliza.objects.filter(usuario=proyecto.usuario, 
                                        proyecto=proyecto, 
                                        aplicacion=nombre_aplicacion, 
                                        archivo=archivo)
    
    for perso in lista_perso:
        if perso.tag in texto:
            lineas = texto.split('\n')
            for linea in lineas:
                if perso.tag in linea:
                    if '<!-- ' in linea:
                        # archivo html
                        strLineaNueva += '<!-- #@(' + perso.tag + ') -->' + '\n'
                    elif '/*' in linea:
                        # archivo css
                        strLineaNueva += '/* #@(' + perso.tag + ') */' + '\n'
                    else:
                        strLineaNueva += '#@(' + perso.tag + ')' + '\n'                        
                    strcodi=perso.codigo.split('\n')
                    for strCod in strcodi:
                        strLineaNueva += strCod + '\n'
                    if '<!-- ' in linea:
                        # archivo html
                        strLineaNueva += '<!-- #@() -->' + '\n'
                    elif '/*' in linea:
                        # archivo css
                        strLineaNueva += '/* #@() */' + '\n'
                    else:
                        strLineaNueva += '#@()' + '\n'
                else:
                    strLineaNueva += linea +'\n'
            texto = strLineaNueva
            strLineaNueva = ''
    # return strLineaNueva
            # print('strlineanueva ',strLineaNueva)
    return texto

# def EscribePersonalizacion(proyecto, nombre_aplicacion, archivo, texto):
#     strLineaNueva = ''
#     lineas = texto.split('\n')
#     for linea in lineas:
#         if '#@[' in linea:
#             strTag = ''
#             if '<!-- ' in linea:
#                 # archivo html
#                 for ch in linea:
#                     if ch != '#' and ch!= '@' and ch != '[' and ch != ']' and ch != ' ' and ch != '<' and ch != '-' and ch != '>' and ch != '!' and ch != '\t':
#                         strTag += ch            
#             elif '/*' in linea:
#                 # archivo css
#                 for ch in linea:
#                     if ch != '#' and ch!= '@' and ch != '[' and ch != ']' and ch != ' ' and ch != '/' and ch != '-' and ch != '*' and ch != '!' and ch != '\t':
#                         strTag += ch            
#             else:
#                 for ch in linea:
#                     if ch != '#' and ch!= '@' and ch != '[' and ch != ']' and ch != ' ' and ch != '\t':
#                         strTag += ch            


#             tag = Personaliza.objects.filter(usuario = proyecto.usuario,
#                                                  proyecto=proyecto,
#                                                  aplicacion=nombre_aplicacion,
#                                                  archivo=archivo,
#                                                  tag=strTag)
#             if tag.count() > 0:
#                 tag = Personaliza.objects.get(usuario=proyecto.usuario,
#                                                   proyecto=proyecto,
#                                                   aplicacion=nombre_aplicacion,
#                                                   archivo=archivo,
#                                                   tag=strTag)

#                 if '<!-- ' in linea:
#                     strLineaNueva += '<!-- #@(' + strTag + ') -->\n'
#                 elif '/*' in linea:
#                     strLineaNueva += '/*#@(' + strTag + ')*/\n'
#                 else:
#                     strLineaNueva += '#@(' + strTag + ')\n'
                
#                 tagcod = tag.codigo.split('\n')
#                 for lp in tagcod:
#                     strLineaNueva += lp + '\n'

#                 if '<!-- ' in linea:
#                     strLineaNueva += '<!-- #@() -->\n'
#                 elif '/*' in linea:
#                     strLineaNueva += '/*#@()*/\n'
#                 else:
#                     strLineaNueva += '#@()\n'

#             else:
#                 strLineaNueva += linea + '\n'

#         else:
#             strLineaNueva += linea + '\n'

#     return strLineaNueva

def CopiaImagenes(destino,upload,url,origen,nombreProyecto,etapa,usuario,borraPrevio):

    # print('destino ',destino)
    # print('upload ',upload)
    # print('url ',url)
    # print('origen ',origen)
    if borraPrevio:
        try:
            os.remove(destino)
        except:
            pass

    try:
        img = url.split('/')
        imagen = ''
        for i in img:
            imagen = i
        origen = origen + imagen
        if os.path.exists(origen):
            with open(origen, 'rb') as forigen:
                with open(destino, 'wb') as fdestino:
                    shutil.copyfileobj(forigen, fdestino)
    except Exception as e:
        errores = ErroresCreacion()
        errores.etapa = etapa
        errores.paso = "No se escribio en el archivo: " + destino
        errores.proyecto = nombreProyecto
        errores.usuario = usuario
        errores.descripcion = e
        errores.severo = True
        errores.save()

def AsignaFonts(font,par,strFont):
    strt = font.split(',')
    strFont = strFont.replace('@' + par + 'fontfamily', strt[0])
    strFont = strFont.replace('@' + par + 'fontsize', strt[1])
    strFont = strFont.replace('@' + par + 'fontweight', strt[2])
    return strFont

def AsignaJustificacion(hv, justi, par, strJusti):
    if hv == 'h':
        if justi == 'i':
            strj = 'justify-content-start'
        if justi == 'd':
            strj = 'justify-content-end'
        if justi == 'c':
            strj = 'justify-content-center'
        strJusti = strJusti.replace(par, strj)

    if hv == 'v':
        if justi == 's':
            strj = 'align-items-start'
        if justi == 'c':
            strj = 'align-items-center'
        if justi == 'i':
            strj = 'align-items-end'
        strJusti = strJusti.replace(par, strj)

    return strJusti

def AsignaTexto(textoOficial, textoAlterno,textoAreemplazar,strTexto ):
    try:
        strteb = textoOficial.split(',')
        strTexto = strTexto.replace(textoAreemplazar.split(',')[0], strteb[0])
        strTexto = strTexto.replace(textoAreemplazar.split(',')[1], strteb[1])
    except:
        strteb = textoAlterno.split(',')
        strTexto = strTexto.replace(textoAreemplazar.split(',')[0], strteb[0])
        strTexto = strTexto.replace(textoAreemplazar.split(',')[1], strteb[1])
    return strTexto

def Etiquetas(modelo,strt,strcss):
    #etiquetas
    strcss = AsignaFonts(modelo.fontlabelmodelo,'label'+modelo.nombre,strcss)
    strcss = strcss.replace('@colorlabel' + modelo.nombre, modelo.colorlabelmodelo)

    # controles
    if modelo.controlesautomaticos:
        strt = strt.replace('@controles', '\t\t\t\t\t\t\t{{form.as_p}}')
    else:
        strctl = ''
        for propiedad in Propiedad.objects.filter(modelo=modelo): 
            if propiedad.noestaenformulario == False:
                if propiedad.etiqueta == '':
                    propiedad.etiqueta = propiedad.nombre
                    propiedad.save()
                if propiedad.etiquetaarriba:
                    strctl += '\t\t\t\t\t<div class="row" >' + '\n'
                    strctl += '\t\t\t\t\t\t<div class="col font-label-' + modelo.nombre + '">' + propiedad.etiqueta + '</div>' + '\n'
                    strctl += '\t\t\t\t\t</div>' + '\n'
                    if propiedad.tipo == 'p': 
                        strctl += '\t\t\t\t\t<div class="row">' + '\n'
                        strctl += '\t\t\t\t\t\t<div class="col">' + '\n'
                        strctl += '\t\t\t\t\t\t\t{% if ' + modelo.nombre + '.' + propiedad.nombre + ' %}' + '\n'
                        strctl += '\t\t\t\t\t\t\t\t<img src="{{' + modelo.nombre + '.' + propiedad.nombre + '.url}}" width="50px" height="50px" alt="">' + '\n'
                        strctl += '\t\t\t\t\t\t\t{% endif %}' + '\n'
                        strctl += '\t\t\t\t\t\t</div>' + '\n'
                        strctl += '\t\t\t\t\t</div>' + '\n'
                    strctl += '\t\t\t\t\t<div class="row mb-4 mt-1">' + '\n'
                    strctl += '\t\t\t\t\t\t<div class="col">' + '\n'
                    strctl += '\t\t\t\t\t\t\t{{form.' + propiedad.nombre + '}}' + '\n'
                    strctl += '\t\t\t\t\t\t</div>' + '\n'
                    strctl += '\t\t\t\t\t</div>' + '\n'
                else:
                    strctl += '\t\t\t\t\t<div class="row mt-2" >' + '\n'
                    strctl += '\t\t\t\t\t\t<div class="col-2 col-md-' + str(modelo.numerocolumnaslabels) + ' font-label-' + modelo.nombre + '">' + propiedad.etiqueta + '</div>' + '\n'
                    strctl += '\t\t\t\t\t\t<div class="col-10 col-md-' + str(modelo.numerocolumnascontroles) + '">' + '\n'
                    strctl += '\t\t\t\t\t\t\t{{form.' + propiedad.nombre + '}}' + '\n'
                    strctl += '\t\t\t\t\t\t</div>' + '\n'
                    strctl += '\t\t\t\t\t</div>' + '\n'

        strt = strt.replace('@controles', strctl)

    texto = []
    texto.append(strt)
    texto.append(strcss)

    return texto

def NumeroPorcentaje(par,valor,texto):
    if valor <0:
        texto = texto.replace(par,str(valor*-1) + '%')
    else:
        texto = texto.replace(par,str(valor) + 'px')
    return texto

def UpperLower(mayu,par,texto):
    if mayu:
        texto = texto.replace(par, 'text-uppercase')
    else:
        texto = texto.replace(par, '')
    return texto

def AplicacionReal(modelo,texto,proyecto):
    # Encuentra la aplicacion real
    msp = Modelo.objects.get(nombre=modelo.padre, proyecto=proyecto)
    while msp.padre != 'nada':
        msp = Modelo.objects.get(nombre=msp.padre,proyecto=proyecto)
    texto = texto.replace('@aplicacionreal', Aplicacion.objects.get(id=msp.aplicacion.id).nombre)
    return texto

def AplicacionConObjetoRaiz(aplicacion):
    for mod in Modelo.objects.filter(aplicacion=aplicacion):
        if mod.padre == 'nada':
            return True
    return False

def ProcesoPersonalizacion(proyecto,aplicacion,archivo,directorio,stri,nombre,etapa,usuario):
    stri = EscribePersonalizacion(proyecto,aplicacion,archivo,stri)
    #Sin lineas de personalizacion
    if not proyecto.conetiquetaspersonalizacion:
        stri = QuitaLineasPersonalizacion(stri)

    EscribirArchivo(directorio + archivo,etapa,nombre,stri,usuario,True)

def ModeloConPropiedadUsuario(modelo):
    for prop in Propiedad.objects.filter(modelo=modelo):
        if prop.tipo == 'u':
            return prop
    return None

class ConfigurarModeloView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configurar_modelo_nueva.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarModeloView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha

            context['columnasizquierdainserta'] = modelo.numerocolumnasizquierdainserta
            context['columnasderechainserta'] = modelo.numerocolumnasderechainserta
            context['columnasmodeloinserta'] = modelo.numerocolumnasmodeloinserta

            # Alto y ancho de secciones

            try:
                flecha = self.request.GET['flecha']
                if flecha == "mi": #ancho izquierda medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasizquierdainserta > 0:
                            modelo.numerocolumnasizquierdainserta =  modelo.numerocolumnasizquierdainserta - 1
                            context['columnasizquierdainserta'] =  modelo.numerocolumnasizquierdainserta
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdainserta + modelo.numerocolumnasmodeloinserta + modelo.numerocolumnasderechainserta < 12:
                            modelo.numerocolumnasizquierdainserta =  modelo.numerocolumnasizquierdainserta + 1
                            context['columnasizquierdainserta'] =  modelo.numerocolumnasizquierdainserta 
                            modelo.save()
                if flecha == "mc": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasmodeloinserta > 0:
                            modelo.numerocolumnasmodeloinserta =  modelo.numerocolumnasmodeloinserta - 1
                            context['columnasmodeloinserta'] =  modelo.numerocolumnasmodeloinserta
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdainserta + modelo.numerocolumnasmodeloinserta + modelo.numerocolumnasderechainserta < 12:
                            modelo.numerocolumnasmodeloinserta =  modelo.numerocolumnasmodeloinserta + 1
                            context['columnasmodeloinserta'] =  modelo.numerocolumnasmodeloinserta
                            modelo.save()
                if flecha == "md": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasderechainserta > 0:
                            modelo.numerocolumnasderechainserta =  modelo.numerocolumnasderechainserta - 1
                            context['columnasderechainserta'] =  modelo.numerocolumnasderechainserta
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdainserta + modelo.numerocolumnasmodeloinserta + modelo.numerocolumnasderechainserta < 12:
                            modelo.numerocolumnasderechainserta =  modelo.numerocolumnasderechainserta + 1
                            context['columnasderechainserta'] =  modelo.numerocolumnasderechainserta
                            modelo.save()
            except:
                pass
            
            context['proyecto'] = proyecto
            context['modelo'] = modelo
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        
        return context

class ConfigurarModeloNuevaView(TemplateView):
    template_name = "crear/configurar_modelo_nueva.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarModeloNuevaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomediocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['izquierdainserta'] = modelo.numerocolumnasizquierdainserta
            context['modeloinserta'] = modelo.numerocolumnasmodeloinserta
            context['derechainserta'] = modelo.numerocolumnasderechainserta
            context['izquierdaupdatecontiguo'] = modelo.numerocolumnasizquierdaupdate
            context['modeloupdatecontiguo'] = modelo.numerocolumnasmodeloupdate
            context['derechaupdatecontiguo'] = modelo.numerocolumnasderechaupdate
            context['hijosupdatecontiguo'] = modelo.numerocolumnashijosupdate
            context['izquierdaupdate'] = modelo.numerocolumnasizquierdaupdate
            context['modeloupdate'] = modelo.numerocolumnasmodeloupdate
            context['derechaupdate'] = modelo.numerocolumnasderechaupdate
            context['izquierdaborra'] = modelo.numerocolumnasizquierdaborra
            context['modeloborra'] = modelo.numerocolumnasmodeloborra
            context['derechaborra'] = modelo.numerocolumnasderechaborra

            context['proyecto'] = proyecto
            context['modelo'] = modelo
            try:
                seccion = self.request.GET['seccion']
                if seccion == 'izquierdainserta':
                    modelo.numerocolumnasizquierdainserta = int(self.request.GET['valor'])
                    context['izquierdainserta'] = modelo.numerocolumnasizquierdainserta
                    modelo.save()
                if seccion == 'modeloinserta':
                    modelo.numerocolumnasmodeloinserta = int(self.request.GET['valor'])
                    context['modeloinserta'] = modelo.numerocolumnasmodeloinserta
                    modelo.save()
                if seccion == 'derechainserta':
                    modelo.numerocolumnasderechainserta = int(self.request.GET['valor'])
                    context['derechainserta'] = modelo.numerocolumnasderechainserta
                    modelo.save()

                if seccion == 'izquierdaupdatecontiguo':
                    modelo.numerocolumnasizquierdaupdate = int(self.request.GET['valor'])
                    context['izquierdaupdatecontiguo'] = modelo.numerocolumnasizquierdaupdate
                    modelo.save()
                if seccion == 'modeloupdatecontiguo':
                    modelo.numerocolumnasmodeloupdate = int(self.request.GET['valor'])
                    context['modeloupdatecontiguo'] = modelo.numerocolumnasmodeloupdate
                    modelo.save()
                if seccion == 'derechaupdatecontiguo':
                    modelo.numerocolumnasderechaupdate = int(self.request.GET['valor'])
                    context['derechaupdatecontiguo'] = modelo.numerocolumnasderechaupdate
                    modelo.save()
                if seccion == 'hijosupdatecontiguo':
                    modelo.numerocolumnashijosupdate = int(self.request.GET['valor'])
                    context['hijosupdatecontiguo'] = modelo.numerocolumnashijosupdate
                    modelo.save()

                if seccion == 'izquierdaupdate':
                    modelo.numerocolumnasizquierdaupdate = int(self.request.GET['valor'])
                    context['izquierdaupdate'] = modelo.numerocolumnasizquierdaupdate
                    proyecto.save()
                if seccion == 'modeloupdate':
                    modelo.numerocolumnasmodeloupdate = int(self.request.GET['valor'])
                    context['modeloupdate'] = modelo.numerocolumnasmodeloupdate
                    modelo.save()
                if seccion == 'derechaupdate':
                    modelo.numerocolumnasderechaupdate = int(self.request.GET['valor'])
                    context['derechaupdate'] = modelo.numerocolumnasderechaupdate
                    modelo.save()

                if seccion == 'izquierdaborra':
                    modelo.numerocolumnasizquierdaborra = int(self.request.GET['valor'])
                    context['izquierdaborra'] = modelo.numerocolumnasizquierdaborra
                    modelo.save()
                if seccion == 'modeloborra':
                    modelo.numerocolumnasmodeloborra = int(self.request.GET['valor'])
                    context['modeloborra'] = modelo.numerocolumnasmodeloborra
                    modelo.save()
                if seccion == 'derechaborra':
                    modelo.numerocolumnasderechaborra = int(self.request.GET['valor'])
                    context['derechaborra'] = modelo.numerocolumnasderechaborra
                    modelo.save()
            except:
                pass
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class ConfigurarUpdateContiguoView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configurar_update_contiguo.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarUpdateContiguoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha

            context['columnasizquierdaupdate'] = modelo.numerocolumnasizquierdaupdate
            context['columnasderechaupdate'] = modelo.numerocolumnasderechaupdate
            context['columnasmodeloupdate'] = modelo.numerocolumnasmodeloupdate
            context['columnashijosupdate'] = modelo.numerocolumnashijosupdate

            # Alto y ancho de secciones

            try:
                flecha = self.request.GET['flecha']
                if flecha == "mi": #ancho izquierda medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasizquierdaupdate > 0:
                            modelo.numerocolumnasizquierdaupdate =  modelo.numerocolumnasizquierdaupdate - 1
                            context['columnasizquierdaupdate'] =  modelo.numerocolumnasizquierdaupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  + modelo.numerocolumnashijosupdate < 12:
                            modelo.numerocolumnasizquierdaupdate =  modelo.numerocolumnasizquierdaupdate + 1
                            context['columnasizquierdaupdate'] =  modelo.numerocolumnasizquierdaupdate 
                            modelo.save()
                if flecha == "mc": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasmodeloupdate > 0:
                            modelo.numerocolumnasmodeloupdate =  modelo.numerocolumnasmodeloupdate - 1
                            context['columnasmodeloupdate'] =  modelo.numerocolumnasmodeloupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  + modelo.numerocolumnashijosupdate < 12:
                            modelo.numerocolumnasmodeloupdate =  modelo.numerocolumnasmodeloupdate + 1
                            context['columnasmodeloupdate'] =  modelo.numerocolumnasmodeloupdate
                            modelo.save()
                if flecha == "md": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasderechaupdate > 0:
                            modelo.numerocolumnasderechaupdate =  modelo.numerocolumnasderechaupdate - 1
                            context['columnasderechaupdate'] =  modelo.numerocolumnasderechaupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  + modelo.numerocolumnashijosupdate < 12:
                            modelo.numerocolumnasderechaupdate =  modelo.numerocolumnasderechaupdate + 1
                            context['columnasderechaupdate'] =  modelo.numerocolumnasderechaupdate
                            modelo.save()
                if flecha == "mh": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnashijosupdate > 0:
                            modelo.numerocolumnashijosupdate =  modelo.numerocolumnashijosupdate - 1
                            context['columnashijosupdate'] =  modelo.numerocolumnashijosupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  + modelo.numerocolumnashijosupdate < 12:
                            modelo.numerocolumnashijosupdate =  modelo.numerocolumnashijosupdate + 1
                            context['columnashijosupdate'] =  modelo.numerocolumnashijosupdate
                            modelo.save()
            except:
                pass
            
            context['proyecto'] = proyecto
            context['modelo'] = modelo
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        

        return context        

class ConfigurarUpdateAbajoView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configurar_update_abajo.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarUpdateAbajoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha

            context['columnasizquierdaupdate'] = modelo.numerocolumnasizquierdaupdate
            context['columnasderechaupdate'] = modelo.numerocolumnasderechaupdate
            context['columnasmodeloupdate'] = modelo.numerocolumnasmodeloupdate

            # Alto y ancho de secciones

            try:
                flecha = self.request.GET['flecha']
                if flecha == "mi": #ancho izquierda medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasizquierdaupdate > 0:
                            modelo.numerocolumnasizquierdaupdate =  modelo.numerocolumnasizquierdaupdate - 1
                            context['columnasizquierdaupdate'] =  modelo.numerocolumnasizquierdaupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  < 12:
                            modelo.numerocolumnasizquierdaupdate =  modelo.numerocolumnasizquierdaupdate + 1
                            context['columnasizquierdaupdate'] =  modelo.numerocolumnasizquierdaupdate 
                            modelo.save()
                if flecha == "mc": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasmodeloupdate > 0:
                            modelo.numerocolumnasmodeloupdate =  modelo.numerocolumnasmodeloupdate - 1
                            context['columnasmodeloupdate'] =  modelo.numerocolumnasmodeloupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  < 12:
                            modelo.numerocolumnasmodeloupdate =  modelo.numerocolumnasmodeloupdate + 1
                            context['columnasmodeloupdate'] =  modelo.numerocolumnasmodeloupdate
                            modelo.save()
                if flecha == "md": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasderechaupdate > 0:
                            modelo.numerocolumnasderechaupdate =  modelo.numerocolumnasderechaupdate - 1
                            context['columnasderechaupdate'] =  modelo.numerocolumnasderechaupdate
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaupdate + modelo.numerocolumnasmodeloupdate + modelo.numerocolumnasderechaupdate  < 12:
                            modelo.numerocolumnasderechaupdate =  modelo.numerocolumnasderechaupdate + 1
                            context['columnasderechaupdate'] =  modelo.numerocolumnasderechaupdate
                            modelo.save()
            except:
                pass
            
            context['proyecto'] = proyecto
            context['modelo'] = modelo
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        
        return context                

class ConfigurarBorraView(TemplateView):
    # template_name = "crear/configurar_base.html"
    template_name = "crear/configurar_update_borra.html"

    def get_context_data(self,**kwargs):
        context = super(ConfigurarBorraView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)

        # Ver si esta en configuracion
        try:
            context['configuracion'] = self.request.GET['configuracion_proyecto']
        except:
            context['configuracion'] = 'false'

        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
            context['altoencabezado'] = str(proyecto.altofilaenizcede) + 'px'
            context['altobume'] = str(proyecto.altofilabume) + 'px'
            context['altomedio'] = str(200) + 'px'
            context['altopie'] = str(proyecto.altofilapie) + 'px'
            context['anchoencabezadoizquierda'] = proyecto.numerocolumnaenizquierda 
            context['anchologo'] = proyecto.numerocolumnalogo
            context['anchotitulo'] = proyecto.numerocolumnatitulo
            context['anchologin'] = proyecto.numerocolumnalogin
            context['anchoencabezadoderecha'] = proyecto.numerocolumnaenderecha
            context['anchobumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['anchobusqueda'] = proyecto.numerocolumnabusqueda
            context['anchomenu'] = proyecto.numerocolumnamenu
            context['anchobumederecha'] = proyecto.numerocolumnabumederecha
            context['anchomedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['anchomedicocentro'] = proyecto.numerocolumnamediocentro
            context['anchomedioderecha'] = proyecto.numerocolumnamedioderecha
            context['numerocolumnaenizquierda'] = proyecto.numerocolumnaenizquierda
            context['numerocolumnalogo'] = proyecto.numerocolumnalogo
            context['numerocolumnatitulo'] = proyecto.numerocolumnatitulo
            context['numerocolumnalogin'] = proyecto.numerocolumnalogin
            context['numerocolumnaenderecha'] = proyecto.numerocolumnaenderecha
            context['numerocolumnabumeizquierda'] = proyecto.numerocolumnabumeizquierda
            context['numerocolumnabusqueda'] = proyecto.numerocolumnabusqueda
            context['numerocolumnamenu'] = proyecto.numerocolumnamenu
            context['numerocolumnabumederecha'] = proyecto.numerocolumnabumederecha
            context['numerocolumnamedioizquierda'] = proyecto.numerocolumnamedioizquierda
            context['numerocolumnamediocentro'] = proyecto.numerocolumnamediocentro
            context['numerocolumnamedioderecha'] = proyecto.numerocolumnamedioderecha

            context['columnasizquierdaborra'] = modelo.numerocolumnasizquierdaborra
            context['columnasderechaborra'] = modelo.numerocolumnasderechaborra
            context['columnasmodeloborra'] = modelo.numerocolumnasmodeloborra

            # Alto y ancho de secciones

            try:
                flecha = self.request.GET['flecha']
                if flecha == "mi": #ancho izquierda medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasizquierdaborra > 0:
                            modelo.numerocolumnasizquierdaborra =  modelo.numerocolumnasizquierdaborra - 1
                            context['columnasizquierdaborra'] =  modelo.numerocolumnasizquierdaborra
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaborra + modelo.numerocolumnasmodeloborra + modelo.numerocolumnasderechaborra  < 12:
                            modelo.numerocolumnasizquierdaborra =  modelo.numerocolumnasizquierdaborra + 1
                            context['columnasizquierdaborrra'] =  modelo.numerocolumnasizquierdaborra 
                            modelo.save()
                if flecha == "mc": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasmodeloborra > 0:
                            modelo.numerocolumnasmodeloborra =  modelo.numerocolumnasmodeloborra - 1
                            context['columnasmodeloborra'] =  modelo.numerocolumnasmodeloborra
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaborra + modelo.numerocolumnasmodeloborra + modelo.numerocolumnasderechaborra  < 12:
                            modelo.numerocolumnasmodeloborra =  modelo.numerocolumnasmodeloborra + 1
                            context['columnasmodeloborra'] =  modelo.numerocolumnasmodeloborra
                            modelo.save()
                if flecha == "md": #ancho medio
                    direccion = self.request.GET['direccion']
                    if direccion == 'menos':
                        if modelo.numerocolumnasderechaborra > 0:
                            modelo.numerocolumnasderechaborra =  modelo.numerocolumnasderechaborra - 1
                            context['columnasderechaborra'] =  modelo.numerocolumnasderechaborra
                            modelo.save()
                            # context['numerocolumnalogo'] = proyecto.numerocolumnalogo + 1
                    else:
                        if modelo.numerocolumnasizquierdaborra + modelo.numerocolumnasmodeloborra + modelo.numerocolumnasderechaborra  < 12:
                            modelo.numerocolumnasderechaborra =  modelo.numerocolumnasderechaborra + 1
                            context['columnasderechaborra'] =  modelo.numerocolumnasderechaborra
                            modelo.save()
            except:
                pass
            
            context['proyecto'] = proyecto
            context['modelo'] = modelo
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        
        return context                        

class CrearPasosView(TemplateView):
    template_name = "crear/crear_pasos.html"

    def get_context_data(self,**kwargs):
        context = super(CrearPasosView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            proyecto = Proyecto.objects.get(id = self.request.GET['proyecto_id'],usuario=self.request.user)
            context['error'] = ''
            paso = self.request.GET['paso']
            context['paso'] = paso
            lista = []
            if paso == '1':
                lista.append(['Crea el directorio',proyecto.nombre,2,9,1])
                lista.append(['Crea el directorio',proyecto.nombre + '/media',2,9,2])
                lista.append(['Crea el directorio',proyecto.nombre + '/' + proyecto.nombre,2,9,3])
                lista.append(['Crea el archivo',proyecto.nombre + '/' + proyecto.nombre + '/_init_.py',2,9,4])
                lista.append(['Crea el archivo',proyecto.nombre + '/' + proyecto.nombre + '/settings.py (p)',2,9,5])
                lista.append(['Crea el archivo',proyecto.nombre + '/' + proyecto.nombre + '/urls.py',2,9,6])
                lista.append(['Crea el archivo',proyecto.nombre + '/' + proyecto.nombre + '/wsgi.py',2,9,7])
                lista.append(['Crea el archivo',proyecto.nombre + '/' + proyecto.nombre + '/manage.py',2,9,8])
            if paso == '2':
                num = 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el directorio',proyecto.nombre + '/' + ap.nombre,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el directorio',proyecto.nombre + '/' + ap.nombre + '/migrations' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el directorio',proyecto.nombre + '/' + ap.nombre + '/migrations/_init_.py' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el directorio',proyecto.nombre + '/' + ap.nombre + '/migrations/_pycache_' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el directorio',proyecto.nombre + '/' + ap.nombre + '/templates' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el directorio',proyecto.nombre + '/' + ap.nombre + '/templates/' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + ap.nombre + '/_init_.py' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + ap.nombre + '/admin.py' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + ap.nombre + '/apps.py' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + ap.nombre + '/models.py' ,2,9,num])
                    num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + ap.nombre + '/tests.py' ,2,9,num])
                    num += 1
                lista.append(['Crea el directorio',proyecto.nombre + '/core/templates/core/includes',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/templates/core/includes/css_general.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/templates/core/includes/js_general.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el directorio',proyecto.nombre + '/core/static',2,9,num])
                num += 1
                lista.append(['Crea el directorio',proyecto.nombre + '/core/static/core',2,9,num])
                num += 1
                lista.append(['Crea el directorio',proyecto.nombre + '/core/static/core/css',2,9,num])
                num += 1
                lista.append(['Crea el directorio',proyecto.nombre + '/core/static/core/js',2,9,num])
                num += 1
                lista.append(['Crea el directorio',proyecto.nombre + '/core/static/core/img',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/animation.css',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/bootstrap.css',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/bootstrap.min.css',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/js/Bootstrap.min.js',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/js/jquery_3.4.1.min.js',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/js/popper.min.js',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/js/js_propios.js',2,9,num])
                num += 1
                lista.append(['Actualizar el archivo',proyecto.nombre + '/' + proyecto.nombre + '/settings.py',2,9,num])
                num += 1
            if paso == '3':
                num = 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Actualiza el archivo',proyecto.nombre + '/' + ap.nombre + '/models.py (p)' ,2,9,num])
                    num += 1
            if paso == '4':
                num = 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crear las vistas',proyecto.nombre + '/' + ap.nombre + '/views.py (p)' ,2,9,num])
                    num += 1
            if paso == '5':
                num = 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crear las urls',proyecto.nombre + '/' + ap.nombre + '/urls.py (p)' ,2,9,num])
                    num += 1
            if paso == '6':
                num = 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    lista.append(['Crear los formularios',proyecto.nombre + '/' + ap.nombre + '/forms.py (p)' ,2,9,num])
                    num += 1
            if paso == '7':
                num = 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/templates/core/base.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/templates/core/home.html (p)',2,9,num])
                num += 1
                for ap in Aplicacion.objects.filter(proyecto=proyecto):
                    if ap.nombre != 'registration':
                        lista.append(['Crea el archivo',proyecto.nombre + '/core/templates/core/includes/menu_' + ap.nombre + '.html (p)',2,9,num])
                        num += 1
                for md in Modelo.objects.filter(proyecto=proyecto):
                    if md.padre == 'nada':
                        lista.append(['Crea el archivo',proyecto.nombre + '/' + md.aplicacion.nombre + '/templates/' + md.aplicacion.nombre + '/' + md.nombre + '_list.html (p)',2,9,num])
                        num += 1
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + md.aplicacion.nombre + '/templates/' + md.aplicacion.nombre + '/' + md.nombre + '_form.html (p)',2,9,num])
                    num += 1
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + md.aplicacion.nombre + '/templates/' + md.aplicacion.nombre + '/' + md.nombre + '_update_form.html (p)',2,9,num])
                    num += 1
                    lista.append(['Crea el archivo',proyecto.nombre + '/' + md.aplicacion.nombre + '/templates/' + md.aplicacion.nombre + '/' + md.nombre + '_confirm_delete.html (p)',2,9,num])
                    num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/estilos.css (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/modelo_borra.css (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/modelo_hijo.css (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/modelo_inserta.css (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/modelo_list.css (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/core/static/core/css/modelo_update.css (p)',2,9,num])
                num += 1
            if paso == '8':
                num = 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/views.py (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/models.py (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/urls.py (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/forms.py (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/views.py (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/login.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/password_change_done.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/password_change_forms.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/password_reset_complete.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/password_reset_confirm.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/password_reset_done.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/password_reset_form.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/profile_form.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/profile_email_form.html (p)',2,9,num])
                num += 1
                lista.append(['Crea el archivo',proyecto.nombre + '/registration/templates/registration/registro.html (p)',2,9,num])
                num += 1

            context['lista'] = lista
            context['proyecto'] = proyecto
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class EditarReporteView(UpdateView):
    model = ReporteNuevo
    form_class = ReporteForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id'] + '&ok'
        # return reverse_lazy('proyectos:arbol') + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarReporteView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])   
            context['size'] = 'A4'            
            if self.request.GET['size'] == 'L':         
                context['size'] = 'Letter'            
            context['orientacion'] = 'Landscape'            
            if self.request.GET['orientacion'] == 'P':         
                context['orientacion'] = 'Portrait'            
            context['proyecto'] = proyecto
            context['proyecto_id'] = proyecto.id
            context['reporte'] = ReporteNuevo.objects.get(reportesize=self.request.GET['size'],orientacion=self.request.GET['orientacion'])
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

