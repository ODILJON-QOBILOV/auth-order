from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# class UserRegisterAPIView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         if not username or not email or not password:
#             return Response({'message': 'all 3 columns are required'})
#
#         if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#             return Response({'message': 'User with this username or email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()
#
#         refresh = RefreshToken.for_user(user)
#         access = refresh.access_token
#
#         return Response({
#             'message': 'User Successfully registered!',
#             'refresh_token': str(refresh),
#             'access_token': str(access)
#         }, status=status.HTTP_201_CREATED)
#
#
# class UserLoginAPIView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         # Validate inputs
#         if not username or not password:
#             return Response({'message': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Authenticate user
#         user = authenticate(username=username, password=password)
#         if user is None:
#             return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # Generate tokens
#         refresh = RefreshToken.for_user(user)
#         access = refresh.access_token
#
#         # Return tokens
#         return Response({
#             "message": "You are logged in successfully",
#             "refresh_token": str(refresh),
#             "access_token": str(access)
#         }, status=status.HTTP_202_ACCEPTED)

# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "user": serializer.data,
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh),
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     "access_token": str(refresh.access_token),
#                     "refresh_token": str(refresh)
#                 }, status=status.HTTP_200_OK)
#             return Response({"error": "username or password isn't correct!"}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Password will be hashed here
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
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

#
class RefreshTokenAPIView(APIView):
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUsersAPIView(APIView):
    def get(self, request):
        if request.user.username == 'admin' or request.user.username == 'mars':
            users = User.objects.all()
            user_data = [{"id": user.id,"username": user.username, "email": user.email, "bio": user.bio} for user in users]
            return Response(user_data)
        return Response({"error": "You are not authorized as admin."}, status=403)

# class ProfileAPIView(APIView):
#     permission_classes = (IsAuthenticated, )
#     def get(self, request):
#         user = request.user
#         response = {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email
#         }
#         return Response(response)
#     def post(self, request):


class ProfileAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request):
        # Return the current user's data
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Update the current user's bio and image
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RootAPIView(APIView):
    def get(self, request):
        response = {
            "Registration page": "register/",
            "Login page": "login/",
            "Refresh token page": "token/refresh",
            "Profile page": "profile/"
        }
        return Response(response)