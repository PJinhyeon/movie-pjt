from django.urls import path
from . import views

app_name ='community'

urlpatterns = [
    path('articles/', views.article_list, name='article-list'),
    path('articles/<int:article_id>/', views.article_detail, name='article-detail'),
    path('user/<int:person_id>/articles/', views.user_articles, name='user-articles'),
    path('articles/<int:article_id>/comments/', views.comment_list, name='comment-list'),
    path('comments/<int:comment_id>/', views.comment_detail, name='comment-detail'),
    path('articles/recent/', views.recent_articles, name='recent-articles'),
    path('main/', views.community_main, name='community-main'),
    path('articles/search/', views.search_articles, name='search-articles'),
]