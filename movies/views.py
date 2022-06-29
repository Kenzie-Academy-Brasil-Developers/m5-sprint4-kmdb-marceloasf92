from django.shortcuts import render

from rest_framework.views import APIView, Response, status

from .models import Movie
from .serializers import MovieSerializer

class MovieView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class MovieViewDetail(APIView):
    def get(self, request, movies_id):
        try:
            movie = Movie.objects.get(pk=movies_id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found."},status.HTTP_404_NOT_FOUND)
