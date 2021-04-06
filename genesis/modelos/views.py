# from django.views.generic.list import ListView
# from aplicaciones.models import Aplicacion
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from modelos.models import Modelo
from proyectos.models import Proyecto
from .forms import ModeloForm
from django import forms
from django.http import HttpResponseRedirect
from proyectos.views import VerificaVigenciaUsuario

class CrearModeloView(CreateView):
    model = Modelo
    form_class = ModeloForm

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearModeloView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            proyecto = Proyecto.objects.get(id = self.request.GET['proyecto_id'],usuario=self.request.user)
            print('1')
            context['proyecto'] = proyecto
            context['modelo'] = None
            context['mensaje_error'] = self.request.GET['mensaje_error']
            print('2')
            if self.request.GET['modelo_id'] != '0':
                print('4')
                context['modelo'] = Modelo.objects.get(id=self.request.GET['modelo_id'])
            print('3')
            context['error'] = ''
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def get_form(self,form_class=None):
        form = super(CrearModeloView, self).get_form()
        #Modificar en tiempo real
        # aplicacion = Aplicacion.objects.get(id = self.request.GET['aplicacion_id'])
        proyecto = Proyecto.objects.get(id = self.request.GET['proyecto_id'],usuario=self.request.user)
        PADRES_LIST = []
        PADRES_LIST.append(['nada','nada'])
        for ml in Modelo.objects.filter(proyecto=proyecto):
           PADRES_LIST.append([ml.nombre, ml.nombre])
        form.fields['padre'].widget = forms.Select(attrs={'class':'form-control font_control'},choices=PADRES_LIST)
        return form

    def get_form_kwargs(self):
        proyecto= self.request.GET['proyecto_id']
        kwargs = super(CrearModeloView, self).get_form_kwargs()
        kwargs.update({'proyect': proyecto})
        return kwargs
        
    def post(self,request,*args,**kwargs):
        print('a')
        form = self.form_class(request.POST, request.FILES)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])
        mensaje_error = ''
        if form.is_valid():
            print('b')
            modelo = form.save(commit=False)
            modelo.proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])
            # Colocamos el valor del padre
            modelo.padre = 'nada'
            if self.request.GET['modelo_id'] != '0':
                modelo.padre = Modelo.objects.get(id=self.request.GET['modelo_id']).nombre
            print('c')
            # Validar que el modelo sea unico

            if Modelo.objects.filter(nombre=modelo.nombre,proyecto=modelo.proyecto).count() == 0:
                print('d')
                modelo.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                mensaje_error = 'El Modelo ' + modelo.nombre + ' ya existe en el proyecto, intente con otro nombre'
                return HttpResponseRedirect('/modelos/crear' + '/?proyecto_id=' + str(proyecto.id) + '&modelo_id=' + str(modelo.id) + '&mensaje_error=' + mensaje_error) 
        # return render(request, 'modelos/modelo_form.html', {'form': form,'mensaje_error':mensaje_error})
        return HttpResponseRedirect('/modelos/crear' + '/?proyecto_id=' + str(proyecto.id)) 

class EditarModeloView(UpdateView):
    model = Modelo
    form_class = ModeloForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
        return reverse_lazy('modelos:editar', args=[modelo.id]) + '?ok&proyecto_id=' + self.request.GET['proyecto_id'] + '&modelo_id=' + self.request.GET['modelo_id']

    def get_context_data(self,**kwargs):
        context = super(EditarModeloView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['proyecto'] = proyecto
            context['modelo'] = Modelo.objects.get(id=self.object.id)
            # context['mensaje_error'] = self.request.GET['mensaje_error']
            context['error'] = ''
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except Exception as e:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context
    
    def get_form(self,form_class=None):
        form = super(EditarModeloView, self).get_form()
        #Modificar en tiempo real
        # aplicacion = Aplicacion.objects.get(id = self.request.GET['aplicacion_id'])
        proyecto = Proyecto.objects.get(id = self.request.GET['proyecto_id'],usuario=self.request.user)
        PADRES_LIST = []
        PADRES_LIST.append(['nada','nada'])
        for ml in Modelo.objects.filter(proyecto=proyecto):
           PADRES_LIST.append([ml.nombre, ml.nombre])
        form.fields['padre'].widget = forms.Select(attrs={'class':'form-control font_control'},choices=PADRES_LIST)
        return form

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        modelo = form.save(commit=False)
        mensaje_error=''
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
        # Validar que el modelo sea unico
        nombre_antiguo = Modelo.objects.get(id=self.request.GET['modelo_id'], proyecto=proyecto).nombre
        if nombre_antiguo != modelo.nombre:
            if Modelo.objects.filter(nombre=modelo.nombre,proyecto=proyecto).count() == 0:
                modelo.save()
                ActualizaModeloPadre(nombre_antiguo, modelo.nombre, proyecto)
                return HttpResponseRedirect(self.get_success_url())
            else:
                mensaje_error = 'El Modelo ' + modelo.nombre + ' ya existe en el proyecto, intente con otro nombre'
                return HttpResponseRedirect('/modelos/editar/' + str(modelo.id) + '/?proyecto_id=' + str(proyecto.id) + '&modelo_id=' + str(modelo.id) + '&mensaje_error=' + mensaje_error) 
        else:
            modelo.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        proyecto= self.request.GET['proyecto_id']
        kwargs = super(EditarModeloView, self).get_form_kwargs()
        kwargs.update({'proyect': proyecto})
        # print('kwargs ',kwargs)
        return kwargs
        # return render(request, 'modelos/modelo_update_form.html', {'form': form,'mensaje_error':mensaje_error})

def ActualizaModeloPadre(nombrePadreAnterior, nuevoNombrePadre,proyecto):
    for modelo in Modelo.objects.filter(proyecto=proyecto, padre=nombrePadreAnterior):
        modelo.padre = nuevoNombrePadre
        modelo.save()

class BorrarModeloView(DeleteView):
    model = Modelo

    def get_success_url(self):
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
        strTexto = []
        BorraRecursiva(strTexto,self.request.GET['nombre'],proyecto)
        for mid in strTexto:
            Modelo.objects.get(id=mid).delete()
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(BorrarModeloView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            obj = Modelo.objects.get(id=self.object.id)
            context['modelo'] = obj
            context['proyecto'] = Proyecto.objects.get(id=obj.proyecto.id)
            context['nombre'] = obj.nombre
            context['error'] = ''
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

def BorraRecursiva(strTexto,nombre,proyecto):
    for li in Modelo.objects.filter(padre=nombre,proyecto=proyecto):
        strTexto.append(li.id)
        BorraRecursiva(strTexto,li.nombre,proyecto)


