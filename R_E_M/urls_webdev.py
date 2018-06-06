from R_E_M import views
from django.urls import path

url_patterns = [
    path('', views.webdev_home, name='webdev'),
    path('<slug:slug>/', views.webdev_view, name='webdev_view')
]