from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
# from core.models import Genesis
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from aplicaciones.models import Aplicacion
from modelos.models import Modelo
from personalizacion.models import Personaliza
from .forms import PersonalizaForm
from proyectos.models import Proyecto
from crear import views
from core.models import Genesis
from django.urls import reverse_lazy
from proyectos.views import VerificaVigenciaUsuario

import os
# Create your views here.
# @method_decorator(staff_member_required,name='dispatch')
class ListarPersonalizaView(ListView):
    model = Personaliza
    template_name = "personalizacion/personaliza_lista.html"

    def get_context_data(self, **kwargs):
        context = super(ListarPersonalizaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['proyecto'] = proyecto
            listapersonaliza = Personaliza.objects.filter(proyecto=proyecto)
            context['lista'] = listapersonaliza
            gen =Genesis.objects.get(nombre='GENESIS')
            if self.request.GET['ingreso'] == '1':
                ActualizaPersonalizacion(proyecto,gen.directorio,proyecto.nombre,'personalizacion')
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'        
        return context

class EditarPersonalizaView(UpdateView):
    model = Personaliza
    form_class = PersonalizaForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('personalizacion:editar', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarPersonalizaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            personaliza =  Personaliza.objects.get(id=self.object.id)
            context['proyecto'] = Proyecto.objects.get(id=personaliza.proyecto.id,usuario=self.request.user)
            context['personaliza'] = personaliza
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class CrearPersonalizaView(CreateView):
    model = Personaliza
    form_class = PersonalizaForm

    def get_success_url(self):
        return reverse_lazy('personalizacion:home')+ '?aplicacion_id=' + self.request.GET['aplicacion_id' + '&ingreso=0']
        # return reverse_lazy('proyectos:editar', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(CrearPersonalizaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            aplicacion=Aplicacion.objects.get(id=str(self.request.GET['aplicacion_id']))
            context['proyecto'] = Proyecto.objects.get(id=aplicacion.proyecto.id,usuario=self.request.user)
            context['aplicacion'] = aplicacion
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        user = request.user
        aplicacion=Aplicacion.objects.get(id=str(self.request.GET['aplicacion_id']))
        proyecto = proyecto=Proyecto.objects.get(id=aplicacion.proyecto.id)
        # print(user)
        if form.is_valid():
            personaliza = form.save(commit=False)
            personaliza.usuario = user
            personaliza.aplicacion = aplicacion
            personaliza.proyecto = proyecto
            personaliza.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarPersonalizaView(DeleteView):
    model = Personaliza
    # success_url = reverse_lazy('personalizacion:home') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_success_url(self):
        return reverse_lazy('personalizacion:home') + '?proyecto_id=' + self.request.GET['proyecto_id'] + '&ingreso=0'

    def get_context_data(self,**kwargs):
        context = super(BorrarPersonalizaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            obj = Personaliza.objects.get(id=self.object.id)
            context['nombre'] = obj.tag
            context['proyecto'] = Proyecto.objects.get(id=obj.proyecto.id)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

def ActualizaPersonalizacion(proyecto,directorio,nombre,etapa):
    
    # genesis = Genesis.objects.get(nombre='GENESIS')
    # dg = genesis.directorio    

    # Personaliza el proyecto
    # settings.py, urls.py
    LeerPersonalizacion(directorio + nombre + '/' + nombre + '/',proyecto,nombre,'settings.py',proyecto.usuario.username, '',etapa,nombre)
    LeerPersonalizacion(directorio + nombre + '/' + nombre + '/',proyecto,nombre,'urls.py',proyecto.usuario.username, '',etapa,nombre)
 
    la = Aplicacion.objects.filter(proyecto=proyecto)
    for app in la:
        # archivos html
        if app.nombre != 'core' and app.nombre != 'registration':
            cd = directorio + nombre + '/' + app.nombre + '/templates/' + app.nombre + '/' 
            LeerPersonalizacion(cd,proyecto,app.nombre,'home.html',proyecto.usuario.username, app.nombre,etapa,nombre)
            # html para modelos
            lm = Modelo.objects.filter(aplicacion=app)
            for modelo in lm:
                if modelo.sinbasedatos == False:
                    if modelo.padre == 'nada':
                        cd = directorio + nombre + '/' + app.nombre + '/templates/' + app.nombre + '/' 
                        LeerPersonalizacion(cd,proyecto,app.nombre,modelo.nombre + '_list.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                        cd = directorio + nombre + '/core/templates/core/includes/' 
                        LeerPersonalizacion(cd,proyecto,app.nombre,'menu_' + modelo.aplicacion.nombre + '.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                    cd = directorio + nombre + '/' + app.nombre + '/templates/' + app.nombre + '/'
                    LeerPersonalizacion(cd,proyecto,app.nombre,modelo.nombre + '_form.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                    LeerPersonalizacion(cd,proyecto,app.nombre,modelo.nombre + '_update_form.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                    LeerPersonalizacion(cd,proyecto,app.nombre,modelo.nombre + '_confirm_delete.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                else:
                    LeerPersonalizacion(cd,proyecto,app.nombre,modelo.nombre + '_sinbase.html',proyecto.usuario.username, app.nombre,etapa,nombre)

        elif app.nombre == 'core':
            cd = directorio + nombre + '/' + app.nombre + '/templates/' + app.nombre + '/includes/' 
            LeerPersonalizacion(cd,proyecto,app.nombre,'menu_core.html',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'css_general.html',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'js_general.html',proyecto.usuario.username, app.nombre,etapa,nombre)
            cd = directorio + nombre + '/' + app.nombre + '/templates/' + app.nombre + '/'
            LeerPersonalizacion(cd,proyecto,app.nombre,'base.html',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'home.html',proyecto.usuario.username, app.nombre,etapa,nombre)
            cd = directorio + nombre + '/' + app.nombre + '/static/' + app.nombre + '/css/'  
            LeerPersonalizacion(cd,proyecto,app.nombre,'estilos.css',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'modelo_borra.css',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'modelo_hijo.css',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'modelo_inserta.css',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'modelo_list.css',proyecto.usuario.username, app.nombre,etapa,nombre)
            LeerPersonalizacion(cd,proyecto,app.nombre,'modelo_update.css',proyecto.usuario.username, app.nombre,etapa,nombre)
        elif app.nombre == 'registration':
            if proyecto.conseguridad:
                cd = directorio + nombre + '/registration/templates/registration/' 
                LeerPersonalizacion(cd,proyecto ,app.nombre,'login.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'password_change_form.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'password_change_done.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'password_reset_complete.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'password_reset_confirm.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'password_reset_done.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'password_reset_form.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'profile_email_form.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'profile_form.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'registro.html',proyecto.usuario.username, app.nombre,etapa,nombre)
                cd = directorio + nombre + '/registration/' 
                LeerPersonalizacion(cd,proyecto ,app.nombre,'forms.py',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'models.py',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'urls.py',proyecto.usuario.username, app.nombre,etapa,nombre)
                LeerPersonalizacion(cd,proyecto ,app.nombre,'views.py',proyecto.usuario.username, app.nombre,etapa,nombre)


        cd = directorio + nombre + '/' + app.nombre + '/'
        # admin
        LeerPersonalizacion(cd,proyecto,app.nombre,'admin.py',proyecto.usuario.username, app.nombre,etapa,nombre)
        # modelos
        LeerPersonalizacion(cd,proyecto,app.nombre,'models.py',proyecto.usuario.username, app.nombre,etapa,nombre)
        # vistas
        LeerPersonalizacion(cd,proyecto,app.nombre,'views.py',proyecto.usuario.username, app.nombre,etapa,nombre)
        # urls
        LeerPersonalizacion(cd,proyecto,app.nombre,'urls.py',proyecto.usuario.username, app.nombre,etapa,nombre)
        # forms
        LeerPersonalizacion(cd,proyecto,app.nombre,'forms.py',proyecto.usuario.username, app.nombre,etapa,nombre)

# lee el archivo y busca tags de personalizacion
# los graba en la tabla y repone el tag original
def LeerPersonalizacion(cd,proyecto,nombre_aplicacion,archivo, username,proname,etapa,nombre):
    # leer el archivo
    stri = views.LeerArchivoEnTexto(cd + archivo,etapa,nombre,username )
    # separa en lineas
    flgEsPersonalizacion = False
    strLineaNueva = ''
    strCodigo = ''
    strls = stri.split('\n')
    # if archivo == 'home.html' and aplicacion.nombre == 'domicilios':
    #     print('stri ',strls)

    try:
        for strl in strls:
            if '#@(' in strl:
                if not flgEsPersonalizacion:
                    flgEsPersonalizacion = True
                    # existe un tag de personalizacion
                    # busca el tag
                    strTag = ''

                    if '<!--' in strl:
                        for ch in strl:
                            if ch!= '<' and ch != '@' and ch != '#' and ch != '-' and ch != '(' and ch != ')' and ch != ' ' and ch != '>' and ch != '!':
                                strTag += ch
                    elif '/*' in strl:
                        for ch in strl:
                            if ch!= '*' and ch != '@' and ch != '#' and ch != '-' and ch != '(' and ch != ')' and ch != ' ' and ch != '/' and ch != '!':
                                strTag += ch
                    else:
                        for ch in strl:
                            if ch != '#' and ch!= '@' and ch != '(' and ch != ')' and ch != ' ':
                                strTag += ch
                    # reemplaza la linea por la linea de personalizacion sin codigo

                    strLineaNueva += strl + '\n'
                    # if '<!--' in strl:
                    #     strLineaNueva += '<!-- ' + '#@[' + strTag + ']' + ' -->' + '\n'
                    # elif '/*' in strl:
                    #     strLineaNueva += '/*' + '#@[' + strTag + ']' + '*/' + '\n'
                    # else:
                    #     strLineaNueva += '#@[' + strTag + ']\n'

                     # busca el tag en personalizacion
                else:
                    if '#@()' in strl:
                        # se llega al final del codigo de personalizacion
                        tag = Personaliza.objects.filter(usuario = proyecto.usuario,
                                                             proyecto=proyecto,
                                                             aplicacion=nombre_aplicacion,
                                                             archivo=archivo,
                                                             tag=strTag)
                        if tag.count() > 0:
                            tag = Personaliza.objects.get(usuario=proyecto.usuario,
                                                              proyecto=proyecto,
                                                              aplicacion=nombre_aplicacion,
                                                              archivo=archivo,
                                                              tag=strTag)
                            if strCodigo == '':
                                tag.delete()
                            else:
                                strLineaNueva += strl + '\n'
                                tag.codigo = strCodigo
                                tag.save()
                                print('tag_nuevo ',strTag)
                        else:
                            # crea el nuevo tag
                            if strCodigo != '':
                                tag = Personaliza(usuario=proyecto.usuario,
                                                      proyecto=proyecto,
                                                      aplicacion=nombre_aplicacion,
                                                      archivo=archivo,
                                                      tag=strTag,
                                                      codigo=strCodigo)
                                tag.save()
                                strLineaNueva += strl + '\n'
                        strCodigo=''    
                        flgEsPersonalizacion = False
            else:
                if flgEsPersonalizacion:
                    if strl != '':
                        strCodigo += strl + '\n'
                strLineaNueva += strl + '\n'    
        views.EscribirEnArchivo(cd + archivo,strLineaNueva,etapa,nombre,username)

    except Exception as e:
        print('error ' ,e)
        
    return stri

# def LeerPersonalizacion(cd,proyecto,nombre_aplicacion,archivo, username,proname,etapa,nombre):
#     # leer el archivo
#     stri = views.LeerArchivoEnTexto(cd + archivo,etapa,nombre,username )
#     # separa en lineas
#     flgEsPersonalizacion = False
#     strLineaNueva = ''
#     strCodigo = ''
#     strls = stri.split('\n')
#     # if archivo == 'home.html' and aplicacion.nombre == 'domicilios':
#     #     print('stri ',strls)

#     try:
#         for strl in strls:
#             # if archivo == 'views.py' and aplicacion.nombre == 'domicilios':
#             #     print(strl)
#             if '#@(' in strl:
#                 if archivo == 'turnoarriba_sinbase.html':
#                     print('1',strLineaNueva,flgEsPersonalizacion)
#                 if not flgEsPersonalizacion:
#                     flgEsPersonalizacion = True
#                     # existe un tag de personalizacion
#                     # busca el tag
#                     strTag = ''

#                     # ve si el archivo html
#                     if '<!--' in strl:
#                         for ch in strl:
#                             if ch!= '<' and ch != '@' and ch != '#' and ch != '-' and ch != '(' and ch != ')' and ch != ' ' and ch != '>' and ch != '!':
#                                 strTag += ch
#                     elif '/*' in strl:
#                         for ch in strl:
#                             if ch!= '*' and ch != '@' and ch != '#' and ch != '-' and ch != '(' and ch != ')' and ch != ' ' and ch != '/' and ch != '!':
#                                 strTag += ch
#                     else:
#                         for ch in strl:
#                             if ch != '#' and ch!= '@' and ch != '(' and ch != ')' and ch != ' ':
#                                 strTag += ch



#                     # if archivo == 'views.py' and aplicacion.nombre == 'domicilios':
#                     #     print('strtag ',strTag)

#                     # reemplaza la linea por la linea de personalizacion sin codigo
#                     if '<!--' in strl:
#                         strLineaNueva += '<!-- ' + '#@[' + strTag + ']' + ' -->' + '\n'
#                     elif '/*' in strl:
#                         strLineaNueva += '/*' + '#@[' + strTag + ']' + '*/' + '\n'
#                     else:
#                         strLineaNueva += '#@[' + strTag + ']\n'

#                     # if archivo == 'turnoarriba_sinbase.html':
#                     #     print('2',strLineaNueva)

#                     # busca el tag en personalizacion
#                 else:
#                     # se llega al final del codigo de personalizacion
#                     tag = Personaliza.objects.filter(usuario = proyecto.usuario,
#                                                          proyecto=proyecto,
#                                                          aplicacion=nombre_aplicacion,
#                                                          archivo=archivo,
#                                                          tag=strTag)
#                     if tag.count() > 0:
#                         tag = Personaliza.objects.get(usuario=proyecto.usuario,
#                                                           proyecto=proyecto,
#                                                           aplicacion=nombre_aplicacion,
#                                                           archivo=archivo,
#                                                           tag=strTag)
#                         tag.codigo = strCodigo
#                         tag.save()
#                         # if archivo == 'views.py' and aplicacion.nombre == 'domicilios':
#                         #     print('tag viejo ',tag)
#                         #     print('codigo viejo nuevo :')
#                         #     print(strCodigo)
#                     else:
#                         # crea el nuevo tag
#                         tag = Personaliza(usuario=proyecto.usuario,
#                                               proyecto=proyecto,
#                                               aplicacion=nombre_aplicacion,
#                                               archivo=archivo,
#                                               tag=strTag,
#                                               codigo=strCodigo)
#                         tag.save()
#                         # if archivo == 'views.py' and aplicacion.nombre == 'domicilios':
#                         #     print('tag nuevo ',tag)
#                         #     print('codigo nuevo:')
#                         #     print(strCodigo)
#                     strCodigo=''    
#                     flgEsPersonalizacion = False
#             else:
#                 if flgEsPersonalizacion:
#                     if strl != '':
#                         strCodigo += strl + '\n'
#                 else:    
#                     strLineaNueva += strl + '\n'    
#                     # if archivo == 'turnoarriba_sinbase.html':
#                     #     print(strLineaNueva)
      

#         views.EscribirEnArchivo(cd + archivo,strLineaNueva,etapa,nombre,username)

#     except Exception as e:
#         print('error ' ,e)
        
#     return stri

