from rest_framework import serializers
from .models import SearchHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'keyword', 'movie', 'searched_at']
        read_only_fields = ['user', 'searched_at']