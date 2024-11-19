from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserProfileSerializer

@api_view(['GET'])
def profile(request, person_id):
    user = get_object_or_404(User, pk=person_id)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def profile_list(request):
    users = get_list_or_404(User)
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

