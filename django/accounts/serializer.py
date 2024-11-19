# accounts/serializers.py
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True
    )

    # 저장 로직 추가
    def save(self, request):
        user = super().save(request)  # 기본 RegisterSerializer의 save 호출
        user.nickname = self.validated_data.get('nickname', '')
        user.profile_picture = self.validated_data.get('profile_picture', None)
        user.save()
        return user