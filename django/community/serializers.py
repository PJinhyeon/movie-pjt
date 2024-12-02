from rest_framework import serializers
from .models import Article, Comment
import requests
from django.conf import settings

class ArticleListSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'user', 'title', 'movie', 'content', 'created_at', 'updated_at']

    def get_movie(self, obj):
        # TMDB API를 사용해 영화 정보를 동적으로 가져옴
        api_url = f"https://api.themoviedb.org/3/movie/{obj.movie_id}?language=ko-KR"
        headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # API 호출 실패 시 기본 데이터 반환
            return {"id": obj.movie_id, "title": "영화 정보를 불러올 수 없습니다."}

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'article', 'created_at', 'updated_at']
