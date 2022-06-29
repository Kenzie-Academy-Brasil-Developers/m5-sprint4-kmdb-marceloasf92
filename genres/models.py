from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=127)

    movies = models.ManyToManyField("movies.Movie", related_name="genres")

