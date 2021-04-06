from django.urls import path
from .views import CrearPropiedadView, EditarPropiedadView, BorrarPropiedadView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

propiedades_patterns = ([
    path('crear/',login_required(CrearPropiedadView.as_view()), name='crear'),
    path('editar/<int:pk>/',login_required(EditarPropiedadView.as_view()), name='editar'),
    path('borrar/<int:pk>/',login_required(BorrarPropiedadView.as_view()), name='borrar'),
], 'propiedades')