from rest_framework import serializers

from genres.serializers import GenreSerializer

from genres.models import Genre
from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=127)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict):
        genre_data = validated_data.pop("genres")

        # genre = Genre.objects.get_or_create(**genre_data)[0]

        movie = Movie.objects.create(**validated_data)

        for only_charac in genre_data:
            genres = Genre.objects.get_or_create(
                **only_charac)[0]
            movie.genres.add(genres)

        return movie
