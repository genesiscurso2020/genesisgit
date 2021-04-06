from django.urls import path
from .views import HomeView, ListaErroresView, ConfigurarBaseView, PaletaView
from .views import ColoresView, OtrosView, ConfigurarModeloNuevaView
from .views import EditarReporteView
from .views import ConfigurarUpdateContiguoView, ConfigurarUpdateAbajoView, ConfigurarBorraView, ConfigurarBaseNuevaView
from .views import CrearPasosView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

crear_patterns = ([
    path('crear/',login_required(HomeView.as_view()), name='home'),
    path('lista/',login_required(ListaErroresView.as_view()), name='lista'),
    path('conf_base/',login_required(ConfigurarBaseView.as_view()), name='conf_base'),
    path('conf_base_nueva/',login_required(ConfigurarBaseNuevaView.as_view()), name='conf_base_nueva'),
    path('paleta/',login_required(PaletaView.as_view()), name='paleta'),
    path('colores/',login_required(ColoresView.as_view()), name='colores'),
    path('otros/',login_required(OtrosView.as_view()), name='otros'),
    path('conf_modelo/',login_required(ConfigurarModeloNuevaView.as_view()), name='conf_modelo'),
    path('conf_update_contiguo/',login_required(ConfigurarUpdateContiguoView.as_view()), name='conf_update_contiguo'),
    path('conf_update_abajo/',login_required(ConfigurarUpdateAbajoView.as_view()), name='conf_update_abajo'),
    path('conf_borra/',login_required(ConfigurarBorraView.as_view()), name='conf_borra'),
    path('crear_pasos/',login_required(CrearPasosView.as_view()), name='crear_pasos'),
    path('reporte/<int:pk>/',login_required(EditarReporteView.as_view()), name='reporte'),
], 'crear')