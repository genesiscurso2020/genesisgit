from django.urls import path
from .views import CrearReglaView, EditarReglaView, BorrarReglaView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

reglas_patterns = ([
    path('crear/',login_required(CrearReglaView.as_view()), name='crear'),
    path('editar/<int:pk>/',login_required(EditarReglaView.as_view()), name='editar'),
    path('borrar/<int:pk>/',login_required(BorrarReglaView.as_view()), name='borrar'),
], 'reglas')