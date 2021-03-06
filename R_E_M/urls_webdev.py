from R_E_M import views
from django.urls import path

urlpatterns = [
    path('', views.webdev_home, name='webdev'),
    path('api/', views.website_ajax, name="website_ajax"),
    path('websites/<slug:cat>/<slug:slug>/', views.webdev_view, name='website_single_view'),
    path('create/', views.webdev_create, name="webdev_create")
]