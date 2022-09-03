from django.urls import path
from accounts.views import (
    CustomTokenVerifyView,
    LoginAPIView,
    LogoutAPIView,
    ProfileDetailView,
    RegisterAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="회원가입"),
    path("login/", LoginAPIView.as_view(), name="로그인"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refreshToken 발급"),
    path("logout/", LogoutAPIView.as_view(), name="로그아웃"),
    path("auth/", CustomTokenVerifyView.as_view(), name="토큰 검증"),
    path("profile/", ProfileDetailView.as_view(), name="회원 정보"),
]
