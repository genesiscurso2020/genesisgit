from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django import forms
from .models import Profile
from core.models import Genesis
from crear import views
from proyectos.models import Proyecto,LicenciaUso


# Create your views here.
class RegistroView(CreateView):
    form_class = UserCreationFormWithEmail
    # success_url = reverse_lazy('login')
    template_name = 'registration/registro.html'

    def get_success_url(self):
        user = self.object
        etapa = 'CrearSeguridad'
        # crear el archivo download en el directorio del usuario
        gen = Genesis.objects.get(nombre='GENESIS')
        # # crear la pagina
        stri = views.LeerArchivoEnTexto(gen.directoriotexto + 'download_file.html',etapa,'',user.username)
        stri = stri.replace('@file', user.username + '/ultimo.zip')
        print('directorio ',gen.directoriogenesis + 'core/static/core/zipfiles/' + user.username)
        # Crear el directorio para el usuario donde se almacena el zip
        views.CrearDirectorio(gen.directoriogenesis + 'core/static/core/zipfiles/' + user.username,etapa,'',user.username,True)
        # Crear el directorio para el usuario donde se almacena el archivo download.html
        views.CrearDirectorio(gen.directoriogenesis + 'proyectos/templates/proyectos/' + user.username,etapa,'',user.username,True)

        views.EscribirEnArchivo(gen.directoriogenesis + 'proyectos/templates/proyectos/' + user.username + '/download.html',stri,etapa,'',user.username)

        return reverse_lazy('login') + '?registro_correcto'

    def get_form(self,form_class=None):
        form = super(RegistroView,self).get_form()
        # Modificar campos
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de Usuario'}) 
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Direccion Email'}) 
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}) 
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Verificacion de password'}) 
        form.fields['username'].label = ''
        form.fields['email'].label = ''
        form.fields['password1'].label = ''
        form.fields['password2'].label = ''
        return form

class ProfileUpdateView(UpdateView):
    form_class = ProfileForm
    # fields = ['nombre', 'avatar','biografia']
    success_url = reverse_lazy('core:home')
    template_name = 'registration/profile_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        return context

    def get_object(self):
        # Recuperar el objeto que se edita
        profile, created = Profile.objects.get_or_create(user = self.request.user)
        return profile

class EmailUpdateView(UpdateView):
    form_class = EmailForm
    # fields = ['nombre', 'avatar','biografia']
    success_url = reverse_lazy('core:home')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # Recuperar el objeto que se edita
        return self.request.user

    def get_form(self,form_class=None):
        form = super(EmailUpdateView,self).get_form()
        # Modificar campos
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Direccion Email'}) 
        form.fields['email'].label = ''
        return form

def VerificaVigenciaUsuario(usuario):
    if LicenciaUso.objects.filter(usuario=usuario, vigente=True).count() > 0:
       return True
    return False           

def PropietarioProyecto(id,usuario):
    try:
        Proyecto.objects.get(id=id,usuario=usuario)    
        return ''
    except:
        return '!!! No eres el propietario del proyecto !!!'