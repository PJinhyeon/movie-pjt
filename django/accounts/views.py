from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserProfileSerializer, UserProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def profile(request, person_id):
    try:
        user = User.objects.get(pk=person_id)  # User.objects.get()으로 통일
    except User.DoesNotExist:
        raise Http404("사용자를 찾을 수 없습니다.")

    # GET 요청: 사용자 정보 조회
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT 요청: 사용자 정보 수정
    elif request.method == 'PUT':
        if request.user.id != person_id:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileUpdateSerializer(instance = user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE 요청: 사용자 계정 삭제
    elif request.method == 'DELETE':
        if request.user.id != person_id:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({"detail": "사용자 계정이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def profile_list(request):
    users = get_list_or_404(User)
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



