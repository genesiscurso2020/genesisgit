from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from .models import Review, Respuesta
from registration.models import Profile
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import ReviewForm, RespuestaForm
from django.contrib.auth.models import User
from registration.views import VerificaVigenciaUsuario

import os

# @method_decorator(staff_member_required,name='dispatch')
class ListarReviewView(ListView):
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ListarReviewView, self).get_context_data(**kwargs)
        try:
            context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['vigente'] = False

        lista =[]
        tel = Review.objects.filter(activo=True).order_by('-created')
        nm = ''
        for te in tel:
            profile = Profile.objects.get(user=te.usuario)
            if te.motivo == 'c':
                nm = 'comentario'
            if te.motivo == 'f':
                nm = 'calificacion'
            if te.motivo == 's':
                nm = 'sugerencia'
            if te.motivo == 't':
                nm = 'consulta'

            lista.append([te.usuario.username, profile.avatar, te.created, nm, te.texto, profile.nombre, te.id,'w'])
            listar = Respuesta.objects.filter(review=te)
            for lr in listar:
                nombre = ''
                avatar = None
                try:
                    profile = Profile.objects.get(user=lr.usuario)
                    nombre = profile.nombre
                    avatar = profile.avatar
                except:
                    nombre = lr.usuario.username
                    avatar = None
                lista.append([lr.usuario.username, avatar, lr.created, '', lr.texto,nombre,lr.id,'r'])

        context['lista'] = lista        
        return context

class CrearReviewView(CreateView):
    model = Review
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super(CrearReviewView, self).get_context_data(**kwargs)
        try:
            context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['vigente'] = False
            
        return context

    def get_success_url(self):
        return reverse_lazy('reviews:home')
        # return reverse_lazy('proyectos:editar', args=[self.object.id]) + '?ok'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        user = request.user
        # print(user)
        if form.is_valid():
            review = form.save(commit=False)
            review.usuario = user
            review.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

from django.core.mail import EmailMessage
from django.utils.safestring import SafeText

class CrearRespuestaView(CreateView):
    model = Respuesta
    form_class = RespuestaForm

    def get_context_data(self, **kwargs):
        context = super(CrearRespuestaView, self).get_context_data(**kwargs)
        try:
            context['vigente'] = VerificaVigenciaUsuario(self.request.user)
        except:
            context['vigente'] = False
            
        return context
        
    def get_success_url(self):
        return reverse_lazy('reviews:home')
        # return reverse_lazy('proyectos:editar', args=[self.object.id]) + '?ok'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        review = Review.objects.get(id = request.GET['review_id'])        # print(user)
        profile = Profile.objects.get(user=review.usuario)
        user = request.user
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.review = review
            respuesta.usuario = user
            respuesta.save()

            if profile.recibemails:
                # enviar email a duenio del review
                asunto = 'Respuesta a tu review de: ' + str(review.created.month) + '-' + str(review.created.day) + '-' + str(review.created.year) + '  ' + str(review.created.hour) + ':' + str(review.created.minute)
                texto = respuesta.texto
                texto = texto.replace('<p>', '')
                texto = texto.replace('</p>', '')
                body = 'El texto es: ' + texto

                email = EmailMessage(asunto, body, to=[review.usuario.email])
                email.send()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

