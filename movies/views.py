from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from .models import Movie
from .serializers import MovieSerializer

from users.permissions import IsAdminOrReadyOnly


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadyOnly]

    def get(self, request):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadyOnly]

    def get(self, request, movies_id):
        try:
            movie = Movie.objects.get(pk=movies_id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, movies_id):
        movie = get_object_or_404(Movie, pk=movies_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, movies_id):
        movie = get_object_or_404(Movie, pk=movies_id)

        serializer = MovieSerializer(movie, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except KeyError:
            return Response(
                KeyError, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return Response(serializer.data)
