from rest_framework import serializers


class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    stars = serializers.IntegerField()
    review = serializers.CharField()
    spoilers = serializers.BooleanField(default=False)
    recomendation = serializers.CharField(max_length=50)
