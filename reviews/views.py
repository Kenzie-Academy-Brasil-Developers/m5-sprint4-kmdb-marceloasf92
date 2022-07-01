from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from movies.models import Movie

from .models import Review
from .serializers import ReviewSerializer


class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewViewDetail(APIView):
    #Somente admin ou próprio crítico que fez a review
    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieReviewViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, movie_id):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(critic=request.user, movie_id=movie_id)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, movie_id):
        try:
            reviews = Review.objects.get(pk=movie_id)
            serializer = ReviewSerializer(reviews)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response({"message": "Review not found."}, status.HTTP_404_NOT_FOUND)

    


