from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            return JsonResponse(
                {
                    "status": "SUCCESS",
                    "message": f"{user.name}님 환영해요🎈",
                    "result": {
                        "user": UserSerializer(
                            user, context=self.get_serializer_context()
                        ).data,
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=200,
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data

            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            return JsonResponse(
                {
                    "status": "SUCCESS",
                    "message": "로그인에 성공했어요",
                    "result": {
                        "user": UserSerializer(
                            user, context=self.get_serializer_context()
                        ).data,
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=200,
            )


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()
        return JsonResponse(
            {
                "status": "SUCCESS",
                "message": "다음에 또 만나요ㅠㅠ",
                "result": "",
            },
            status=200,
        )


class CustomTokenVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return JsonResponse(
            {
                "status": "SUCCESS",
                "message": "",
                "result": {
                    "id": user.id,
                    "nickname": user.nickname,
                    "photo": user.photo.url,
                },
            },
            status=200,
        )


class ProfileDetailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        return JsonResponse(
            {
                "status": "SUCCESS",
                "message": "",
                "result": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            },
            status=200,
        )
