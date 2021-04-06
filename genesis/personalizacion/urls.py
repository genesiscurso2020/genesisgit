from django.urls import path
from .views import ListarPersonalizaView,  EditarPersonalizaView, CrearPersonalizaView, BorrarPersonalizaView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

personalizacion_patterns = ([
    path('', login_required(ListarPersonalizaView.as_view()), name='home'),
    path('editar/<int:pk>/',login_required(EditarPersonalizaView.as_view()), name='editar'),
    path('crear/',login_required(CrearPersonalizaView.as_view()), name='crear'),
    path('borrar/<int:pk>/',login_required(BorrarPersonalizaView.as_view()), name='borrar'),
], 'personalizacion')