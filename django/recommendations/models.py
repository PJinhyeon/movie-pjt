from django.db import models
from django.conf import settings

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
class RecommendedResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendeduser')
    movie = models.IntegerField() # tmdb의 영화 id만 저장
    added_at = models.DateTimeField(auto_now_add=True)
