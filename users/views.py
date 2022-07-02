from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from users.serializers import LoginSerializer, RegisterSerializer

from users.models import User

from users.permissions import IsAdmin


class UserView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        user = User.objects.all()
        result_page = self.paginate_queryset(user, request, self)
        serializer = RegisterSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class UserViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            movie = User.objects.get(pk=user_id)
            serializer = RegisterSerializer(movie)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            # token = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response(
            {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
        )
