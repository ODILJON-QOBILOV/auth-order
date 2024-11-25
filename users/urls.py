from django.urls import path

from users.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, GetUsersAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/refresh/', RefreshTokenAPIView.as_view()),
    path('get-users/', GetUsersAPIView.as_view())
]