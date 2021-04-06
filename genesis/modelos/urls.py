from django.urls import path
from .views import CrearModeloView, EditarModeloView, BorrarModeloView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

modelos_patterns = ([
    path('crear/',login_required(CrearModeloView.as_view()), name='crear'),
    path('editar/<int:pk>/',login_required(EditarModeloView.as_view()), name='editar'),
    path('borrar/<int:pk>/',login_required(BorrarModeloView.as_view()), name='borrar'),
], 'modelos')