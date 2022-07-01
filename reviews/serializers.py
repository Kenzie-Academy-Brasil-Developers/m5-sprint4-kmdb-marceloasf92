from dataclasses import fields
from rest_framework import serializers

from .models import Review
from users.serializers import CriticSerializer


# class ReviewSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     stars = serializers.IntegerField()
#     review = serializers.CharField()
#     spoilers = serializers.BooleanField(default=False)
#     recomendation = serializers.CharField(max_length=50)

class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "stars", "review", "spoilers", "recomendation", "critic", "movie_id"]
        read_only_fields = ['id']

    def create(self, validated_data: dict) -> Review:
        return Review.objects.create(**validated_data)

    
