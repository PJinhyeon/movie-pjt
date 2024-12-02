from django.urls import path
from .views import ImageUploadView
from .views import MatchTMDBKeywordsView
from .views import movies_by_keywords
from . import views


urlpatterns = [
    path('api/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('api/match-tmdb/', MatchTMDBKeywordsView.as_view(), name='match-tmdb-keywords'), # TMDB 키워드 매핑 API 경로 추가
    path('api/movies-by-keywords/', movies_by_keywords, name='movies-by-keywords'),
    path('recommendations/', views.save_recommendation, name='save_recommendation'),  # 추천 저장
    path('recommendations/user/', views.user_recommendations, name='user_recommendations'),  # 특정 사용자 추천 조회
    path('recommendations/<int:recommendation_id>/', views.recommendation_detail, name='recommendation_detail'),  # 추천 ID로 조회
    path('recommendations/<int:recommendation_id>/delete/', views.delete_recommendation, name='delete_recommendation'),  # 추천 삭제
    path('recommendations/all/', views.all_recommendations, name='all_recommendations'),  # 모든 추천 조회 (관리자)
]

