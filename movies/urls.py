from django.urls import path

from . import views

urlpatterns = [
    path("movies/", views.MovieView.as_view()),
    path("movies/<int:movies_id>/", views.MovieViewDetail.as_view()),
]
