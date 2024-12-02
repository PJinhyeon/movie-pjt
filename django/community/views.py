from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleListSerializer, CommentSerializer, ArticleSerializer
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import Length
from django.conf import settings
import requests

@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        response_data = []

        for article in articles:
            # TMDB API 호출로 영화 데이터 가져오기
            api_url = f"https://api.themoviedb.org/3/movie/{article.movie_id}?language=ko-KR"
            headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}
            try:
                tmdb_response = requests.get(api_url, headers=headers)
                tmdb_response.raise_for_status()
                movie_data = tmdb_response.json()
            except requests.exceptions.RequestException:
                movie_data = {"id": article.movie_id, "title": "영화 정보를 불러올 수 없습니다."}

            # 게시글 데이터에 영화 정보를 추가
            response_data.append({
                "id": article.id,
                "user": article.user.username,
                "title": article.title,
                "movie": movie_data,  # TMDB에서 가져온 영화 데이터 포함
                "content": article.content,
                "created_at": article.created_at,
                "updated_at": article.updated_at,
            })

        return Response(response_data)

    elif request.method == 'POST':
        # 요청 데이터에서 movie_id와 content 가져오기
        movie_id = request.data.get('movie_id')
        title = request.data.get('title')
        content = request.data.get('content')

        if not movie_id or not content or not title:
            error_message = "Movie ID and content are required"
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        # 영화 ID만 저장
        try:
            article = Article.objects.create(
                user=request.user,
                movie_id=movie_id,  # 영화 ID만 저장
                title = title,
                content=content
            )
        except Exception as e:
            error_message = f"Failed to create article: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Article created successfully", "id": article.id}, status=status.HTTP_201_CREATED)


# 특정 게시글 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method in ['PUT', 'DELETE']:
        if article.user != request.user:
            raise PermissionDenied("You do not have permission to modify this article.")

    if request.method == 'GET':
        # TMDB API 호출로 영화 데이터 가져오기
        api_url = f"https://api.themoviedb.org/3/movie/{article.movie_id}?language=ko-KR"
        headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}

        try:
            tmdb_response = requests.get(api_url, headers=headers)
            tmdb_response.raise_for_status()
            movie_data = tmdb_response.json()
        except requests.exceptions.RequestException as e:
            movie_data = {"title": "Unknown", "poster_path": None}  # 기본 값 설정

        # 응답 데이터 구성
        response_data = {
            "id": article.id,
            "user": article.user.username,
            "title": article.title,
            "content": article.content,
            "created_at": article.created_at,
            "updated_at": article.updated_at,
            "movie": {
                "title": movie_data.get("title"),
                "poster_path": movie_data.get("poster_path"),
                "overview": movie_data.get("overview"),
                "release_date": movie_data.get("release_date"),
            }
        }

        return Response(response_data)
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 특정 유저의 게시글 목록 조회
@api_view(['GET'])
def user_articles(request, person_id):
    articles = Article.objects.filter(user__id=person_id)
    # articles = get_list_or_404(Article, user__id=person_id)
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

# 특정 게시글의 댓글 목록 조회 및 댓글 생성
@api_view(['GET', 'POST'])
def comment_list(request, article_id):
    if request.method == 'GET':
        comments = get_list_or_404(Comment, article__id=article_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 게시글의 댓글 목록 조회 및 댓글 생성
@api_view(['GET', 'POST'])
def comment_list(request, article_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(article__id=article_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 댓글 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # 수정 (작성자 본인만 가능)
    elif request.method == 'PUT':
        if request.user != comment.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제 (작성자 본인만 가능)
    elif request.method == 'DELETE':
        if request.user != comment.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def recent_articles(request):
    articles = Article.objects.all().order_by('-created_at')  # 작성일 기준 내림차순
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def community_main(request):
    top_commented_articles = Article.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:10]
    recent_articles = Article.objects.all().order_by('-created_at')
    top_commented_serializer = ArticleListSerializer(top_commented_articles, many=True)
    recent_serializer = ArticleListSerializer(recent_articles, many=True)

    return Response({
        "top_commented": top_commented_serializer.data,
        "recent": recent_serializer.data
    })

@api_view(['GET'])
def search_articles(request):
    query = request.GET.get('q', '').strip()  # 검색어 가져오기
    if query:
        articles = Article.objects.filter(
            Q(content__icontains=query)
        ).annotate(
            relevance=Length('content')  # 컨텐츠 길이를 기준으로 relevance 점수 계산 (다양한 기준 적용 가능)
        ).order_by('-relevance', '-created_at')  # 관련성과 최신순 정렬
    else:
        articles = Article.objects.none()

    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

