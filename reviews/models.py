from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ReviewRecomendation(models.TextChoices):
    MUST_WATCH = ("Must Watch",)
    SHOULD_WATCH = ("Should Watch",)
    AVOID_WATCH = ("Avoid Watch",)
    NO_OPINION = ("No Opinion",)


MIN = 1
MAX = 10


class Review(models.Model):
    stars = models.IntegerField(
        validators=[MinValueValidator(MIN), MaxValueValidator(MAX)])
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=50, choices=ReviewRecomendation.choices, default=ReviewRecomendation.NO_OPINION)

    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="reviews")
    critic = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews")
