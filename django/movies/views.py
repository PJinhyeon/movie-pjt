from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from django.db.models import Count
from community.models import Article  # Articles 앱의 모델
import json

API_KEY = settings.API_KEY
API_TOKEN = settings.API_TOKEN

import requests
from django.http import JsonResponse


# # 전체 배우 목록 제공
# def actor_list(request):
#     total_data = []
#     api_url = "https://api.themoviedb.org/3/person/popular"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_TOKEN}"
#     }

#     try:
#         # 1페이지부터 20페이지까지 데이터를 가져옴
#         for i in range(1, 2):
#             response = requests.get(f"{api_url}?language=ko-KR&page={i}", headers=headers)
#             if response.status_code == 200:
#                 data = response.json()
#                 total_data.extend(data.get('results', []))  # 'results' 키의 데이터를 추가
#             else:
#                 return JsonResponse({"error": f"Failed to fetch data at page {i}"}, status=response.status_code)

#         # 모든 데이터를 JSON으로 반환
#         return JsonResponse(total_data, safe=False)

#     except Exception as e:
#         # 예외 처리
#         return JsonResponse({"error": str(e)}, status=500)


# # 단일 배우 정보 제공
# def actor_detail(request, actor_pk):
#     api_url = f"https://api.themoviedb.org/3/person/{actor_pk}?language=ko-KR"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_TOKEN}"
#     }

#     try:
#         # TMDB API 호출
#         response = requests.get(api_url, headers=headers)
#         if response.status_code == 200:
#             data = response.json()  # 성공적으로 데이터 가져옴
#             return JsonResponse(data, safe=False)
#         else:
#             # API 호출 실패 시 에러 반환
#             return JsonResponse({"error": "Failed to fetch actor data"}, status=response.status_code)
#     except Exception as e:
#         # 예외 처리
#         return JsonResponse({"error": str(e)}, status=500)


# 전체 영화 목록 제공 >> Movie list > Popular
def movie_list(request):
    total_movies = []
    api_url = "https://api.themoviedb.org/3/movie/popular"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        # 1페이지부터 20페이지까지 데이터를 가져옴
        for i in range(1, 10):
            response = requests.get(f"{api_url}?language=ko-KR&page={i}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                total_movies.extend(data.get('results', []))  # 'results' 키의 데이터를 추가
            else:
                return JsonResponse({"error": f"Failed to fetch data at page {i}"}, status=response.status_code)

        # 모든 데이터를 JSON으로 반환
        return JsonResponse(total_movies, safe=False)

    except Exception as e:
        # 예외 처리
        return JsonResponse({"error": str(e)}, status=500)
    



# 단일 영화 정보 제공
def movie_detail(request, movie_pk):
    api_url = f"https://api.themoviedb.org/3/movie/{movie_pk}?language=ko-KR"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        # TMDB API 호출
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # API로부터 받은 데이터
            return JsonResponse(data, safe=False)
        else:
            # API 호출 실패 시 에러 반환
            return JsonResponse({"error": "Failed to fetch movie data"}, status=response.status_code)
    except Exception as e:
        # 예외 처리
        return JsonResponse({"error": str(e)}, status=500)


# 영화별 배우, 감독 조회
def movie_credits(request, movie_pk):
    api_url = f"https://api.themoviedb.org/3/movie/{movie_pk}/credits?language=ko-KR"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        # TMDB API 호출
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # API로부터 받은 데이터
            return JsonResponse(data, safe=False)
        else:
            # API 호출 실패 시 에러 반환
            return JsonResponse({"error": "Failed to fetch movie credits data"}, status=response.status_code)
    except Exception as e:
        # 예외 처리
        return JsonResponse({"error": str(e)}, status=500)



# 장르별 영화 조회
def movies_by_genre(request, genre_id):
    api_url = "https://api.themoviedb.org/3/discover/movie"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    total_movies = []

    try:
        # 1페이지부터 20페이지까지 가져오기 (필요 시 범위를 조정 가능)
        for page in range(1, 10):
            params = {
                "language": "ko-KR",
                "with_genres": genre_id,
                "page": page,
            }
            response = requests.get(api_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                total_movies.extend(data.get('results', []))
            else:
                return JsonResponse({"error": f"Failed to fetch data for genre {genre_id} at page {page}"}, status=response.status_code)

        return JsonResponse(total_movies, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# 장르 리스트
def genre_list(request):
    api_url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)  # 데이터를 JSON으로 반환
        else:
            return JsonResponse({"error": "Failed to fetch genre list"}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from .serializers import CartItemSerializer

# 영화 찜
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_list(request):
    if request.method == 'GET':
        cartitems = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cartitems, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, movie_id):
    if request.method == 'DELETE':
        cartitem = CartItem.objects.get(movie=movie_id, user=request.user)
        cartitem.delete()
        return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)


# 게시글에서 선택된 영화
@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({"results": []}, status=200)

    api_url = f"https://api.themoviedb.org/3/search/movie?query={query}&language=ko-KR&api_key={settings.API_KEY}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch movies"}, status=response.status_code)

@api_view(['GET'])
def movies_with_most_articles(request):
    top_movies = (
        Article.objects.values('movie_id')  # 영화별로 그룹화
        .annotate(article_count=Count('id'))  # 게시글 수 계산
        .order_by('-article_count')[:6]  # 상위 10개 추출
    )

    results = []
    for movie in top_movies:
        movie_id = movie['movie_id']
        # movie_detail 호출
        movie_data_response = movie_detail(request, movie_id)
        if movie_data_response.status_code == 200:
            # JsonResponse에서 데이터 디코딩
            movie_data = json.loads(movie_data_response.content)
            results.append({
                "id": movie_id,
                "title": movie_data.get("title"),
                "poster_path": movie_data.get("poster_path"),
                "article_count": movie['article_count'],
            })
        else:
            results.append({
                "id": movie_id,
                "title": "영화 정보를 불러올 수 없습니다.",
                "poster_path": None,
                "article_count": movie['article_count'],
            })

    return Response(results)



