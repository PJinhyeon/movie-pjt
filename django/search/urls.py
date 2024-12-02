from django.urls import path
from . import views

app_name = 'search-history'
urlpatterns = [
    path('', views.search_history_list, name='search_history_list'),
    path('delete/', views.delete_all_search_histories, name='delete_all_search_histories'),
    path('topsearch/', views.most_searched_movies, name='topsearch'),
]