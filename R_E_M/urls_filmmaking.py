from R_E_M import views
from django.urls import path

url_patterns = [
    path('', views.filmmaking_home, name="movie_home"),
    path('<slug:slug>', views.movie_single_view, name="movie")
]