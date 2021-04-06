from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import BusquedaForm
from proyectos.views import VerificaVigenciaUsuario

# Create your views here.

class CorePageView(FormView):
    template_name = "core/home.html"
    form_class = BusquedaForm
    # success_url = reverse_lazy('core:home')

    def get_success_url(self):
        # return reverse_lazy('proyectos:lista') + '?criterio=' + self.request.POST['textob'] + '&duplica=0'
        print('post')
        return reverse_lazy('proyectos:lista') + '?criterio=3' + '&duplica=0'

    def get_context_data(self,**kwargs):
        context = super(CorePageView, self).get_context_data(**kwargs)
        try:
            context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['vigente'] = False
        return context

    # def post(self,request,*args,**kwargs):
    #     # print('llegoooooo')
    #     # texto = self.request.POST['textob']
    #     # print(texto)
    #     return HttpResponseRedirect(self.get_success_url())

    # def get(self, request, *args, **kwargs):
    #     print('llegopri')
    #     context = self.get_context_data()
    #     try:
    #         lista = ListaProyectos(self.request.GET['textob'], request.user)
    #     except:
    #         print ('aqui')
    #         return HttpResponseRedirect(self.get_success_url())
    #         lista = ListaProyectos(None, request.user)

    #     context['lista_proyectos'] = lista
    #     """Handle GET requests: instantiate a blank version of the form."""
    #     # return reverse_lazy('proyectos:lista') #+ '?criterio=' + self.request.POST['textob']
    #     return render_to_response('proyectos/proyecto_list.html', context) 
        # return self.render_to_response(self.get_context_data())

