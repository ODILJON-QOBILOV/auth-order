from django.urls import path

from users.views import UserLoginAPIView, UserRegisterAPIView, RefreshTokenAPIView, GetUsersAPIView, ProfileAPIView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('token/refresh/', RefreshTokenAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('get-users/', GetUsersAPIView.as_view())
]