from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.views import VerificaVigenciaUsuario
from aplicaciones.models import Aplicacion
from proyectos.models import Proyecto
from .forms import AplicacionForm
from registration.views import VerificaVigenciaUsuario, PropietarioProyecto

class AplicacionListaView(ListView):
    model = Aplicacion

class EditarAplicacionView(UpdateView):
    model = Aplicacion
    form_class = AplicacionForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('aplicaciones:editar', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarAplicacionView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.object.proyecto.id,usuario=self.request.user)
            # modelos = Modelo.objects.filter(aplicacion = self.object)
            context['proyecto'] = proyecto
            context['nombre'] = self.object.nombre
            # context['listamodelo'] =  modelos
            context['proyecto_id'] = self.object.proyecto.id
            context['aplicacion'] = self.object
            # context['mensaje_error'] = self.request.GET['mensaje_error']
            # context['numero'] = Modelo.objects.filter(aplicacion=self.object).count()
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        aplicacion = form.save(commit=False)
        mensaje_error=''
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
        # Validar que el modelo sea unico
        nombre_antiguo = Aplicacion.objects.get(id=self.request.GET['aplicacion_id'], proyecto=proyecto).nombre
        if nombre_antiguo != aplicacion.nombre:
            if Aplicacion.objects.filter(nombre=aplicacion.nombre,proyecto=proyecto).count() == 0:
                aplicacion.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                mensaje_error = 'La Aplicacion ' + aplicacion.nombre + ' ya existe en el proyecto, intente con otro nombre'
                return HttpResponseRedirect('/aplicaciones/editar/' + str(aplicacion.id) + '/?proyecto_id=' + str(proyecto.id) + '&aplicacion_id=' + str(aplicacion.id) + '&mensaje_error=' + mensaje_error) 
        else:
            aplicacion.save()
            return HttpResponseRedirect(self.get_success_url())

        # return render(request, 'modelos/modelo_update_form.html', {'form': form,'mensaje_error':mensaje_error})


from django.http import HttpResponseRedirect

class CrearAplicacionView(CreateView):
    model = Aplicacion
    form_class = AplicacionForm

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearAplicacionView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'],usuario=self.request.user)
            context['proyecto'] = proyecto
            # context['mensaje_error'] = self.request.GET['mensaje_error']
            # verifica si tiene vigencia de uso
            # context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

    def post(self,request,*args,**kwargs):
        mensaje_error=''
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])
        if form.is_valid():
            aplicacion = form.save(commit=False)
            aplicacion.proyecto = proyecto
            # Validar que el modelo sea unico

            if Aplicacion.objects.filter(nombre=aplicacion.nombre,proyecto=aplicacion.proyecto).count() == 0:
                aplicacion.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                mensaje_error = 'La Aplicacion ' + aplicacion.nombre + ' ya existe en el proyecto, intente con otro nombre'
                return HttpResponseRedirect('/aplicaciones/crear' + '/?proyecto_id=' + str(proyecto.id) + '&mensaje_error=' + mensaje_error)             
                # aplicacion.save()
        #     return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect('/aplicaciones/crear' + '/?proyecto_id=' + str(proyecto.id))             
        # return render(request, 'aplicaciones/aplicacion_form.html', {'form': form})

class BorrarAplicacionView(DeleteView):
    model = Aplicacion

    def get_success_url(self):
        return reverse_lazy('proyectos:arbol') + '?proyecto_id=' + self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(BorrarAplicacionView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        try:
            context['error'] = ''
            # proyecto = Proyecto.objects.get(id=self.object.proyecto.id,usuario=self.request.user)
            obj = Aplicacion.objects.get(id=self.object.id)
            context['nombre'] = obj.nombre
            context['proyecto_id'] = obj.proyecto.id
        except:
            context['error'] = '!!! No eres el propietario del proyecto !!!'
        return context

      