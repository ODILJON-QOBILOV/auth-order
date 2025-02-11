from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Order, Product
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer, UserProfileSerializer, \
    UserProfileUpdateSerializer, UserPutPatchSerializer, ChangePasswordSerializer, LastOrdersSerializer, \
    RecentOrdersSerializer, TopProductSerializer, ProductsSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics


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
        users = User.objects.all()
        user_data = [{"id": user.id,"username": user.username, "email": user.email, "bio": user.bio} for user in users]
        return Response(user_data)

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
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LastOrdersAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @extend_schema(tags=['orders'])
    def get(self, request):
        # Fetch all orders
        orders = Order.objects.all()

        response = [
            {
                "customer_id": order.customer_id,
                "product_name": order.product.name,
                "date": f"{order.created_at.day} {order.created_at.strftime('%B')} {order.created_at.year}",
                "status": order.status
            }
            for order in orders
        ]
        return Response(response, status=status.HTTP_200_OK)

    @extend_schema(tags=['orders'], request=LastOrdersSerializer)
    def post(self, request):
        serializer = LastOrdersSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecentOrdersAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @extend_schema(tags=['orders'])

    def get(self, request):
        orders = Order.objects.all()
        serializer = RecentOrdersSerializer(orders, many=True)
        # 'created_at', 'price', 'username', 'product_name'
        response = [
            {
                "product_name": order["product_name"],
                "price": order["price"],
                "username": order["username"],
                "created_at": f"{order['created_at'].split('T')[0]}",
            }
            for order in serializer.data
        ]
        return Response(response, status=status.HTTP_200_OK)


class TopSoldProductsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        top_products = (
            Product.objects
            .annotate(total_sold=Sum('order__amount'))
            .order_by('-total_sold')[:3]
        )
        serializer = TopProductSerializer(top_products, many=True)
        return Response(serializer.data)

class BarChartGetAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        db_user = User.objects.get(id=user.id)
        return Response({"data": db_user.statistics})
        # return Response({"message": "you are not authorized"})

@extend_schema(tags=['products'], request=ProductsSerializer)
class ProductsAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


@extend_schema(tags=['products'], request=ProductsSerializer)
class ProductGetUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer