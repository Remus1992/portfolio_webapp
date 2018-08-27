from R_E_M import views
from django.urls import path

urlpatterns = [
    path('', views.filmmaking_home, name="movie_home"),
    path('movies/<slug:cat>/<slug:slug>', views.movie_single_view, name="movie_single_view"),
    path('create/', views.movie_create, name="movie_create")
]
