from django.db import models
from django.conf import settings


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    movie = models.IntegerField() # tmdb의 영화 id만 저장
    added_at = models.DateTimeField(auto_now_add=True)


