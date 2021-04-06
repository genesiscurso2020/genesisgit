"""piensaluegoensenia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core.urls import core_patterns
from proyectos.urls import proyectos_patterns
from aplicaciones.urls import aplicaciones_patterns
from modelos.urls import modelos_patterns
from propiedades.urls import propiedades_patterns
from reglas.urls import reglas_patterns
from crear.urls import crear_patterns
from registration.urls import registration_patterns
from personalizacion.urls import personalizacion_patterns
from reviews.urls import reviews_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(core_patterns)),
    path('proyectos/',include(proyectos_patterns)),
    path('aplicaciones/',include(aplicaciones_patterns)),
    path('modelos/',include(modelos_patterns)),
    path('propiedades/',include(propiedades_patterns)),
    path('reglas/',include(reglas_patterns)),
    path('crear/',include(crear_patterns)),
    path('personalizacion/', include(personalizacion_patterns)),
    path('reviews/', include(reviews_patterns)),
    # Autenticacion
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include(registration_patterns)),
]

if settings.DEBUG == True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
