from R_E_M import views
from django.urls import path

urlpatterns = [

    path('', views.blog, name='blog_home'),
    path('api/', views.blog_ajax, name="blog_ajax"),
    path('<slug:cat>/<slug:slug>/', views.blog_single_view, name='blog_single_view'),

    path('create/', views.blog_create, name='blog_create')

]
