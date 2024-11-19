from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    poster = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField()
    release_date = models.DateField()
    runtime = models.PositiveIntegerField(help_text="상영 시간(분 단위)")
    status = models.CharField(max_length=50, blank=True, null=True)
    adult = models.BooleanField(default=False)
    vote_average = models.FloatField()
    vote_count = models.PositiveIntegerField()
    original_language = models.CharField(max_length=50, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    watch_platforms = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    keywords = models.ManyToManyField('Keyword', related_name='movies', blank=True)

    def __str__(self):
        return self.title


class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name