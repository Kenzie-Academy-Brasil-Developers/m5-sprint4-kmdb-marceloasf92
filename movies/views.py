from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Movie
from .serializers import MovieSerializer

from users.permissions import IsAdmin


class MovieView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]

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
        except KeyError as err:
            return Response(
                {"message": str(err).replace("'", "")
                 }, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return Response(serializer.data)
