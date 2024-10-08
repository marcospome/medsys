"""
URL configuration for medicalsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from apps.home.views import custom_404_view, custom_500_view

# Configuración para manejar el error 404, 500 y 403.
handler404 = custom_404_view
handler500 = custom_500_view

handler403 = TemplateView.as_view(template_name='base/403.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
]
