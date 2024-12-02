from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UploadedImageSerializer
from .models import UploadedImage
from google.cloud import vision
from django.conf import settings
import os

import json
from .gpt_utils import get_tmdb_keywords

from django.http import JsonResponse
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import RecommendedResult
from django.shortcuts import get_object_or_404
from .serializers import RecommendedResultSerializer

API_TOKEN = settings.API_TOKEN

# google_api >> upload image >> 키워드 추출
class ImageUploadView(APIView):
    def post(self, request):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_image = serializer.save()

            # Vision API 설정
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_CLOUD_CREDENTIALS
            client = vision.ImageAnnotatorClient()

            # 이미지 분석
            with open(uploaded_image.image.path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.label_detection(image=image)

            # Vision API 결과 추출
            labels = [label.description for label in response.label_annotations]
            return Response({"labels": labels})
        return Response(serializer.errors, status=400)
    


# gpt_api >> 이미지에서 추출된 키워드와 tmdb 키워드와 매핑
class MatchTMDBKeywordsView(APIView):
    def post(self, request):
        vision_keywords = request.data.get("keywords", [])
        if not vision_keywords:
            return Response({"error": "No keywords provided"}, status=400)

        # TMDB 키워드 로드
        # views.py와 같은 폴더에 있는 tmdb_keywords.json 파일 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tmdb_keywords_path = os.path.join(current_dir, "tmdb_keywords.json")

        # 파일 읽기 (UTF-8 인코딩으로 설정)
        with open(tmdb_keywords_path, "r", encoding="utf-8") as f:
            tmdb_keywords = json.load(f)

        # GPT API를 통해 TMDB 키워드 매핑
        matched_keywords = get_tmdb_keywords(vision_keywords, tmdb_keywords)
        print('////match:', matched_keywords)
        return Response({"matched_keywords": matched_keywords})
    

def movies_by_keywords(request):
    api_url_template = "https://api.themoviedb.org/3/keyword/{keyword_id}/movies"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    total_movies = {}
    try:
        # 요청에서 매칭된 키워드 추출
        matched_keywords = request.GET.getlist('keywords')  # 키워드 ID 배열
        if not matched_keywords:
            return JsonResponse({"error": "No keywords provided"}, status=400)

        # 키워드별 영화 데이터 가져오기
        for keyword_id in matched_keywords:
            params = {
                "include_adult": False,
                "language": "ko-KR",
                "page": 1,
            }
            api_url = api_url_template.format(keyword_id=keyword_id)
            response = requests.get(api_url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                for movie in data.get('results', []):
                    movie_id = movie['id']
                    if movie_id not in total_movies:
                        total_movies[movie_id] = {
                            "movie": movie,
                            "keyword_count": 0
                        }
                    total_movies[movie_id]["keyword_count"] += 1
            else:
                return JsonResponse({"error": f"Failed to fetch data for keyword {keyword_id}"}, status=response.status_code)

        # 키워드 매칭 수 기준으로 정렬
        sorted_movies = sorted(
            total_movies.values(),
            key=lambda x: x["keyword_count"],
            reverse=True
        )

        # 상위 5개 영화 반환
        top_movies = [movie["movie"] for movie in sorted_movies[:5]]
        return JsonResponse(top_movies, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# 1. 추천 결과 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_recommendation(request):
    user = request.user
    movie_id = request.data.get('movie')

    if not movie_id:
        return Response({"error": "movie ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # 중복 저장 방지
    if RecommendedResult.objects.filter(user=user, movie=movie_id).exists():
        return Response({"error": "This movie has already been recommended to the user."}, status=status.HTTP_400_BAD_REQUEST)

    recommendation = RecommendedResult.objects.create(user=user, movie=movie_id)
    serializer = RecommendedResultSerializer(recommendation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 2. 특정 사용자에 대한 추천결과 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_recommendations(request):
    user = request.user
    recommendations = RecommendedResult.objects.filter(user=user)
    serializer = RecommendedResultSerializer(recommendations, many=True)
    return Response(serializer.data)

# 3. 추천 ID로 특정 추천 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation_detail(request, recommendation_id):
    recommendation = get_object_or_404(RecommendedResult, id=recommendation_id, user=request.user)
    serializer = RecommendedResultSerializer(recommendation)
    return Response(serializer.data)

# 4. 추천 결과 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_recommendation(request, recommendation_id):
    recommendation = get_object_or_404(RecommendedResult, id=recommendation_id, user=request.user)
    recommendation.delete()
    return Response({"message": "Recommendation deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# 5. 모든 추천 조회 (관리자 전용)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_recommendations(request):
    recommendations = RecommendedResult.objects.all()
    serializer = RecommendedResultSerializer(recommendations, many=True)
    return Response(serializer.data)
