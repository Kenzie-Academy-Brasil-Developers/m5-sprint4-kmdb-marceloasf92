from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from users.permissions import IsAdminOrCritic

from .models import Review
from .serializers import ReviewSerializer


class ReviewView(APIView, PageNumberPagination):
    def get(self, request):
        reviews = Review.objects.all()
        result_page = self.paginate_queryset(reviews, request, self)
        serializer = ReviewSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class ReviewViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCritic]
    # Somente admin ou próprio crítico que fez a review

    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieReviewViewDetail(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, movie_id):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(critic=request.user, movie_id=movie_id)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, movie_id):
        try:
            reviews = Review.objects.filter(movie_id=movie_id)
            result_page = self.paginate_queryset(reviews, request, self)
            serializer = ReviewSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)
        except Review.DoesNotExist:
            return Response({"message": "Review not found."}, status.HTTP_404_NOT_FOUND)
