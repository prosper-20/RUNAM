from django.urls import path
from .views import APIRegisterView, ConfirmEmailView, UserLoginAPIView, UserLogoutAPIView, UserAPIView, UserAvatarAPIView, UserProfileAPIView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", APIRegisterView.as_view(), name="register-user"),
    path('confirm-email/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("", UserAPIView.as_view(), name="user-info"),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path("profile/avatar/", UserAvatarAPIView.as_view(), name="user-avatar"),
    path("password-change/", ChangePasswordView.as_view(), name="change-password"),
]