from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie-list'),
    path('<int:movie_pk>/', views.movie_detail, name='movie-detail'),
    path('genres/', views.genre_list, name='genre-list'),
]
