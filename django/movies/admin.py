from django.contrib import admin
from .models import Genre, Actor, Movie, Keyword

# 각 모델을 admin에 등록합니다.
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Keyword)
