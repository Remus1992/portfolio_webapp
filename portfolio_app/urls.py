"""portfolio_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from R_E_M import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('about/', views.about, name="about"),
    path('technology/', views.technology, name="technology"),
    path('contact/', views.contact, name="contact"),
    path('', views.home, name='home'),
    path('photography/', include('R_E_M.urls_photography')),
    path('filmmaking/', include('R_E_M.urls_filmmaking')),
    path('webdev/', include('R_E_M.urls_webdev')),
    path('blog/', include('R_E_M.urls_blog')),
    path('instagram_api/', views.instagram_api, name="instagram_api" )
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

