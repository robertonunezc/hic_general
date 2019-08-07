"""hic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^inicio/', include('hic.main.url', namespace="main")),
    url(r'^pacientes/', include('hic.paciente.url', namespace="pacientes")),
    url(r'^citas/', include('hic.cita.url', namespace="citas")),
    url(r'^consultas/', include('hic.consulta.url', namespace="consultas")),
    url(r'^$', views.login,
        {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^accounts/login/$', views.login,
        {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^accounts/logout/$', views.logout,
        {'template_name': 'registration/logout.html', 'next_page': 'auth_login'},
        name='auth_logout', )
]
