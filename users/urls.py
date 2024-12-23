from django.urls import path

from users.views import RefreshTokenAPIView, GetUsersAPIView, ProfileAPIView, RegisterAPIView, LoginAPIView, \
    RootAPIView, ProfileUpdateAPIView, ProfilePutAPIView, ChangePasswordAPIView, LastOrdersAPIView, RecentOrdersAPIView, \
    TopSoldProductsAPIView, BarChartGetAPIView

urlpatterns = [
    path('', RootAPIView.as_view()),
    path('get-users/', GetUsersAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/refresh/', RefreshTokenAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('profile/update/', ProfileUpdateAPIView.as_view()),
    path('profile/put/', ProfilePutAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('last-orders/', LastOrdersAPIView.as_view()),
    path('recent-orders/', RecentOrdersAPIView.as_view()),
    path('top-products/', TopSoldProductsAPIView.as_view()),
    path('chart/', BarChartGetAPIView.as_view()),
]