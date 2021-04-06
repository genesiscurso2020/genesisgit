from .models import Modelo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django import forms
# from core.views import VerificaVigenciaUsuario
from .models import Propiedad
from proyectos.models import Proyecto
from .forms import PropiedadForm
from django.http import HttpResponseRedirect
from proyectos.views import VerificaVigenciaUsuario

class CrearPropiedadView(CreateView):
    model = Propiedad
    form_class = PropiedadForm

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearPropiedadView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
            context['modelo'] = modelo
            proyecto = Proyecto.objects.get(id=modelo.proyecto.id,usuario=self.request.user)
            context['proyecto'] = proyecto
            context['error'] = ''
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        modelo = Modelo.objects.get(id = request.GET['modelo_id'])
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.modelo = modelo
            propiedad.save()
            return HttpResponseRedirect(self.get_success_url())
        return render(request, 'propiedades/propiedad_form.html', {'form': form})

    def get_form(self,form_class=None):
        form = super(CrearPropiedadView, self).get_form()
        #Modificar en tiempo real
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
        FORANEA_LIST = []
        FORANEA_LIST.append(['nada','nada'])
        for ml in Modelo.objects.filter(proyecto=proyecto):
           FORANEA_LIST.append([ml.nombre, ml.nombre])
        form.fields['foranea'].widget = forms.Select(attrs={'class':'form-control'}, choices=FORANEA_LIST)
        return form

class EditarPropiedadView(UpdateView):
    model = Propiedad
    form_class = PropiedadForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        # propiedad = self.object
        # modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
        # aplicacion = Aplicacion.objects.get(id=modelo.aplicacion.id)
        # propiedad.foranea = propiedad.foranea.lower()
        # propiedad.save()
        return reverse_lazy('propiedades:editar', args=[self.object.id]) + '?ok&proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(EditarPropiedadView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            obj = self.object
            context['propiedad'] = obj
            context['modelo'] = Modelo.objects.get(id=obj.modelo.id)
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['proyecto'] = proyecto
            context['error'] = ''
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def get_form(self,form_class=None):
        form = super(EditarPropiedadView, self).get_form()
        #Modificar en tiempo real
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
        FORANEA_LIST = []
        FORANEA_LIST.append(['nada','nada'])
        for ml in Modelo.objects.filter(proyecto=proyecto):
           FORANEA_LIST.append([ml.nombre, ml.nombre])
        form.fields['foranea'].widget = forms.Select(attrs={'class':'form-control'}, choices=FORANEA_LIST)
        return form

class BorrarPropiedadView(DeleteView):
    model = Propiedad

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?ok&proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(BorrarPropiedadView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            obj = self.object
            print('proyecto borrar', obj)
            modelo = Modelo.objects.get(id=obj.modelo.id)
            proyecto = Proyecto.objects.get(id=modelo.proyecto.id,usuario=self.request.user)
            context['nombre'] = obj.nombre
            context['proyecto'] = proyecto
            context['error'] = ''
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

