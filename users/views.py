from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer, UserProfileSerializer, \
    UserProfileUpdateSerializer, UserPutPatchSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample


class RootAPIView(APIView):
    @extend_schema(tags=['root'])
    def get(self, request):
        response = {
            "Registration page": "register/",
            "Login page": "login/",
            "Refresh token page": "token/refresh",
            "Profile page": "profile/"
        }
        return Response(response)

class RegisterAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=RegisterSerializer,
        examples=[
            OpenApiExample(
                name="Example of Request",
                value={
                    'username': 'Jhon',
                    'email': 'example@gmail.com',
                    'password': 'qwertyuiop'
                },
                description="Example of a user registration request"
            )
        ]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                name="Example of Login Request",
                value={
                    'username': 'Jhon',
                    'password': 'qwertyuiop'
                },
                description="Example of a user login request"
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return Response({"error": "User account is inactive."}, status=status.HTTP_401_UNAUTHORIZED)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=RefreshTokenSerializer,
        examples=[
            OpenApiExample(
                name="Example of Refresh Access Token Request",
                value={
                    'refresh': "asdfgtresdcvbnjytrdfbhjyw4567uythgfd"
                },
                description="Example of a user get another access token request"
            )
        ]
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUsersAPIView(APIView):
    @extend_schema(tags=['users'])
    def get(self, request):
        if request.user.username == 'admin' or request.user.username == 'mars':
            users = User.objects.all()
            user_data = [{"id": user.id,"username": user.username, "email": user.email, "bio": user.bio} for user in users]
            return Response(user_data)
        return Response({"error": "You are not authorized as admin."}, status=403)

class ProfileAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    @extend_schema(
        tags=["User Profile"],
        request=UserProfileSerializer,
    )
    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileUpdateAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileUpdateSerializer

    @extend_schema(
        tags=["User Profile"],
        request=RefreshTokenSerializer,
        examples=[
            OpenApiExample(
                name="Example of Update Request",
                value={
                    'bio': "here will be user's bio"
                },
                description="Example of a user's bio request"
            )
        ]
    )
    def post(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfilePutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @extend_schema(
        tags=["User Profile"],
        request=UserPutPatchSerializer,
        # examples=[
        #     OpenApiExample(
        #         name="Example of Put and Patch Request",
        #         value={
        #             'username': '',
        #             'bio': ''
        #         },
        #         description="Example of a user's bio request"
        #     )
        # ]
    )
    def put(self, request):
        user = request.user
        serializer = UserPutPatchSerializer(user,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @extend_schema(request=ChangePasswordSerializer, tags=['auth'])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Save the new password if everything is valid
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)