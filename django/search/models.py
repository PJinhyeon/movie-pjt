from django.db import models
from django.conf import settings


# Create your models here.
class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_histories')
    keyword = models.CharField(max_length=255)
    movie = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.keyword}"
    