from django.urls import path
from .views import ListaProyectosView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import ListaProyectosView, ArbolProyectoView, CrearProyectoView, EditarProyectoView, BorrarProyectoView, dumpView, DesplegarPreciosView
from .views import ListaTextoView, CrearTextoView, EditarTextoView, BorrarTextoView, ProcesaTextoView, EsquemaView

proyectos_patterns = ([
    path('lista/', login_required(ListaProyectosView.as_view()), name='lista'),
    path('arbol/', login_required(ArbolProyectoView.as_view()), name='arbol'),
    path('crear/', login_required(CrearProyectoView.as_view()), name='crear'),
    path('crear_texto/', login_required(CrearTextoView.as_view()), name='crear_texto'),
    path('lista_texto/', login_required(ListaTextoView.as_view()), name='lista_texto'),
    path('editar_texto/<int:pk>/', login_required(EditarTextoView.as_view()), name='editar_texto'),
    path('borrar_texto/<int:pk>/', login_required(BorrarTextoView.as_view()), name='borrar_texto'),
    path('procesa_texto/', login_required(ProcesaTextoView.as_view()), name='procesa_texto'),
    path('editar/<int:pk>/',login_required(EditarProyectoView.as_view()), name='editar'),
    path('borrar/<int:pk>/',login_required(BorrarProyectoView.as_view()), name='borrar'),
    path('descarga/',login_required(dumpView.as_view()), name='descarga'),
    path('desplegar_precios', login_required(DesplegarPreciosView.as_view()), name='desplegar_precios'),
    path('esquema', login_required(EsquemaView.as_view()), name='esquema'),
], 'proyectos')