from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
# from core.views import VerificaVigenciaUsuario
from modelos.models import Modelo
from .models import Regla
from propiedades.models import Propiedad
from proyectos.models import Proyecto
from .forms import ReglaForm
from django.http import HttpResponseRedirect
from registration.views import VerificaVigenciaUsuario

class CrearReglaView(CreateView):
    model = Regla
    form_class = ReglaForm

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearReglaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            propiedad = Propiedad.objects.get(id=self.request.GET['propiedad_id'])
            context['propiedad'] = propiedad
            modelo = Modelo.objects.get(id=propiedad.modelo.id)
            proyecto = Proyecto.objects.get(id=modelo.proyecto.id,usuario=self.request.user)
            context['modelo'] = modelo
            context['proyecto'] = proyecto
            context['error'] = ''
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        propiedad = Propiedad.objects.get(id = request.GET['propiedad_id'])
        if form.is_valid():
            regla = form.save(commit=False)
            regla.propiedad = propiedad
            regla.save()
            return HttpResponseRedirect(self.get_success_url())
        return render(request, 'reglas/regla_form.html', {'form': form})

class EditarReglaView(UpdateView):
    model = Regla
    form_class = ReglaForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        # propiedad = self.object
        # modelo = Modelo.objects.get(id=self.request.GET['modelo_id'])
        # aplicacion = Aplicacion.objects.get(id=modelo.aplicacion.id)
        # propiedad.foranea = propiedad.foranea.lower()
        # propiedad.save()
        return reverse_lazy('reglas:editar', args=[self.object.id]) + '?ok&proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(EditarReglaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            obj = self.object
            context['regla'] = obj
            propiedad = Propiedad.objects.get(id=obj.propiedad.id)
            context['propiedad'] = propiedad
            modelo = Modelo.objects.get(id=propiedad.modelo.id)
            context['modelo'] = modelo
            proyecto = Proyecto.objects.get(id=modelo.proyecto.id,usuario=self.request.user)
            context['proyecto'] = proyecto
            context['regla'] = obj
            context['error'] = ''
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

class BorrarReglaView(DeleteView):
    model = Regla

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?ok&proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(BorrarReglaView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            obj = self.object
            propiedad = Propiedad.objects.get(id=obj.propiedad.id)
            print('propiedad ',propiedad)
            modelo = Modelo.objects.get(id=propiedad.modelo.id)
            proyecto = Proyecto.objects.get(id=modelo.proyecto.id,usuario=self.request.user)
            print('proyecto ',proyecto)
            context['nombre'] = obj.mensaje
            context['proyecto'] = proyecto
            context['error'] = ''
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

