from django.urls import path
from .views import CrearAplicacionView, EditarAplicacionView, BorrarAplicacionView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

aplicaciones_patterns = ([
    path('crear/',login_required(CrearAplicacionView.as_view()), name='crear'),
    path('editar/<int:pk>/',login_required(EditarAplicacionView.as_view()), name='editar'),
    path('borrar/<int:pk>/',login_required(BorrarAplicacionView.as_view()), name='borrar'),
], 'aplicaciones')