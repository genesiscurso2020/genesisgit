from django.urls import path
from .views import ListarReviewView,  CrearReviewView, CrearRespuestaView
from . import views

reviews_patterns = ([
    path('', ListarReviewView.as_view(), name='home'),
    path('crear/',CrearReviewView.as_view(), name='crear'),
    path('respuesta/',CrearRespuestaView.as_view(), name='respuesta'),
], 'reviews')