from django.contrib import admin
from .models import Article, Comment

# 각 모델을 admin에 등록합니다.
admin.site.register(Article)
admin.site.register(Comment)
