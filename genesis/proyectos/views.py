from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# from django.shortcuts import render_to_response
from .models import Proyecto,Crear,LicenciaUso, ProyectoTexto
from aplicaciones.models import Aplicacion
from crear.models import ErroresCreacion, ReporteNuevo
from .forms import ProyectoForm, ProyectoTextoForm
from core.models import Genesis, Precio
from crear import views
from django.utils import timezone
import datetime
from registration.views import VerificaVigenciaUsuario

# Create your views here.
class ListaProyectosView(ListView):
    model = Proyecto

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data()
    #     try:
    #         lista = ListaProyectos(self.request.GET['textob'], request.user)
    #     except:
    #         lista = ListaProyectos(None, request.user)

    #     context['lista_proyectos'] = lista
    #     return render_to_response('proyectos/proyecto_list.html', context) 

    def get_context_data(self, **kwargs):
        context = super(ListaProyectosView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['lista_proyectos'] = ListaProyectos(self.request.GET['criterio'],self.request.user)
        print('lista de proyextos')
        context['criterio'] = self.request.GET['criterio']
        if self.request.GET['duplica'] == '1':
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
            # print('uno')
            # DUPLICO EL PROYECTO
            pd = copy.deepcopy(proyecto)
            # print('desc ' ,c.descripcion)
            # print('dos')
            pd.id = None
            pd.save()
            # DUPLICA APLICACIONES
            for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
                apn = copy.deepcopy(aplicacion)
                apn.proyecto = pd
                apn.id = None
                apn.save()
                for modelo in Modelo.objects.filter(proyecto=proyecto,aplicacion=aplicacion):
                    mon = copy.deepcopy(modelo)
                    mon.proyecto = pd
                    mon.aplicacion = apn
                    mon.id = None
                    mon.save()
                    for propiedad in Propiedad.objects.filter(modelo=modelo):
                        prn = copy.deepcopy(propiedad)
                        prn.modelo = mon
                        prn.id = None
                        prn.save()
                        for regla in Regla.objects.filter(propiedad=propiedad):
                            rgn = copy.deepcopy(regla)
                            rgn.propiedad = prn
                            rgn.id = None
                            rgn.save()



        # lista =[]
        # tel = Proyecto.objects.filter(usuario=self.request.user)
        # for te in tel:
        #     lista.append([te.topico.upper(),te.descripcion,str(te.correlativo) + '.',te.diagrama,'e',te.id])
        #     tdl = TutorialDetalle.objects.filter(tutorialencabezado = te)
        #     for td in tdl:
        #         lista.append([string.capwords(td.topico.lower()),td.descripcion,str(te.correlativo) + '.' + str(td.correlativo) + '.',td.diagrama,'d',td.id])
        # context['lista'] = lista
        # tutorial = self.request.GET['video']
        # if tutorial != '':
        #     context['video'] = 'video.mp4'
        # return context              
        # context['lista_proyectos'] = lista_proyectos
        return context

    # def get_success_url(self):
    #     return reverse_lazy('proyectos:lista') + '?criterio=' + self.request.POST['textob']

    # def post(self,request,*args,**kwargs):
    #     return HttpResponseRedirect(self.get_success_url())

# Devuelve la lista de proyectos despues de analizar criterio
import copy

class ArbolProyectoView(ListView):
    model = Proyecto
    template_name = 'proyectos/arbol_proyecto.html'

    def get_context_data(self, **kwargs):
        context = super(ArbolProyectoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(usuario = self.request.user, id = self.request.GET['proyecto_id'])
            # Maneja arriba abajo
            try:
                if self.request.GET['modeloarriba'] == '1':
                    # recuperar el modelo a mover
                    modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
                    # leer los modelos en orden inverso
                    lista = Modelo.objects.filter(proyecto=proyecto,padre='nada').order_by('ordengeneracion')
                    # construir una lista con los campos ordengeneracion
                    i = 0
                    for it in lista:
                        if it.id == modelo.id:
                            ma = Modelo.objects.get(id=it.id)
                            mp = Modelo.objects.get(id=lista[i-1].id)
                            tp = mp.ordengeneracion
                            ta = ma.ordengeneracion
                            ma.ordengeneracion = tp
                            ma.save()
                            mp.ordengeneracion = ta
                            mp.save()
                        i+=1                            
            except:
                pass

            try:
                if self.request.GET['modeloabajo'] == '1':
                    # recuperar el modelo a mover
                    modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
                    # leer los modelos en orden inverso
                    lista = Modelo.objects.filter(proyecto=proyecto,padre='nada').order_by('ordengeneracion')
                    # construir una lista con los campos ordengeneracion
                    i = 0
                    for it in lista:
                        if it.id == modelo.id:
                            ma = Modelo.objects.get(id=it.id)
                            mp = Modelo.objects.get(id=lista[i+1].id)
                            tp = mp.ordengeneracion
                            ta = ma.ordengeneracion
                            ma.ordengeneracion = tp
                            ma.save()
                            mp.ordengeneracion = ta
                            mp.save()
                        i+=1                            
            except:
                pass

            context['proyecto'] = proyecto
            context['proyecto_id'] = proyecto.id
            context['lista_aplicaciones'] = Aplicacion.objects.filter(proyecto = proyecto).order_by('ordengeneracion')
            context['lista_reportes'] = ReporteNuevo.objects.all()
            try:
                if self.request.GET['haciatexto'] == '1':
                    # Procesa hacia texto
                    # Borrar el anterior
                    ProyectoTexto.objects.filter(proyecto=proyecto.id).delete()
                    # Comienza con el proyecto
                    size  = 24
                    sizetexto = 12
                    ident = 20
                    texto = '<p><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Proyecto: [npr ' + proyecto.nombre + ']</strong></span></span></p>'
                    texto += '<p><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">El proyecto que se construye con Genesis tiene la siguiente descripcion: [dpr ' + proyecto.descripcion + ']</span></span></p>'

                    # Texto variable
                    textov = 'Este proyecto @seguridad definida la opcion de seguridad, @personaliza las etiquetas de personalizacion, @busqueda una opcion de busqueda general y los menus de aplicaciones y modelos @contiguos contiguos al menu de seguridad.' 

                    if proyecto.conseguridad:
                        textov = textov.replace('@seguridad','tiene')
                    else:
                        textov = textov.replace('@seguridad','no tiene')

                    if proyecto.conetiquetaspersonalizacion:
                        textov = textov.replace('@personaliza','incluye')
                    else:
                        textov = textov.replace('@personaliza','no incluye')

                    if proyecto.conbusqueda:
                        textov = textov.replace('@busqueda','tiene')
                    else:
                        textov = textov.replace('@busqueda','no tiene')

                    if proyecto.menuscotiguos:
                        textov = textov.replace('@contiguos','son')
                    else:
                        textov = textov.replace('@contiguos','no son')

                    texto += '<p><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">' + textov + '</span></span></p>'

                    # Caracteristicas graficas
                    texto += '<ul>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Color de la pagina principal ' + '[cpp ' + proyecto.colorpaginaprincipal + ']</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">El proyecto tienen una separacion entre seciones de ' + '[ses ' + proyecto.separacionsecciones + ']</span></span></li>'

                    # Texto del centro
                    if proyecto.textomedio != '':
                        textov = 'El texto de la seccion central es: [txm ' + proyecto.textomedio + '] y tiene un color [ctxm ' + proyecto.colortextomedio + '] con un formato de letra [ftxm ' + proyecto.fonttextomedio + ']'
                        texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">' + textov + '</span></span></li>'

                    # Texto del titulo
                    if proyecto.titulo != '':
                        textov = 'El proyecto esta identificado en la pagina por el titulo [tit ' + proyecto.titulo + '] cuyo color es: [cti ' + proyecto.colortitulo +']. El font del titulo es: [fti ' + proyecto.fonttitulo + '] y se encuentra alineado horizontalmente @horizontal [jht ' + proyecto.justificacionhorizontaltitulo +'] y verticalmente en la parte @vertical [jvt ' + proyecto.justificacionverticaltitulo +']'
                        
                        if proyecto.justificacionhorizontaltitulo == 'i':
                            textov = textov.replace('@horizontal', 'a la izquierda')
                        elif proyecto.justificacionhorizontaltitulo == 'd':
                            textov = textov.replace('@horizontal', 'a la derecha')
                        else:
                            textov = textov.replace('@horizontal', 'al centro')

                        if proyecto.justificacionverticaltitulo == 's':
                            textov = textov.replace('@vertical', 'superior')
                        elif proyecto.justificacionhorizontaltitulo == 'i':
                            textov = textov.replace('@vertical', 'inferior')
                        else:
                            textov = textov.replace('@vertical', 'central')

                        texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">' + textov + '</span></span></li>'

                    # Imagen de titulo
                    textov ='Si el proyecto tuviera una imagen que estuviera en lugar del titulo, esta tendria [itw ' + proyecto.imagentitulowidth + '] pixels en su dimension horizontal y [ith ' + proyecto.imagentituloheight + '] pixels en su dimension vertical y estaria alineado horizontalmente @horizontal [jht ' + proyecto.justificacionhorizontaltitulo + '] y verticalmente en la parte @vertical [jvt ' + proyecto.justificacionverticaltitulo +'].'

                    if proyecto.justificacionhorizontaltitulo == 'i':
                        textov = textov.replace('@horizontal', 'a la izquierda')
                    elif proyecto.justificacionhorizontaltitulo == 'd':
                        textov = textov.replace('@horizontal', 'a la derecha')
                    else:
                        textov = textov.replace('@horizontal', 'al centro')

                    if proyecto.justificacionverticaltitulo == 's':
                        textov = textov.replace('@vertical', 'superior')
                    elif proyecto.justificacionhorizontaltitulo == 'i':
                        textov = textov.replace('@vertical', 'inferior')
                    else:
                        textov = textov.replace('@vertical', 'central')
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">' + textov + '</span></span></li>'

                    # Logo del proyecto
                    textov = 'Si se define un logo para el proyecto tendria [avw ' + proyecto.avatarwidth +'] pixels en su dimension vertical y [avh ' + proyecto.avatarheight +'] pixels en su dimension horizontal y se colocaria @horizontal [] horizontalmente y en la parte @vertical [] verticalmente.'
                    if proyecto.justificacionhorizontallogo == 'i':
                        textov = textov.replace('@horizontal', 'a la izquierda')
                    elif proyecto.justificacionhorizontallogo == 'd':
                        textov = textov.replace('@horizontal', 'a la derecha')
                    else:
                        textov = textov.replace('@horizontal', 'al centro')
                    if proyecto.justificacionverticallogo == 's':
                        textov = textov.replace('@horizontal', 'superior')
                    elif proyecto.justificacionverticallogo == 'i':
                        textov = textov.replace('@horizontal', 'inferior')
                    else:
                        textov = textov.replace('@horizontal', 'central')
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">' + textov + '</span></span></li>'

                    # menu
                    textov = 'El menu del proyecto tiene un font [fme ' + proyecto.fontmenu + '] con un color [cme ' + proyecto.colormenu + '] y esta ubicado horizontalmente @horizontal [jum ' + proyecto.justificacionmenu +']'
                    if proyecto.justificacionmenu == 'i':
                        textov = textov.replace('@horizontal', 'a la izquierda')
                    elif proyecto.justificacionmenu == 'd':
                        textov = textov.replace('@horizontal', 'a la derecha')
                    else:
                        textov = textov.replace('@horizontal', 'al centro')
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">' + textov + '</span></span></li>'

                    texto += '</ul>'

                    texto += '<p><span style="font-size:' + str(size-4) + 'px"><span style="color:#000000"><strong>La fila superior de la pagina del proyecto tiene la siguiente estructura:</strong></span></span></p>'

                    # Estructura fila superior
                    texto += '<ul>'

                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Su altura es de [afs ' + proyecto.altofilaenizcede + '] pixels y su color de fondo es [cfs ' + proyecto.colorfilaenizcede + ']</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La seccion de la izquierda de la fila superior tiene [nci ' + proyecto.numerocolumnaenizquierda +'] columnas, es de color [cci ' + proyecto.colorcolumnaenizquierda + '] y su altura es de [aci ' + proyecto.altocolumnaenizquierda + '] pixels.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La seccion del logo de la fila superior tiene [ncl ' + proyecto.numerocolumnalogo + '] columnas, es de color [ccl ' + proyecto.colorcolumnalogo + '] y su altura es de [acl ' + proyecto.altocolumnalogo + '] pixels.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La seccion del titulo de la fila superior tiene [nct ' + proyecto.numerocolumnatitulo + '] columnas, es de color [cct ' + proyecto.colorcolumnatitulo + '] y su altura es de [act ' + proyecto.altocolumnatitulo + '] pixels.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La seccion auxiliar de la fila superior tiene [ncg ' + proyecto.numerocolumnalogin + '] columnas, es de color [ccg ' + proyecto.colorcolumnalogin + '] y su altura es de [acg ' + proyecto.altocolumnalogin + '] pixels.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La seccion de la derecha de la fila superior tiene [ncd ' + proyecto.numerocolumnaenderecha + '] columnas, es de color [ccd ' + proyecto.colorcolumnaenderecha + '] y su altura es de [acd ' + proyecto.altocolumnaenderecha + '] pixels.</span></span></li>'

                    if proyecto.enborde:
                        texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Las secciones de la fila superior tienen un borde [bss] que es de color [cbss ' + proyecto.encolorborde + '] y tienen un ancho de linea de [abss ' + proyecto.enanchoborde + '] puntos.</span></span></li>'
                    else:
                        texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Las secciones de la fila superior no tienen un borde.</span></span></li>'

                    texto += '</ul>'

                    # Fila de busqueda y menu
                    texto += '<p><span style="font-size:' + str(size-4) + 'px"><span style="color:#000000"><strong>La fila de busqueda y menu de la pagina del proyecto esta estructurada de la siguiente manera:</strong></span></span></p>'
                    texto += '<ul>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La altura de toda la fila es de [afb ' + proyecto.altofilabume + '] pixels y tiene un color de fondo [cfb ' + proyecto.colorfilabume + '].</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La altura de la seccion de la izquierda de la fila busqueda y menu es de [acbi ' + proyecto.altocolumnabumeizquierda + '] pixels, es de color [ccbi ' + proyecto.colorcolumnabumeizquierda + '] y tiene una dimension de [ncbi ' + proyecto.numerocolumnabumeizquierda + '] columnas.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La altura de la seccion de busqueda de la fila busqueda y menu es de [acb ' + proyecto.altocolumnabusqueda + '] pixels, es de color [ccb ' + proyecto.colorcolumnabusqueda + '] y tiene una dimension de [ncb ' + proyecto.numerocolumnabusqueda + '] columnas.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La altura de la seccion del menu de la fila busqueda y menu es de [acm ' + proyecto.altocolumnamenu + '] pixels, es de color [ccm ' + proyecto.colorcolumnamenu + '] y tiene una dimension de [ncm ' + proyecto.numerocolumnamenu + '] columnas.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">La altura de la seccion de la derecha de la fila busqueda y menu es de [acbd ' + proyecto.altocolumnabumederecha + '] pixels, es de color [ccbd ' + proyecto.colorcolumnabumederecha + '] y tiene una dimension de [ncbd ' + proyecto.numerocolumnabumederecha + '] columnas.</span></span></li>'
                    texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Las opciones del menu tienen un color de letra [cme ' + proyecto.colormenu + '] con un font [fme ' + proyecto.fontmenu + '] </span></span></li>'

                    if proyecto.bumeborde:
                        texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Las secciones de la fila de busqueda y menu tienen un borde [bme] que es de color [cbme ' + proyecto.bumecolorborde + '] y tienen un ancho de linea de [abme ' + proyecto.bumeanchoborde + '] puntos.</span></span></li>'
                    else:
                        texto += '<li style="margin-left: 20px;"><span style="font-size:' + str(sizetexto) + 'px"><span style="color:#000000">Las secciones de la fila de busqueda y menu no tienen un borde.</span></span></li>'

                    texto += '</ul>'










                    texto += '<p><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion: </strong>' + '<em>[dpro ' + proyecto.descripcion + ']</em></span></span></p>'
                    if Aplicacion.objects.filter(proyecto=proyecto).count() > 0:
                        texto += '<p style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Aplicaciones del Proyecto:</strong> '+ proyecto.nombre + '</span></span></p>'
                        # Recorre la aplicaciones
                        for app in Aplicacion.objects.filter(proyecto=proyecto):
                            if app.nombre != 'registration' and app.nombre != 'core':
                                texto += '<p style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Nombre:</strong>[nap ' + app.nombre + ']</span></span></span></p>'
                                texto += '<p style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion: </strong>' + '<em>[dap ' + app.descripcion + ']</em></span></span></span></p>'
                                lista_modelos = Modelo.objects.filter(aplicacion = app, padre='nada').order_by('ordengeneracion') 
                                if lista_modelos.count() > 0:
                                    texto += '<p style="margin-left:30px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Modelos de la Aplicacion : </strong>' + app.nombre + '</span></span></p>'
                                    ident += 10
                                    print('1')
                                    for modelo_lista in lista_modelos:
                                        print('2')
                                        texto += '<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#9b59b6"><strong>[nmo ' + modelo_lista.nombre + ']</strong></span></span></span></p>'
                                        texto += '<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion: </strong>' + '<em>[dmo ' + modelo_lista.descripcion + ']</em></span></span></span></p>'                                      
                                        lista_texto = []
                                        print('3')
                                        ReglasPropiedades(modelo_lista,lista_texto,40,size)
                                        print('4')
                                        HaciaTextoRecursiva(proyecto,modelo_lista,lista_texto,size,30)
                                        for strTexto in lista_texto:
                                            texto += strTexto

                    proyecto_texto = ProyectoTexto()
                    proyecto_texto.usuario = self.request.user
                    proyecto_texto.titulo = proyecto.nombre
                    proyecto_texto.texto = texto
                    proyecto_texto.proyecto = proyecto.id
                    # print(texto)
                    proyecto_texto.save()

            except Exception as e:     
                print(e)
                context['lista_crear'] = ListaCrear(proyecto.id)
            # context['lista_crear'] = None
            context['tiene_errores'] = ErroresCreacion.objects.filter(proyecto = proyecto).count() >0
        except:
            # context['error'] = e
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

def HaciaTextoRecursiva(proyecto,modelo,lista_texto,size,ident):
    print('modelo ',modelo.nombre)
    texto = ''
#     lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#9b59b6"><strong>[nmo ' + modelo.nombre + ']</strong></span></span></span></p>')
#     lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion: </strong>' + '<em>[dmo ' + modelo.descripcion + ']</em></span></span></span></p>')
#     modelos_modelo = Modelo.objects.filter(padre = modelo.nombre)
#     # Ve si tiene propiedades
#     propiedades_modelo = Propiedad.objects.filter(modelo=modelo)
#     if propiedades_modelo.count() > 0:
#         ident += 10
#         lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Propiedades del Modelo :</strong>' + modelo.nombre + '</span></span></span></p>')
#         for propiedad_modelo in propiedades_modelo:
#             # size -= 1
#             lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Nombre:</strong>[npro ' + propiedad_modelo.nombre + ']</span></span></span></p>')
#             lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion:</strong>' + '<em>[dpro ' + propiedad_modelo.descripcion + ']</em></span></span></span></p>')

#             # Ve si tiene reglas
#             reglas_propiedad = Regla.objects.filter(propiedad=propiedad_modelo)
#             if reglas_propiedad.count() > 0:
#                 ident += 10
#                 lista_texto.append('<p><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Reglas de la Propiedad : ' + propiedad_modelo.nombre + '</strong></span></span></p>')
#                 for regla_propiedad in reglas_propiedad:
#                     # size -= 1
#                     lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Mensaje:</strong><em>' + regla_propiedad.mensaje + '</em></span></span></span></p>')
#                     lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Codigo: </strong><em>[dpro ' + regla_propiedad.codigo + ']</em></span></span></span></p>')

# # if modelos_modelo.count() > 0:
# #     ident += 10
# #     lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:16px"><span style="color:#000000"><strong>Modelos del Modelo: '+ modelo.nombre + '</strong></span></span></span></p>')
    for modelo_modelo in Modelo.objects.filter(padre = modelo.nombre):
        texto += '<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#9b59b6"><strong>[nmo ' + modelo_modelo.nombre + ']</strong></span></span></span></p>'
        texto += '<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion: </strong>' + '<em>[dmo ' + modelo_modelo.descripcion + ']</em></span></span></span></p>'                                      
        ReglasPropiedades(modelo_modelo,lista_texto,ident,size)
        HaciaTextoRecursiva(proyecto,modelo_modelo,lista_texto,size,ident+10)

def ReglasPropiedades(modelo,lista_texto,ident,size):
    propiedades_modelo = Propiedad.objects.filter(modelo=modelo)
    print('r1')
    if propiedades_modelo.count() > 0:
        print('r2')
        ident += 10
        lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Propiedades del Modelo :</strong>' + modelo.nombre + '</span></span></span></p>')
        print('r3')
        ident += 10
        for propiedad_modelo in propiedades_modelo:
            print('r4')
            # size -= 1
            lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Nombre:</strong>[npro ' + propiedad_modelo.nombre + ']</span></span></span></p>')
            lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Descripcion:</strong>' + '<em>[dpro ' + propiedad_modelo.descripcion + ']</em></span></span></span></p>')

            # Ve si tiene reglas
            reglas_propiedad = Regla.objects.filter(propiedad=propiedad_modelo)
            if reglas_propiedad.count() > 0:
                ident += 10
                lista_texto.append('<p><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Reglas de la Propiedad : ' + propiedad_modelo.nombre + '</strong></span></span></p>')
                for regla_propiedad in reglas_propiedad:
                    # size -= 1
                    lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Mensaje:</strong><em>' + regla_propiedad.mensaje + '</em></span></span></span></p>')
                    lista_texto.append('<p span style="margin-left:' + str(ident) + 'px"><span style="font-size:' + str(size) + 'px"><span style="color:#000000"><strong>Codigo: </strong><em>[dpro ' + regla_propiedad.codigo + ']</em></span></span></span></p>')

class CrearProyectoView(CreateView):
    model = Proyecto
    form_class = ProyectoForm

    def get_success_url(self):
        # return reverse_lazy('proyectos:home')
        return reverse_lazy('proyectos:lista') + '?criterio=' + '&duplica=0'

    def get_context_data(self,**kwargs):
        context = super(CrearProyectoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['criterio'] = self.request.GET['criterio']
        context['error'] = ''
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        user = request.user
        if user.id == None:
            return render(request, 'proyectos/proyecto_form.html', {'form': form})
        else:
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.usuario = user
                proyecto.save()
                return HttpResponseRedirect(self.get_success_url())
            return render(request, 'proyectos/proyecto_form.html', {'form': form})

class EditarProyectoView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        # proyecto = self.object
        # proyecto.save()
        return reverse_lazy('proyectos:editar', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarProyectoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.object.id,usuario=self.request.user)
            context['proyecto'] = proyecto

        except Exception as e:
            context['error'] = e
            # context['error'] = "!! No eres el propietario del proyecto !!!"
        return context


def RecursivoReporte(lista,modelo,nivel,proyecto,pospadre,strpp='',strsp='',strh = ''):
    strpp = 'primera parte ' + modelo.nombre
    lista.append(strpp)
    for mod in Modelo.objects.filter(padre=modelo,proyecto=proyecto):
        RecursivoReporte(lista,mod,nivel+1,proyecto,pospadre,strpp,strsp,strh)
    strsp = 'segunda parte ' + modelo.nombre
    lista.append(strsp)

class BorrarProyectoView(DeleteView):
    model = Proyecto
    # success_url = reverse_lazy('proyectos:lista')

    def get_success_url(self):
        # proyecto = self.object
        # proyecto.save()
        return reverse_lazy('proyectos:lista') + '?criterio=' + self.request.GET['criterio'] + '&duplica=0'

    def get_context_data(self,**kwargs):
        context = super(BorrarProyectoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            obj = Proyecto.objects.get(id=self.object.id,usuario=self.request.user)
            context['nombre'] = obj.nombre
            context['criterio'] = self.request.GET['criterio']
            context['error'] = ''
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context


# RUTINAS
# Devuelve la lista de proyectos despues de analizar criterio
def ListaProyectos(criterio,usuario):
    if criterio == None:
        return Proyecto.objects.all()
    else:
        return Proyecto.objects.filter(usuario=usuario, nombre__icontains = criterio)

from modelos.models import Modelo
from propiedades.models import Propiedad
from reglas.models import Regla

def ListaRecursiva(index,strTexto,nombre,proyecto,i,lis):
    for li in Modelo.objects.filter(padre=nombre,proyecto=proyecto):
        li.ordengeneracion = i
        li.save()
        i+=1
        lis[0] = i
        strTexto.append(str(index+1) + ',' + li.nombre)
        ListaRecursiva(index+1,strTexto,li.nombre,proyecto,i,lis)
        
# def ListaRecursiva(index,strTexto,nombre,proyecto,i):
#     for li in Modelo.objects.filter(padre=nombre,proyecto=proyecto):
#         li.ordengeneracion = i
#         li.save()
#         i+=1
#         strTexto.append(str(index+1) + ',' + li.nombre)
#         ListaRecursiva(index+1,strTexto,li.nombre,proyecto,i)

def ListaCrear(id):
    strCrear = []
    proyecto = Proyecto.objects.get(id=id)

    strTexto = []
    # for aplicacion in Aplicacion.objects.filter(proyecto=proyecto).order_by('ordengeneracion'):
    #     if aplicacion.nombre != 'core' and aplicacion.nombre != 'registration':
    #         lista = Modelo.objects.filter(padre='nada',proyecto=proyecto,aplicacion=aplicacion).order_by('ordengeneracion')

    #         orden = 1
    #         for li in lista:
    #             if orden == lista.count():
    #                 li.ordengeneracion = 10000
    #                 li.save()
    #             else:
    #                 li.ordengeneracion = orden
    #             orden += 1
    #             strTexto.append('1' + ',' + li.nombre)
    #             ListaRecursiva(1,strTexto,li.nombre,proyecto)
    
    lista = Modelo.objects.filter(padre='nada',proyecto=proyecto).order_by('ordengeneracion')
    orden = 1
    lis = [orden]
    for li in lista:
        li.ordengeneracion = lis[0]
        if orden == lista.count():
            li.ultimoregistro = 'u'
        else:
            li.ultimoregistro = 'p'
        li.save()
        lis[0] += 1
        # lis = [orden]
        strTexto.append('1' + ',' + li.nombre)
        ListaRecursiva(1,strTexto,li.nombre,proyecto,li.ordengeneracion+1,lis)
    for item in strTexto:
        strCrear.append(item)

    # lista = Modelo.objects.filter(padre='nada',proyecto=proyecto).order_by('ordengeneracion')
    # orden = 1
    # for li in lista:
    #     li.ordengeneracion = orden
    #     if orden == lista.count():
    #         li.ultimoregistro = 'u'
    #     else:
    #         li.ultimoregistro = 'p'
    #     li.save()
    #     orden += 1
    #     strTexto.append('1' + ',' + li.nombre)
    #     ListaRecursiva(1,strTexto,li.nombre,proyecto,li.ordengeneracion+1)

    # for item in strTexto:
    #     strCrear.append(item)


    identa = 0
    Crear.objects.all().delete()
    proyecto = Proyecto.objects.get(id=id)

    listacrear = Crear()
    listacrear.elemento = 'p'
    listacrear.nombre = proyecto.nombre
    listacrear.nombrepadre = 'Genesis'
    listacrear.proyectoid = proyecto.id
    listacrear.identa = identa
    listacrear.save()
    # Modelos
    for item in strCrear:
        nombre_modelo=item.split(',')[1]
        identa = int(item.split(',')[0]) * 50
        ml = Modelo.objects.get(nombre=nombre_modelo,proyecto=proyecto)
        listacrear = Crear()
        listacrear.identa = identa
        listacrear.nombre = ml.nombre
        listacrear.elemento = 'm'
        listacrear.proyectoid = proyecto.id
        listacrear.modeloid = ml.id
        aplicacion = Aplicacion.objects.get(id=ml.aplicacion.id)
        listacrear.aplicacionid = aplicacion.id
        listacrear.posicion = ml.ordengeneracion
        listacrear.ultimoregistro = ml.ultimoregistro
        listacrear.save()
        for propiedad in Propiedad.objects.filter(modelo = ml):
            listacrear = Crear()
            # identa += 50
            listacrear.identa = identa + 70
            listacrear.nombre = propiedad.nombre + ' (' + propiedad.tipo + ')'
            listacrear.elemento = 'd'
            listacrear.proyectoid = proyecto.id
            listacrear.aplicacionid = aplicacion.id
            listacrear.modeloid = ml.id
            listacrear.propiedadid = propiedad.id
            listacrear.save()

            for regla in Regla.objects.filter(propiedad = propiedad):
                listacrear = Crear()
                listacrear.identa = identa + 140
                listacrear.nombre = regla.mensaje
                listacrear.elemento = 'r'
                listacrear.proyectoid = proyecto.id
                listacrear.aplicacionid = aplicacion.id
                listacrear.modeloid = ml.id
                listacrear.propiedadid = propiedad.id
                listacrear.reglaid = regla.id
                listacrear.save()

    # # crear aplicaciones
    # pa=1
    # for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
    #     listacrear = Crear()
    #     listacrear.elemento='a'
    #     listacrear.nombre = aplicacion.nombre
    #     if pa == 1:
    #         pa=0
    #         listacrear.primero = True
    #     listacrear.proyectoid = proyecto.id
    #     listacrear.aplicacionid = aplicacion.id
    #     identa = 70
    #     listacrear.identa = 70
    #     listacrear.save()

    #     # crear modelos
    #     pm=1
    #     for modelo in Modelo.objects.filter(aplicacion=aplicacion):
    #         identa=70
    #         listacrear = Crear()
    #         listacrear.elemento ='m'
    #         listacrear.nombre = modelo.nombre
    #         listacrear.padre = modelo.padre
    #         if pm == 1:
    #             pm=0
    #             listacrear.primero = True
    #         listacrear.proyectoid = proyecto.id
    #         listacrear.aplicacionid = aplicacion.id
    #         listacrear.modeloid = modelo.id

    #         # verificar la identacion del modelo
    #         modeloi = modelo
    #         # identa += 70
    #         while modeloi.padre != 'nada':
    #             identa += 55
    #             modeloi = Modelo.objects.get(nombre=modeloi.padre , proyecto=proyecto)
    #         listacrear.identa = identa + 55
    #         listacrear.restoidenta = 12 - identa
    #         identa = listacrear.identa
    #         listacrear.save()

    #         # crear propiedades
    #         pd=1    
    #         for propiedad in Propiedad.objects.filter(modelo=modelo):
    #             listacrear = Crear()
    #             listacrear.elemento ='d'
    #             listacrear.nombre = propiedad.nombre
    #             if pd == 1:
    #                 pd=0
    #                 listacrear.primero = True
    #             listacrear.proyectoid = proyecto.id
    #             listacrear.aplicacionid = aplicacion.id
    #             listacrear.modeloid = modelo.id
    #             listacrear.propiedadid = propiedad.id
    #             listacrear.identa = identa + 55
    #             listacrear.restoidenta = 12 - (identa + 1)
    #             # identa = listacrear.identa
    #             listacrear.save()

    #             # crear reglas
    #             pr=1    
    #             for regla in Regla.objects.filter(propiedad=propiedad):
    #                 listacrear = Crear()
    #                 listacrear.elemento ='r'
    #                 listacrear.nombre = regla.mensaje
    #                 if pr == 1:
    #                     pr=0
    #                     listacrear.primero = True
    #                 listacrear.proyectoid = proyecto.id
    #                 listacrear.aplicacionid = aplicacion.id
    #                 listacrear.modeloid = modelo.id
    #                 listacrear.propiedadid = propiedad.id
    #                 listacrear.reglaid = regla.id
    #                 listacrear.identa = identa + 110
    #                 listacrear.restoidenta = 12 - (identa + 2)
    #                 identa = listacrear.identa
    #                 listacrear.save()

    lista = Crear.objects.all()

    return lista

import shutil
from django.views import View

class dumpView(View):

    def get(self, request):
        vigente = VerificaVigenciaUsuario(self.request.user)
        try:
            error = ''
            user = self.request.user
            proyecto = Proyecto.objects.get(usuario = self.request.user, id = self.request.GET['proyecto_id'])
            etapa = 'CrearZip'
            # Borrar los errores de generacion

            # Borrar los errores
            ErroresCreacion.objects.filter(proyecto=proyecto.nombre,usuario=user.username).delete()
            # Leer los directorios
            gen = Genesis.objects.get(nombre='GENESIS')

            # Leer el archivo download.html
            stri =  views.LeerArchivoEnTexto(gen.directoriotexto + 'download_file.html',etapa,proyecto.nombre,user.username )
            # Reemplazar nombre de archivo
            stri = stri.replace('@file', user.username + '/' + proyecto.nombre + '.zip')
            stri = stri.replace('@nombrefile', proyecto.nombre + '.zip')
            # Grabar el nuevo download en el directorio proyectos/username/
            views.EscribirEnArchivo(gen.directoriogenesis + 'proyectos/templates/proyectos/' + user.username + '/download.html',stri,etapa,proyecto.nombre,user.username) 

            # leer el directorio de genesis
            cdzip = gen.directoriogenesis + 'core/static/core/zipfiles/' + user.username + '/' + proyecto.nombre
            cdarchivoazipear = gen.directoriozip + proyecto.nombre
            try:
                shutil.make_archive(cdzip, 'zip', cdarchivoazipear )
            except:
                # Si no existe se crear solo el directorio del proyecto
                views.CrearDirectorio(cdarchivoazipear,etapa,user.username,user.username,True)
                shutil.make_archive(cdzip, 'zip', cdarchivoazipear )
            return render(request, 'proyectos/' + user.username + '/download.html' ,{'nombre':proyecto.nombre, 'proyecto': proyecto,'vigente':vigente,'error':error})             
        except:
            error = '!!! No eres el propietario del proyecto !!!'            
            return render(request, 'proyectos/' + user.username + '/download.html' ,{'nombre':proyecto.nombre, 'proyecto': proyecto,'vigente':vigente,'error':error})             


        # proyecto = Proyecto.objects.get(usuario = self.request.user, id = self.request.GET['proyecto_id'])

        # user = self.request.user

        # gen = Genesis.objects.get(nombre='GENESIS')
        # # leer el directorio de genesis
        # cdzip = gen.directorio + '/core/static/core/zipfiles/' + user.username + '/proyecto'
        # cdarchivoazipear = gen.directoriozip + proyecto.nombre
        # shutil.make_archive(cdzip, 'zip', cdarchivoazipear )
        # return render(request, 'proyectos/' + user.username + '/download.html' ,{'nombre':proyecto.nombre})             

class DesplegarPreciosView(TemplateView):
    template_name = "proyectos/desplegar_precios.html"

    def post(self, request, *args, **kwargs):
        # crea la licencia gratuita
        lic = LicenciaUso()
        lic.usuario = self.request.user
        lic.opcion = 1
        lic.inicio = timezone.now()
        lic.expira = timezone.now() + datetime.timedelta(days=6000)
        lic.save()

        return self.get(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super(DesplegarPreciosView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        puede = 's'
        # Uso gratuito
        if LicenciaUso.objects.filter(usuario=self.request.user,opcion=1).count() == 1:
            lic = LicenciaUso.objects.get(usuario=self.request.user,opcion=1)
            if lic.expira > timezone.now():
                context['expira'] = 'Expirada'
            context['expira'] = lic.expira
            puede = 'n'
        context['puede'] = puede
        context['username'] = self.request.user.username
        lista = []
        for precio in Precio.objects.all():
            dt=Genesis.objects.get(nombre='GENESIS').directoriotexto
            stri = views.LeerArchivo(dt + precio.paypal,'','','')
            lista.append([precio.titulo, precio.descripcion, precio.importe,stri])
        context['precios'] = lista
        context['error'] = ''
        return context  


class ListaTextoView(ListView):
    model = ProyectoTexto

    def get_context_data(self, **kwargs):
        context = super(ListaTextoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['lista_texto'] = ProyectoTexto.objects.filter(usuario=self.request.user)
        context['error'] = ''
        context['criterio'] = self.request.GET['criterio']
        return context

class CrearTextoView(CreateView):
    model = ProyectoTexto
    form_class = ProyectoTextoForm

    def get_success_url(self):
        # return reverse_lazy('proyectos:home')
        return reverse_lazy('proyectos:lista_texto') + '?criterio=' + self.request.GET['criterio']

    def get_context_data(self,**kwargs):
        context = super(CrearTextoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['error'] = ''
        context['criterio'] = self.request.GET['criterio']
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        user = request.user
        if form.is_valid():
            proyectotexto = form.save(commit=False)
            proyectotexto.usuario = user
            proyectotexto.save()
            return HttpResponseRedirect(self.get_success_url())
        return render(request, 'proyectos/proyectotexto_form.html', {'form': form})

class EditarTextoView(UpdateView):
    model = ProyectoTexto
    form_class = ProyectoTextoForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('proyectos:editar_texto', args=[self.object.id]) + '?ok' + '&criterio=' + self.request.GET['criterio']

    def get_context_data(self,**kwargs):
        context = super(EditarTextoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['error'] = ''
        context['criterio'] = self.request.GET['criterio']
        context['etiquetas'] = Etiquetas
        return context

def Etiquetas():
    try:
        lista = []
        lista.append(['','PROYECTOS','t'])
        lista.append(['npr','Nombre del Proyecto','e'])
        lista.append(['dpr','Descripcion del Proyecto','e'])
        lista.append(['cpp','Color de la pagina principal','e'])
        lista.append(['tit','Titulo del Proyecto','e'])
        lista.append(['pcs','El Proyecto tiene seguridad','e'])
        lista.append(['pce','Codigo del Proyecto con etiquetas de personalizacion','e'])
        lista.append(['pcb','Proyecto con opcion de busqueda','e'])
        lista.append(['ses','Separacion entre secciones','e'])
        lista.append(['avw','Ancho del Logo del Proyecto','e'])
        lista.append(['avh','Alto del Logo del Proyecto','e'])
        lista.append(['itw','Ancho de la imagen del Titulo','e'])
        lista.append(['ith','Alto de la imagen del Titulo','e'])
        lista.append(['fti','Font del Titulo','e'])
        lista.append(['cti','Color del texto del Titulo','e'])
        lista.append(['act','Alto de la columna del Titulo','e'])
        lista.append(['nct','Numero de columnas de la columna del Titulo','e'])
        lista.append(['cct','Color de la columna del Titulo','e'])
        lista.append(['jht','Justificacion horizontal del Titulo','e'])
        lista.append(['jvt','Justificacion vertical del Titulo','e'])
        lista.append(['afs','Altura de la fila superior','e'])
        lista.append(['cfs','Color de la fila superior','e'])
        lista.append(['nci','Numero de columnas de la columna superior izquierda','e'])
        lista.append(['aci','Altura de la columna superior izquierda','e'])
        lista.append(['cci','Color de la columna superior izquierda','e'])
        lista.append(['ncd','Numero de columnas de la columna superior derecha','e'])
        lista.append(['acd','Altura de la columna superior derecha','e'])
        lista.append(['ccd','Color de la columna superior derecha','e'])
        lista.append(['acl','Altura de la columna del Logo','e'])
        lista.append(['ccl','Color de la columna del Logo','e'])
        lista.append(['ncl','Numero de las columnas de la columna del Logo','e'])
        lista.append(['jhl','Justificacion horizontal del Logo','e'])
        lista.append(['jvl','Justificacion vertical del Logo','e'])
        lista.append(['acg','Altura de la columna de Login','e'])
        lista.append(['ncg','Numero de columnas de la columna de Login','e'])
        lista.append(['ccg','Color de la columna de Login','e'])
        lista.append(['bss','Borde de las secciones de la fila superior','e'])
        lista.append(['cbss','Color borde de las secciones de la fila superior','e'])
        lista.append(['abss','Ancho borde de las secciones de la fila superior','e'])
        lista.append(['afb','Alto de la fila de bus-menu','e'])
        lista.append(['cfb','Color de la fila de bus-menu','e'])
        lista.append(['ncbi','Numero de columnas de la columna bus-menu izquierda ','e'])
        lista.append(['acbi','Altura de la columna bus-menu izquierda','e'])
        lista.append(['ccbi','Color de la columna bus-menu izquierda','e'])
        lista.append(['ncbd','Numero de columnas de la columna bus-menu derecha','e'])
        lista.append(['acbd','Altura de la columna bus-menu derecha','e'])
        lista.append(['ccbd','Color de la columna bus-menu derecha','e'])
        lista.append(['acb','Altura de la columna de busqueda','e'])
        lista.append(['ncb','Numero de columnas de la columna de busqueda','e'])
        lista.append(['ccb','Color de la columna de busqueda','e'])
        lista.append(['acm','Altura de la columna del menu','e'])
        lista.append(['ncm','Numero de columnas de la columna del menu','e'])
        lista.append(['ccm','Color de la columna del menu','e'])
        lista.append(['cme','Color de las opciones del menu','e'])
        lista.append(['fme','Font de la opcion del menu','e'])
        lista.append(['bme','Borde de las secciones de la fila de busqueda y menu','e'])
        lista.append(['abme','Ancho del borde de las secciones de la fila de busqueda y menu','e'])
        lista.append(['cbme','Color del borde de las secciones de la fila de busqueda y menu','e'])
        lista.append(['afm','Altura de la fila del medio','e'])
        lista.append(['cfm','Color de la fila del medio','e'])
        lista.append(['jum','Justificacion del menu','e'])
        lista.append(['acmi','Altura de la columna izquierda del medio','e'])
        lista.append(['ncmi','Numero de columnas de la la columna izquierda del medio','e'])
        lista.append(['ccmi','Color de la columna izquierda del medio','e'])
        lista.append(['acmc','Altura de la columna central del medio','e'])
        lista.append(['ncmc','Numero de columnas de la columna central del medio','e'])
        lista.append(['ccmc','Color de la columna central del medio','e'])
        lista.append(['acmd','Altura de la columna derecha del medio','e'])
        lista.append(['ncmd','Numero de columnas de la columna derecha del medio','e'])
        lista.append(['ccmd','Color de la columna derecha del medio','e'])
        lista.append(['txm','Texto de la columna central del medio','e'])
        lista.append(['ctxm','Color del texto de la columna central del medio','e'])
        lista.append(['ftxm','Font del texto de la columna central del medio','e'])
        lista.append(['afp','Alto de la fila del pie','e'])
        lista.append(['cfp','Color de la fila del pie','e'])
        lista.append(['acp','Altura de la columna del pie','e'])
        lista.append(['ccp','Color de la columna del pie','e'])
        lista.append(['txv','Texto de la opcion volver','e'])
        lista.append(['ftxv','Font del texto de la opcion volver','e'])
        lista.append(['ctxv','Color del texto de la opcion volver','e'])
        lista.append(['','APLICACIONES','t'])
        lista.append(['nap','Nombre de la Aplicacion','e'])
        lista.append(['dap','Descripcion de la Aplicacion','e'])
        lista.append(['txma','Texto de la opcion en el menu','e'])
        lista.append(['as','Para acceder a la Aplicacion se debe ser miembro del staff','e'])
        lista.append(['al','Para acceder a la Aplicacion se debe etar autenticado','e'])
        lista.append(['tta','ToolTip en la opcion del menu','e'])
        lista.append(['oga','Orden de generacion de la aplicacion','e'])
        lista.append(['','MODELOS','t'])
        lista.append(['nmo','Nombre del Modelo','e'])
        lista.append(['dmo','Descripcion del Modelo','e'])
        lista.append(['pmo','Padre del Modelo','e'])
        lista.append(['smo','Identificacion self del Modelo','e'])
        lista.append(['bmo','Identificacion de borrado del Modelo','e'])
        lista.append(['amo','Aplicacion del Modelo','e'])
        lista.append(['tom','Texto para la opcion del menu','e'])
        lista.append(['ttm','ToolTip de la opcion del menu','e'])
        lista.append(['tli','Titulo de la lista del Modelo','e'])
        lista.append(['ftli','Font del titulo de la lista del Modelo','e'])
        lista.append(['cftl','Color de fondo del titulo de la lista','e'])
        lista.append(['ctli','Color del titulo de la lista','e'])
        lista.append(['atli','Altura del titulo de la lista','e'])
        lista.append(['mtli','El titulo de la lista esta en mayusculas','e'])
        lista.append(['jvtl','Justificacion vertical del titulo de la lista','e'])
        lista.append(['jhtl','Justificacion horizontal del titulo de la lista','e'])
        lista.append(['fcli','Fonto del comentario de la lista','e'])
        lista.append(['cmli','Texto del comentario de la lista','e'])
        lista.append(['cfcml','Color de fondo del comentario de la lista','e'])
        lista.append(['ccmli','Color del texto del comentario de la lista','e'])
        lista.append(['mco','Las columnas estan en mayusculas','e'])
        lista.append(['aco','Altura de las columnas','e'])
        lista.append(['cfcl','Color del fondo de las columnas de la lista','e'])
        lista.append(['ccli','Color del texto de las columnas de la lista','e'])
        lista.append(['fcli','Font del texto de las columnas de la lista','e'])
        lista.append(['clcb','La columna de la lista tiene borde','e'])
        lista.append(['ftxl','Font del texto de la lista','e'])
        lista.append(['cftxc','Color de fondo del texto de la lista','e'])
        lista.append(['ctxl','Color del texto de la lista','e'])
        lista.append(['feb','Font texto editar borrar','e'])
        lista.append(['ceb','Color del texto editar borrar','e'])
        lista.append(['teb','Texto de Editar y Borrar','e'])
        lista.append(['flnm','Font del link de nuevo modelo','e'])
        lista.append(['clnm','Color del link de nuevo modelo','e'])
        lista.append(['tlnm','Texto del link de nuevo modelo','e'])
        lista.append(['lnm','La opcion de nuevo modelo es un link','e'])
        lista.append(['tin','Titulo de formulario nuevo Modelo','e'])
        lista.append(['ftin','Font del titulo del formulario nuevo Modelo','e'])
        lista.append(['ctin','Color del titulo del formulario nuevo Modelo','e'])
        lista.append(['cfti','Color de fondo del titulo del formulario nuevo Modelo','e'])
        lista.append(['cffti','Color de fondo de la fila del titulo del formulario nuevo Modelo','e'])
        lista.append(['afti','Altura de la fila del titulo del formulario nuevo Modelo','e'])
        lista.append(['jvti','Justificacion vertical del titulo del formulario nuevo Modelo','e'])
        lista.append(['jhti','Justificacion horizontal del titulo del formulario nuevo Modelo','e'])
        lista.append(['cfci','Color de fondo del comentario del formulario nuevo Modelo','e'])
        lista.append(['ccin','Color del comentario del formulario nuevo Modelo','e'])
        lista.append(['fcin','Font del comentario del formulario nuevo Modelo','e'])
        lista.append(['cin','Texto del comentario del formulario nuevo Modelo','e'])
        lista.append(['ncii','Numero columnas del margen izquierdo formulario nuevo Modelo','e'])
        lista.append(['ncmi','Numero de columnas para formulario nuevo Modelo','e'])
        lista.append(['ncdi','Numero columnas del margen derecho formulario nuevo Modelo','e'])
        lista.append(['tup','Titulo de formulario editar Modelo','e'])
        lista.append(['ftup','Font del titulo del formulario editar Modelo','e'])
        lista.append(['ctup','Color del titulo del formulario editar Modelo','e'])
        lista.append(['cftu','Color de fondo del titulo del formulario editar Modelo','e'])
        lista.append(['cfftu','Color de fondo de la fila del titulo del formulario editar Modelo','e'])
        lista.append(['aftu','Altura de la fila del titulo del formulario editar Modelo','e'])
        lista.append(['jvtu','Justificacion vertical del titulo del formulario editar Modelo','e'])
        lista.append(['jhtu','Justificacion horizontal del titulo del formulario editar Modelo','e'])
        lista.append(['cup','Texto del comentario del formulario nuevo Modelo','e'])
        lista.append(['cfcu','Color de fondo del comentario del formulario nuevo Modelo','e'])
        lista.append(['fcup','Font del comentario del formulario editar Modelo','e'])
        lista.append(['ccup','Color del comentario del formulario editar Modelo','e'])
        lista.append(['nciu','Numero columnas del margen izquierdo formulario editar Modelo','e'])
        lista.append(['ncdu','Numero columnas del margen derecho formulario editar Modelo','e'])
        lista.append(['ncmu','Numero de columnas para formulario editar Modelo','e'])
        lista.append(['flm','Font de las etiquetas','e'])
        lista.append(['clm','Color de las etiquetas','e'])
        lista.append(['cau','Lo constroles se crean de forma automatica','e'])
        lista.append(['tbo','Titulo de formulario borrar Modelo','e'])
        lista.append(['ftbo','Font del titulo del formulario borrar Modelo','e'])
        lista.append(['cftb','Color de fondo del titulo del formulario borrar Modelo','e'])
        lista.append(['cfftb','Color de fondo de la fila del titulo del formulario borrar Modelo','e'])
        lista.append(['aftb','Altura de la fila del titulo del formulario borrar Modelo','e'])
        lista.append(['jvtb','Justificacion vertical del titulo del formulario borrar Modelo','e'])
        lista.append(['jhtb','Justificacion horizontal del titulo del formulario borrar Modelo','e'])
        lista.append(['cfcb','Color de fondo del comentario del formulario borrar Modelo','e'])
        lista.append(['ccbo','Color del comentario del formulario borrar Modelo','e'])
        lista.append(['fcbo','Font del comentario del formulario borrar Modelo','e'])
        lista.append(['cbo','Texto del comentario del formulario borrar Modelo','e'])
        lista.append(['cftxb','Color del fondo del texto borrar del formulario borrar Modelo','e'])
        lista.append(['ctxb','Color del texto borrar del formulario borrar Modelo','e'])
        lista.append(['ftxb','Font del texto borrar del formulario borrar Modelo','e'])
        lista.append(['txbo','Texto de borrar del formulario borrar Modelo','e'])
        lista.append(['txbb','Texto del boton borrar del formulario borrar Modelo','e'])
        lista.append(['ncib','Numero columnas del margen izquierdo formulario borrar Modelo','e'])
        lista.append(['ncdb','Numero columnas del margen derecho formulario borrar Modelo','e'])
        lista.append(['ncmb','Numero de columnas para formulario borrar Modelo','e'])
        lista.append(['hco','Los hijos del Modelo son contiguos','e'])
        lista.append(['nchu','Numero columnas del margen derecho editar Hijos','e'])
        lista.append(['ls','Para la lista se debe pertenecer al staff','e'])
        lista.append(['ll','Para la lista se debe estar autenticado','e'])
        lista.append(['cs','Para un nuevo Modelo se debe pertenecer al staff','e'])
        lista.append(['cl','Para un nuevo Modelo se debe estar autenticado','e'])
        lista.append(['es','Para editar un Modelo debe pertenecer al staff','e'])
        lista.append(['el','Para editar un modelo se debe estra autenticado','e'])
        lista.append(['bc','Para borrar un Modelo de debe pertenecer al staff','e'])
        lista.append(['bl','Para borrar un Modelo se debe estar autenticado','e'])
        lista.append(['nclb','Numero de columnas para las etiquetas','e'])
        lista.append(['ncct','Numero de columnas para los controles','e'])
        lista.append(['msb','El Modelo no esta en la base de datos','e'])
        lista.append(['','PROPIEDADES','t'])
        lista.append(['npro','Nombre de la Propiedad','e'])
        lista.append(['dpro','Descripcion de la Propiedad','e'])
        lista.append(['tpro','Tipo de la Propiedad','e'])
        lista.append(['','s - String','p'])
        lista.append(['','x - Text Field','p'])
        lista.append(['','h - RichText','p'])
        lista.append(['','m - Entero small','p'])
        lista.append(['','i - Entero','p'])
        lista.append(['','l - Entero long','p'])
        lista.append(['','d - Decimal','p'])
        lista.append(['','f - Foranea','p'])
        lista.append(['','n - Fecha','p'])
        lista.append(['','t - Hora y Fecha','p'])
        lista.append(['','e - Hora','p'])
        lista.append(['','b - Boolean','p'])
        lista.append(['','r - Radio Button','p'])
        lista.append(['','p - Imagen','p'])
        lista.append(['','u - Usuario','p'])
        lista.append(['prf','Modelo para Propiedad foranea','e'])
        lista.append(['txb','Texto de los Radio Buttons','e'])
        lista.append(['vdf','Valor inicial por defecto','e'])
        lista.append(['lst','Longitud de una Propiedad tipo string','e'])
        lista.append(['tph','Texto del PlaceHolder','e'])
        lista.append(['epro','Etiqueta de la Propiedad en el formulario','e'])
        lista.append(['enl','La Propedad se despliega en la lista del Modelo','e'])
        lista.append(['emb','La Propiedad puede ser vista en Mobile','e'])
        lista.append(['ncl','Numero de columnas de la Propiedad en la lista del Modelo','e'])
        lista.append(['txc','Texto de la columna en la lista del Modelo','e'])
        lista.append(['jtxc','Justificacion horizontal del texto en la columna de la lista','e'])
        lista.append(['ffch','Formato de la Propiedad tipo DateTime','e'])
        lista.append(['ear','La etiqueta se coloca arriba del control en el formulario','e'])
        lista.append(['mdt','La Propiedad es mandatoria','e'])
        lista.append(['','REGLAS','t'])
        lista.append(['msj','Mensaje de error cuando se incumple la Regla','e'])
        lista.append(['crg','Codigo de la Regla','e'])
        return lista
    except:
        return''

class BorrarTextoView(DeleteView):
    model = ProyectoTexto

    def get_success_url(self):
        return reverse_lazy('proyectos:lista_texto') + '?criterio=' + self.request.GET['criterio']

    def get_context_data(self,**kwargs):
        context = super(BorrarTextoView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['error'] = ''
        context['criterio'] = self.request.GET['criterio']
        return context

class ProcesaTextoView(TemplateView):
    template_name = "proyectos/proyecto_procesa_texto.html"

    def get_context_data(self,**kwargs):
        context = super(ProcesaTextoView, self).get_context_data(**kwargs)
        print('1')
        texto_procesar = ProyectoTexto.objects.get(id=self.request.GET['id'])
        print('texto procesar ',texto_procesar.texto)
        try:
            Proyecto.objects.get(id=texto_procesar.proyecto).delete()
        except:
            pass
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['error'] = ''
        context['criterio'] = self.request.GET['criterio']

        caracteres_especiales = []
        caracteres_especiales.append(['&#39;',"'"])
        caracteres_especiales.append(['&quot;','"'])
        caracteres_especiales.append(['&lt;','<'])
        caracteres_especiales.append(['&gt;','>'])
        Texto = texto_procesar.texto

        # Cambiar caracteres espaciales

        for car in caracteres_especiales:
            Texto = Texto.replace(car[0],car[1])
            
        # Comienza en proceso
        # Proyecto que se crea
        tag = ''

        try:
            proyecto = Proyecto()
            aplicacion = None
            modelo = None
            propiedad = None
            regla = None
            nap = 1
            nmo = 1
            npr = 1
            nrg = 1
            proyecto.usuario = self.request.user
            context['mensaje'] = Texto
            strTexto = Texto.split('[')
            for parrafo in strTexto:
                if parrafo != '':
                    strTag = parrafo.split(']')
                    elemento = strTag[0].replace('&nbsp;',' ').split(' ')
                    elementos = ''
                    for i in range(len(elemento)):
                        if i != 0:
                            if i < len(elemento)-1 :
                                elementos += elemento[i] + ' '
                            else:
                                elementos += elemento[i]
                    tag = elemento[0]
                    if tag == 'npr':
                        print(tag)
                        proyecto.nombre =  ProcesaTags(elementos,'nuevo')
                    if tag == 'dpr':
                        proyecto.descripcion =  ProcesaTags(elementos,'Descripcion')
                    if tag == 'cpp':
                        proyecto.colorpaginaprincipal =  ProcesaTags(elementos,proyecto.colorpaginaprincipal)
                    if tag == 'tit':
                        proyecto.titulo =  ProcesaTags(elementos,proyecto.titulo)
                    if tag == 'pcs':
                        proyecto.conseguridad =  True
                    if tag == 'pce':
                        proyecto.conetiquetaspersonalizacion = True
                    if tag == 'pcb':
                        proyecto.conbusqueda = True
                    if tag == 'avw':
                        proyecto.avatarwidth = ProcesaTags(elementos,proyecto.avatarwidth)
                    if tag == 'ses':
                        proyecto.separacionsecciones = ProcesaTags(elementos,proyecto.separacionsecciones)
                    if tag == 'avh':
                        proyecto.avatarheight = ProcesaTags(elementos,proyecto.avatarheight)
                    if tag == 'itw':
                        proyecto.imagentitulowidth = ProcesaTags(elementos,proyecto.imagentitulowidth)
                    if tag == 'ith':
                        proyecto.imagentituloheight = ProcesaTags(elementos,proyecto.imagentituloheight)
                    if tag == 'fti':
                        proyecto.fonttitulo = ProcesaTags(elementos,proyecto.fonttitulo)
                    if tag == 'cti':
                        proyecto.colortitulo = ProcesaTags(elementos,proyecto.colortitulo)
                    if tag == 'act':
                        proyecto.altocolumnatitulo = ProcesaTags(elementos,proyecto.altocolumnatitulo)
                    if tag == 'nct':
                        proyecto.numerocolumnatitulo = ProcesaTags(elementos,proyecto.numerocolumnatitulo)
                    if tag == 'cct':
                        proyecto.colorcolumnatitulo = ProcesaTags(elementos,proyecto.colorcolumnatitulo)
                    if tag == 'jht':
                        proyecto.justificacionhorizontaltitulo = ProcesaTags(elementos,proyecto.justificacionhorizontaltitulo)
                    if tag == 'jvt':
                        proyecto.justificacionverticaltitulo = ProcesaTags(elementos,proyecto.justificacionverticaltitulo)
                    if tag == 'afs':
                        proyecto.altofilaenizcede = ProcesaTags(elementos,proyecto.altofilaenizcede)
                    if tag == 'cfs':
                        proyecto.colorfilaenizcede = ProcesaTags(elementos,proyecto.colorfilaenizcede)
                    if tag == 'nci':
                        proyecto.numerocolumnaenizquierda = ProcesaTags(elementos,proyecto.numerocolumnaenizquierda)
                    if tag == 'aci':
                        proyecto.altocolumnaenizquierda = ProcesaTags(elementos,proyecto.altocolumnaenizquierda)
                    if tag == 'cci':
                        proyecto.colorcolumnaenizquierda = ProcesaTags(elementos,proyecto.colorcolumnaenizquierda)
                    if tag == 'ncd':
                        proyecto.numerocolumnaenderecha = ProcesaTags(elementos,proyecto.numerocolumnaenderecha)
                    if tag == 'acd':
                        proyecto.altocolumnaenderecha = ProcesaTags(elementos,proyecto.altocolumnaenderecha)
                    if tag == 'ccd':
                        proyecto.colorcolumnaenderecha = ProcesaTags(elementos,proyecto.colorcolumnaenderecha)
                    if tag == 'ncl':
                        proyecto.numerocolumnalogo = ProcesaTags(elementos,proyecto.numerocolumnalogo)
                    if tag == 'acl':
                        proyecto.altocolumnalogo= ProcesaTags(elementos,proyecto.altocolumnalogo)
                    if tag == 'ccl':
                        proyecto.colorcolumnalogo = ProcesaTags(elementos,proyecto.colorcolumnalogo)
                    if tag == 'jhl':
                        proyecto.justificacionhorizontallogo = ProcesaTags(elementos,proyecto.justificacionhorizontallogo)
                    if tag == 'jvl':
                        proyecto.justificacionverticallogo = ProcesaTags(elementos,proyecto.justificacionverticallogo)
                    if tag == 'ncg':
                        proyecto.numerocolumnalogin = ProcesaTags(elementos,proyecto.numerocolumnalogin)
                    if tag == 'acg':
                        proyecto.altocolumnalogin = ProcesaTags(elementos,proyecto.altocolumnalogin)
                    if tag == 'ccg':
                        proyecto.colorcolumnalogin = ProcesaTags(elementos,proyecto.colorcolumnalogin)
                    if tag == 'bss':
                        proyecto.enborde = True
                    if tag == 'cbss':
                        proyecto.encolorborde = ProcesaTags(elementos,proyecto.encolorborde)
                    if tag == 'abss':
                        proyecto.enanchoborde = ProcesaTags(elementos,proyecto.enanchoborde)
                    if tag == 'afb':
                        proyecto.altofilabume = ProcesaTags(elementos,proyecto.altofilabume)
                    if tag == 'cfb':
                        proyecto.colorfilabume = ProcesaTags(elementos,proyecto.colorfilabume)
                    if tag == 'ncbi':
                        proyecto.numerocolumnabumeizquierda = ProcesaTags(elementos,proyecto.numerocolumnabumeizquierda)
                    if tag == 'acbi':
                        proyecto.altocolumnabumeizquierda = ProcesaTags(elementos,proyecto.altocolumnabumeizquierda)
                    if tag == 'ccbi':
                        proyecto.colorcolumnabumeizquierda = ProcesaTags(elementos,proyecto.colorcolumnabumeizquierda)
                    if tag == 'ncbd':
                        proyecto.numerocolumnabumederecha = ProcesaTags(elementos,proyecto.numerocolumnabumederecha)
                    if tag == 'acbd':
                        proyecto.altocolumnabumederecha = ProcesaTags(elementos,proyecto.altocolumnabumederecha)
                    if tag == 'ccbd':
                        proyecto.colorcolumnabumederecha = ProcesaTags(elementos,proyecto.colorcolumnabumederecha)
                    if tag == 'ncb':
                        proyecto.numerocolumnabusqueda = ProcesaTags(elementos,proyecto.numerocolumnabusqueda)
                    if tag == 'acb':
                        proyecto.altocolumnabusqueda = ProcesaTags(elementos,proyecto.altocolumnabusqueda)
                    if tag == 'ccb':
                        proyecto.colorcolumnabusqueda = ProcesaTags(elementos,proyecto.colorcolumnabusqueda)
                    if tag == 'ncm':
                        proyecto.numerocolumnamenu = ProcesaTags(elementos,proyecto.numerocolumnamenu)
                    if tag == 'acm':
                        proyecto.altocolumnamenu = ProcesaTags(elementos,proyecto.altocolumnamenu)
                    if tag == 'ccm':
                        proyecto.colorcolumnamenu = ProcesaTags(elementos,proyecto.colorcolumnamenu)
                    if tag == 'cme':
                        proyecto.colormenu = ProcesaTags(elementos,proyecto.colormenu)
                    if tag == 'fme':
                        proyecto.fontmenu = ProcesaTags(elementos,proyecto.fontmenu)
                    if tag == 'jum':
                        proyecto.justificacionmenu = ProcesaTags(elementos,proyecto.justificacionmenu)
                    if tag == 'bme':
                        proyecto.bumeborde = True
                    if tag == 'cbme':
                        proyecto.bumecolorborde = ProcesaTags(elementos,proyecto.bumecolorborde)
                    if tag == 'abme':
                        proyecto.bumeanchoborde = ProcesaTags(elementos,proyecto.bumeanchoborde)
                    if tag == 'afm':
                        proyecto.altofilamedio = ProcesaTags(elementos,proyecto.altofilamedio)
                    if tag == 'cfm':
                        proyecto.colorfilamedio = ProcesaTags(elementos,proyecto.colorfilamedio)
                    if tag == 'acmi':
                        proyecto.altocolumnamedioizquierda = ProcesaTags(elementos,proyecto.altocolumnamedioizquierda)
                    if tag == 'ncmi':
                        proyecto.numerocolumnamedioizquierda = ProcesaTags(elementos,proyecto.numerocolumnamedioizquierda)
                    if tag == 'ccmi':
                        proyecto.colorcolumnamedioizquierda = ProcesaTags(elementos,proyecto.colorcolumnamedioizquierda)
                    if tag == 'acmc':
                        proyecto.altocolumnamediocentro = ProcesaTags(elementos,proyecto.altocolumnamediocentro)
                    if tag == 'ncmc':
                        proyecto.numerocolumnamediocentro = ProcesaTags(elementos,proyecto.numerocolumnamediocentro)
                    if tag == 'ccmc':
                        proyecto.colorcolumnamediocentro = ProcesaTags(elementos,proyecto.colorcolumnamediocentro)
                    if tag == 'acmd':
                        proyecto.altocolumnamedioderecha = ProcesaTags(elementos,proyecto.altocolumnamedioderecha)
                    if tag == 'ncmd':
                        proyecto.numerocolumnamedioderecha = ProcesaTags(elementos,proyecto.numerocolumnamedioderecha)
                    if tag == 'ccmd':
                        proyecto.colorcolumnamedioderecha = ProcesaTags(elementos,proyecto.colorcolumnamedioderecha)
                    if tag == 'txm':
                        proyecto.textomedio = ProcesaTags(elementos,proyecto.textomedio)
                    if tag == 'ctxm':
                        proyecto.colortextomedio = ProcesaTags(elementos,proyecto.colortextomedio)
                    if tag == 'ftxm':
                        proyecto.fonttextomedio = ProcesaTags(elementos,proyecto.fonttextomedio)
                    if tag == 'afp':
                        proyecto.altofilapie = ProcesaTags(elementos,proyecto.altofilapie)
                    if tag == 'cfp':
                        proyecto.colorfilapie = ProcesaTags(elementos,proyecto.colorfilapie)
                    if tag == 'afm':
                        proyecto.altofilamedio = ProcesaTags(elementos,proyecto.altofilamedio)
                    if tag == 'acp':
                        proyecto.altocolumnapie = ProcesaTags(elementos,proyecto.altocolumnapie)
                    if tag == 'ccp':
                        proyecto.colorcolumnapie = ProcesaTags(elementos,proyecto.colorcolumnapie)
                    if tag == 'txv':
                        proyecto.textovolver = ProcesaTags(elementos,proyecto.textovolver)
                    if tag == 'ftxv':
                        proyecto.fonttextovolver = ProcesaTags(elementos,proyecto.fonttextovolver)
                    if tag == 'ctxv':
                        proyecto.colortextovolver = ProcesaTags(elementos,proyecto.colortextovolver)
                    proyecto.save()
                    # Aplicaciones
                    if tag == 'nap':
                        aplicacion = Aplicacion()
                        aplicacion.proyecto = proyecto
                        aplicacion.nombre = ProcesaTags(elementos,'app' + str(nap))
                        nap += 1
                    if aplicacion != None:
                        if tag == 'nap':
                            aplicacion.descripcion = ProcesaTags(elementos,'app desc')
                        if tag == 'txma':
                            aplicacion.textoenmenu = ProcesaTags(elementos,aplicacion.textoenmenu)
                        if tag == 'tta':
                            aplicacion.tooltip = ProcesaTags(elementos,aplicacion.tooltip)
                        if tag == 'oga':
                            aplicacion.ordengeneracion = ProcesaTags(elementos,aplicacion.ordengeneracion)
                        if tag == 'hlg':
                            aplicacion.homelogin = True
                        if tag == 'hst':
                            aplicacion.homestaff = True
                        aplicacion.save()
                    # Modelos
                    if tag == 'nmo':
                        modelo = Modelo()
                        modelo.proyecto = proyecto
                        modelo.aplicacion = aplicacion
                        modelo.nombre = ProcesaTags(elementos,'modelo' + str(nmo))
                        print('modelos ',modelo.nombre)
                        nmo += 1
                    if modelo != None:
                        if tag == 'dmo':
                            modelo.descripcion = ProcesaTags(elementos,modelo.descripcion)
                            print('self ',modelo.descripcion)
                        if tag == 'pmo':
                            modelo.padre = ProcesaTags(elementos,modelo.padre)
                        if tag == 'smo':
                            modelo.nombreself = ProcesaTags(elementos,modelo.nombreself)
                        if tag == 'bmo':
                            modelo.nombreborrar = ProcesaTags(elementos,modelo.nombreborrar)
                        if tag == 'amo':
                            napp = ProcesaTags(elementos,aplicacion.nombre)
                            aplicacion = Aplicacion.objects.get(nombre=napp,proyecto=proyecto)
                            modelo.aplicacion = aplicacion
                        if tag == 'tom':
                            modelo.textoopcionmenu = ProcesaTags(elementos,modelo.textoopcionmenu)
                        if tag == 'ttm':
                            modelo.tooltip = ProcesaTags(elementos,modelo.tooltip)
                        if tag == 'tli':
                            modelo.titulolista = ProcesaTags(elementos,modelo.titulolista)
                        if tag == 'ftli':
                            modelo.fonttitulolista = ProcesaTags(elementos,modelo.fonttitulolista)
                        if tag == 'cftl':
                            modelo.colorfondotitulolista = ProcesaTags(elementos,modelo.colorfondotitulolista)
                        if tag == 'ctli':
                            modelo.colortitulolista = ProcesaTags(elementos,modelo.colortitulolista)
                        if tag == 'atli':
                            modelo.altotitulolista = ProcesaTags(elementos,modelo.altotitulolista)
                        if tag == 'mtli':
                            modelo.mayusculastitulolista = True
                        if tag == 'jvtl':
                            modelo.justificacionverticaltitulolista = ProcesaTags(elementos,modelo.justificacionverticaltitulolista)
                        if tag == 'jhtl':
                            modelo.justificacionhorizontaltitulolista = ProcesaTags(elementos,modelo.justificacionhorizontaltitulolista)
                        if tag == 'fcli':
                            modelo.fontcomentariolista = ProcesaTags(elementos,modelo.fontcomentariolista)
                        if tag == 'cli':
                            modelo.comentariolista = ProcesaTags(elementos,modelo.comentariolista)
                        if tag == 'cfcl':
                            modelo.colorfondocomentariolista = ProcesaTags(elementos,modelo.colorfondocomentariolista)
                        if tag == 'ccli':
                            modelo.colorcomentariolista = ProcesaTags(elementos,modelo.colorcomentariolista)
                        if tag == 'mco':
                            modelo.mayusculascolumnas = True
                        if tag == 'aco':
                            modelo.altocolumnas = ProcesaTags(elementos,modelo.altocolumnas)
                        if tag == 'cfcl':
                            modelo.colorfondocolumnaslista = ProcesaTags(elementos,modelo.colorfondocolumnaslista)
                        if tag == 'ccli':
                            modelo.colorcolumnaslista = ProcesaTags(elementos,modelo.colorcolumnaslista)
                        if tag == 'fcli':
                            modelo.fontcolumnaslista = ProcesaTags(elementos,modelo.fontcolumnaslista)
                        if tag == 'clcb':
                            modelo.columnaslistaconborde = True
                        if tag == 'ftxl':
                            modelo.fonttextolista = ProcesaTags(elementos,modelo.fonttextolista)
                        if tag == 'cftxl':
                            modelo.colorfondotextolista = ProcesaTags(elementos,modelo.colorfondotextolista)
                        if tag == 'ctxl':
                            modelo.colortextolista = ProcesaTags(elementos,modelo.colortextolista)
                        if tag == 'feb':
                            modelo.fonteditarborrar = ProcesaTags(elementos,modelo.fonteditarborrar)
                        if tag == 'ceb':
                            modelo.coloreditarborrar = ProcesaTags(elementos,modelo.coloreditarborrar)
                        if tag == 'teb':
                            modelo.textoeditarborrar = ProcesaTags(elementos,modelo.textoeditarborrar)
                        if tag == 'flnm':
                            modelo.fontlinknuevomodelo = ProcesaTags(elementos,modelo.fontlinknuevomodelo)
                        if tag == 'clnm':
                            modelo.colorlinknuevomodelo = ProcesaTags(elementos,modelo.colorlinknuevomodelo)
                        if tag == 'tlnm':
                            modelo.textolinknuevomodelo = ProcesaTags(elementos,modelo.textolinknuevomodelo)
                        if tag == 'lnm':
                            modelo.linknuevomodelo = True
                        if tag == 'tin':
                            modelo.tituloinserta = ProcesaTags(elementos,modelo.tituloinserta)
                        if tag == 'ftin':
                            modelo.fonttituloinserta = ProcesaTags(elementos,modelo.fonttituloinserta)
                        if tag == 'ctin':
                            modelo.colortituloinserta = ProcesaTags(elementos,modelo.colortituloinserta)
                        if tag == 'cfti':
                            modelo.colorfondotituloinserta = ProcesaTags(elementos,modelo.colorfondotituloinserta)
                        if tag == 'cffti':
                            modelo.colorfondofilatituloinserta = ProcesaTags(elementos,modelo.colorfondofilatituloinserta)
                        if tag == 'afti':
                            modelo.altofilatituloinserta = ProcesaTags(elementos,modelo.altofilatituloinserta)
                        if tag == 'jvti':
                            modelo.justificacionverticaltituloinserta = ProcesaTags(elementos,modelo.justificacionverticaltituloinserta)
                        if tag == 'jhti':
                            modelo.justificacionhorizontaltituloinserta = ProcesaTags(elementos,modelo.justificacionhorizontaltituloinserta)
                        if tag == 'cfci':
                            modelo.colorfondocomentarioinserta = ProcesaTags(elementos,modelo.colorfondocomentarioinserta)
                        if tag == 'ccin':
                            modelo.colorcomentarioinserta = ProcesaTags(elementos,modelo.colorcomentarioinserta)
                        if tag == 'fcin':
                            modelo.fontcomentarioinserta = ProcesaTags(elementos,modelo.fontcomentarioinserta)
                        if tag == 'cin':
                            modelo.comentarioinserta = ProcesaTags(elementos,modelo.comentarioinserta)
                        if tag == 'ncii':
                            modelo.numerocolumnasizquierdainserta = ProcesaTags(elementos,modelo.numerocolumnasizquierdainserta)
                        if tag == 'ncmi':
                            modelo.numerocolumnasmodeloinserta = ProcesaTags(elementos,modelo.numerocolumnasmodeloinserta)
                        if tag == 'ncdi':
                            modelo.numerocolumnasderechainserta = ProcesaTags(elementos,modelo.numerocolumnasderechainserta)
                        if tag == 'tup':
                            modelo.tituloupdate = ProcesaTags(elementos,modelo.tituloupdate)
                        if tag == 'ftup':
                            modelo.fonttituloupdate = ProcesaTags(elementos,modelo.fonttituloupdate)
                        if tag == 'ctup':
                            modelo.colortituloupdate = ProcesaTags(elementos,modelo.colortituloupdate)
                        if tag == 'cftu':
                            modelo.colorfondotituloupdate = ProcesaTags(elementos,modelo.colorfondotituloupdate)
                        if tag == 'cfftu':
                            modelo.colorfondofilatituloupdate = ProcesaTags(elementos,modelo.colorfondofilatituloupdate)
                        if tag == 'aftu':
                            modelo.altofilatituloupdate = ProcesaTags(elementos,modelo.altofilatituloupdate)
                        if tag == 'jvtu':
                            modelo.justificacionverticaltituloupdate = ProcesaTags(elementos,modelo.justificacionverticaltituloupdate)
                        if tag == 'jhtu':
                            modelo.justificacionhorizontaltituloupdate = ProcesaTags(elementos,modelo.justificacionhorizontaltituloupdate)
                        if tag == 'cup':
                            modelo.comentarioupdate = ProcesaTags(elementos,modelo.comentarioupdate)
                        if tag == 'cfcu':
                            modelo.colorfondocomentarioupdate = ProcesaTags(elementos,modelo.colorfondocomentarioupdate)
                        if tag == 'fcup':
                            modelo.fontcomentarioupdate = ProcesaTags(elementos,modelo.fontcomentarioupdate)
                        if tag == 'ccup':
                            modelo.colorcomentarioupdate = ProcesaTags(elementos,modelo.colorcomentarioupdate)
                        if tag == 'nciu':
                            modelo.numerocolumnasizquierdaupdate = ProcesaTags(elementos,modelo.numerocolumnasizquierdaupdate)
                        if tag == 'ncdu':
                            modelo.numerocolumnasderechaupdate = ProcesaTags(elementos,modelo.numerocolumnasderechaupdate)
                        if tag == 'ncmu':
                            modelo.numerocolumnasmodeloupdate = ProcesaTags(elementos,modelo.numerocolumnasmodeloupdate)
                        if tag == 'flm':
                            modelo.fontlabelmodelo = ProcesaTags(elementos,modelo.fontlabelmodelo)
                        if tag == 'clm':
                            modelo.colorlabelmodelo = ProcesaTags(elementos,modelo.colorlabelmodelo)
                        if tag == 'cau':
                            modelo.controlesautomaticos = True
                        if tag == 'tbo':
                            modelo.tituloborra = ProcesaTags(elementos,modelo.tituloborra)
                        if tag == 'ftbo':
                            modelo.fonttituloborra = ProcesaTags(elementos,modelo.fonttituloborra)
                        if tag == 'ctbo':
                            modelo.colortituloborra = ProcesaTags(elementos,modelo.colortituloborra)
                        if tag == 'cftb':
                            modelo.colorfondotituloborra = ProcesaTags(elementos,modelo.colorfondotituloborra)
                        if tag == 'cfftb':
                            modelo.colorfondofilatituloborra = ProcesaTags(elementos,modelo.colorfondofilatituloborra)
                        if tag == 'aftb':
                            modelo.altofilatituloborra = ProcesaTags(elementos,modelo.altofilatituloborra)
                        if tag == 'jvtb':
                            modelo.justificacionverticaltituloborra = ProcesaTags(elementos,modelo.justificacionverticaltituloborra)
                        if tag == 'jhtb':
                            modelo.justificacionhorizontaltituloborra = ProcesaTags(elementos,modelo.justificacionhorizontaltituloborra)
                        if tag == 'cfcb':
                            modelo.colorfondocomentarioborra = ProcesaTags(elementos,modelo.colorfondocomentarioborra)
                        if tag == 'ccbo':
                            modelo.colorcomentarioborra = ProcesaTags(elementos,modelo.colorcomentarioborra)
                        if tag == 'fcbo':
                            modelo.fontcomentarioborra = ProcesaTags(elementos,modelo.fontcomentarioborra)
                        if tag == 'cbo':
                            modelo.comentarioborra = ProcesaTags(elementos,modelo.comentarioborra)
                        if tag == 'cftxb':
                            modelo.colorfondotextoborra = ProcesaTags(elementos,modelo.colorfondotextoborra)
                        if tag == 'ctxb':
                            modelo.colortextoborra = ProcesaTags(elementos,modelo.colortextoborra)
                        if tag == 'ftxb':
                            modelo.fonttextoborra = ProcesaTags(elementos,modelo.fonttextoborra)
                        if tag == 'txbo':
                            modelo.textoborra = ProcesaTags(elementos,modelo.textoborra)
                        if tag == 'txbb':
                            modelo.textobotonborra = ProcesaTags(elementos,modelo.textobotonborra)
                        if tag == 'ncib':
                            modelo.numerocolumnasizquierdaborra = ProcesaTags(elementos,modelo.numerocolumnasizquierdaborra)
                        if tag == 'ncdb':
                            modelo.numerocolumnasderechaborra = ProcesaTags(elementos,modelo.numerocolumnasderechaborra)
                        if tag == 'ncmb':
                            modelo.numerocolumnasmodeloborra = ProcesaTags(elementos,modelo.numerocolumnasmodeloborra)
                        if tag == 'hco':
                            modelo.hijoscontiguos = True
                        if tag == 'ncho':
                            modelo.numerocolumnashijosupdate = ProcesaTags(elementos,modelo.numerocolumnashijosupdate)
                        if tag == 'ls':
                            modelo.listastaff = True
                        if tag == 'll':
                            modelo.listalogin = True
                        if tag == 'cl':
                            modelo.crearlogin = True
                        if tag == 'cs':
                            modelo.crearstaff = True
                        if tag == 'es':
                            modelo.editarstaff = True
                        if tag == 'el':
                            modelo.editarlogin = True
                        if tag == 'bs':
                            modelo.borrarstaff = True
                        if tag == 'bl':
                            modelo.borrarlogin = True
                        if tag == 'nclb':
                            modelo.numerocolumnaslabels = ProcesaTags(elementos,modelo.numerocolumnaslabels)
                        if tag == 'ncct':
                            modelo.numerocolumnascontroles = ProcesaTags(elementos,modelo.numerocolumnascontroles)
                        if tag == 'msb':
                            modelo.sinbasedatos = True
                        modelo.save()
                    # Propiedades
                    if tag == 'npro':
                        propiedad = Propiedad()
                        propiedad.modelo = modelo
                        propiedad.nombre = ProcesaTags(elementos,'propiedad' + str(npr))
                        npr += 1
                    if propiedad != None:
                        tag = tag.replace('&nbsp','')
                        if tag == 'dpro':
                            propiedad.descripcion = ProcesaTags(elementos,propiedad.descripcion)
                        if tag == 'tpro':
                            propiedad.tipo = ProcesaTags(elementos,propiedad.tipo)
                        if tag == 'prf':
                            propiedad.foranea = ProcesaTags(elementos,propiedad.foranea)
                        if tag == 'txb':
                            propiedad.textobotones = ProcesaTags(elementos,propiedad.textobotones)
                        if tag == 'vdf':
                            propiedad.valorinicial = ProcesaTags(elementos,propiedad.valorinicial)
                        if tag == 'lst':
                            propiedad.largostring = ProcesaTags(elementos,propiedad.largostring)
                        if tag == 'tph':
                            propiedad.textoplaceholder = ProcesaTags(elementos,propiedad.textoplaceholder)
                        if tag == 'epro':
                            propiedad.etiqueta = ProcesaTags(elementos,propiedad.etiqueta)
                        if tag == 'enl':
                            propiedad.enlista = True
                        if tag == 'emb':
                            propiedad.enmobile = True
                        if tag == 'ncl':
                            propiedad.numerocolumnas = ProcesaTags(elementos,propiedad.numerocolumnas)
                        if tag == 'txc':
                            propiedad.textocolumna = ProcesaTags(elementos,propiedad.textocolumna)
                        if tag == 'jtxc':
                            propiedad.justificaciontextocolumna = ProcesaTags(elementos,propiedad.justificaciontextocolumna)
                        if tag == 'ffch':
                            propiedad.formatofecha = ProcesaTags(elementos,propiedad.formatofecha)
                        if tag == 'ear':
                            propiedad.etiquetaarriba = True
                        propiedad.save()
                    # Reglas
                    if tag == 'msj':
                        regla = Regla()
                        regla.propiedad = propiedad
                        regla.mensaje = ProcesaTags(elementos,'regla' + str(nrg))
                        nrg += 1
                    if regla != None:
                        if tag == 'crg':
                            elementos = elementos.replace('~','[')
                            elementos = elementos.replace('@',']')
                            regla.codigo = ProcesaTags(elementos,regla.codigo)
                        regla.save()
            context['error_texto'] = ''
            context['proyecto'] =  proyecto
            texto_procesar.proyecto = proyecto.id
            texto_procesar.save()
            context['mensaje'] =  Texto
            # proyecto.save()
        except Exception as e:
            context['error_texto'] = 'Existe error en la construccion del Texto: ' + str(e)
        return context

def ProcesaTags(elementos,campo):
    try:
        return elementos.replace('&nbsp',' ')
    except:
        return campo.replace('&nbsp',' ')

class EsquemaView(TemplateView):
    template_name = 'esquema.html'

    def get_context_data(self,**kwargs):
        context = super(EsquemaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['error'] = ''
        return context

class DuplicaView(FormView):
    template_name = 'esquema.html'

    def get_context_data(self,**kwargs):
        context = super(DuplicaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        context['error'] = ''
        return context        