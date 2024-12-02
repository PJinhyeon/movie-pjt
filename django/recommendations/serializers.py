from rest_framework import serializers
from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'

from .models import RecommendedResult

class RecommendedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedResult
        fields = ['id', 'user', 'movie', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']

