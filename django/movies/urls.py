from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # tmdb 에서 api로 movie 관련 데이터들 가져오기
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/credits/', views.movie_credits, name='movie_credits'),

    # path('actors/', views.actor_list, name='actor_list'),
    # path('actors/<int:actor_pk>/', views.actor_detail, name='actor_detail'),
    path('genre/<int:genre_id>/', views.movies_by_genre, name='movies_by_genre'),
    path('genres/', views.genre_list, name='genre_list'),
    path('search/', views.search_movies, name='search-movies'),

    # 영화 찜
    path('cart/', views.cart_list, name='cart_list'),
    path('cart/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('movies-with-most-articles/', views.movies_with_most_articles, name='movies_with_most_articles'),
]