from R_E_M import views
from django.urls import path

urlpatterns = [
    path('', views.webdev_home, name='webdev'),
    path('websites/<slug:slug>/', views.webdev_view, name='webdev_view'),
    path('create/', views.webdev_create, name="webdev_create")
]