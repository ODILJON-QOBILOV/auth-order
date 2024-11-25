from django.urls import path

from users.views import RegisterAPIView, Test, LoginAPIView, RefreshTokenAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/refresh/', RefreshTokenAPIView.as_view()),
    path('test/', Test.as_view())
]