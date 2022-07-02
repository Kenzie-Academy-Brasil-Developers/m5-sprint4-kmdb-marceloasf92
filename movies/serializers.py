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

        movie = Movie.objects.create(**validated_data)

        for only_genre in genre_data:
            genres = Genre.objects.get_or_create(
                **only_genre)[0]
            movie.genres.add(genres)

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        genres = validated_data.pop('genres', None)
        if genres:
            genres_list = []
            for genre in genres:
                genre, _ = Genre.objects.get_or_create(**genre)
                genres_list.append(genre)
            instance.genres.add(*genres_list)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
