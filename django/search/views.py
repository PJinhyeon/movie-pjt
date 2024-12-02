from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SearchHistory
from .serializers import SearchHistorySerializer
from django.db.models import Count
from .models import SearchHistory

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def search_history_list(request):
    if request.method == 'GET':
        # 검색 기록 가져오기
        histories = SearchHistory.objects.filter(user=request.user)
        serializer = SearchHistorySerializer(histories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 검색 기록 저장
        data = request.data
        movie_id = data.get('movie')  # 영화 ID
        keyword = data.get('keyword')  # 영화 제목
        if not movie_id or not keyword:
            return Response({"error": "Movie ID and keyword are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 기록 생성
        search_history = SearchHistory.objects.create(
            user=request.user,
            keyword=keyword,
            movie=movie_id
        )
        serializer = SearchHistorySerializer(search_history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_search_histories(request):
    if request.method == 'DELETE':
        # 검색 기록 삭제
        SearchHistory.objects.filter(user=request.user).delete()
        return Response({"message": "All search histories have been deleted."}, status=status.HTTP_204_NO_CONTENT)
    

# 영화 정보 가져오기 위한 movie_detail 함수 임포트
from movies.views import movie_detail  # movies 앱의 movie_detail 함수 사용
import json
@api_view(['GET'])
def most_searched_movies(request):
    # 1. 검색 횟수를 기준으로 상위 6개의 영화 ID와 검색 횟수를 가져오기
    top_searches = (
        SearchHistory.objects.values('movie')  # 영화 ID 기준으로 그룹화
        .annotate(search_count=Count('movie'))  # 검색 횟수 계산
        .order_by('-search_count')[:6]  # 상위 6개 추출
    )

    results = []

    # 2. 각 영화 ID에 대해 TMDB API 호출 (movie_detail 함수 사용)
    for search in top_searches:
        movie_id = search['movie']
        # movie_detail 함수 호출
        movie_data_response = movie_detail(request, movie_id)
        
        if movie_data_response.status_code == 200:
            # JsonResponse에서 데이터를 추출
            movie_data = json.loads(movie_data_response.content)
            results.append(movie_data)  # 그대로 추가
        else:
            # 실패 시 간단한 오류 정보 추가
            results.append({
                "id": movie_id,
                "title": "영화 정보를 불러올 수 없습니다.",
                "poster_path": None,
            })

    # 3. 결과 반환
    return Response(results)

