from R_E_M import views
from django.urls import path

urlpatterns = [
    path('', views.photography_home, name='photos_home'),
    path('<slug:slug>/', views.photo_album_view, name='album_view'),
    path('<slug:slug>', views.photo_single_view, name='picture_view'),
    path('upload/', views.photo_upload, name='picture_upload')
]
