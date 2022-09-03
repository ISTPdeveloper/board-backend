from django.shortcuts import render
from rest_framework import generics
from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.response import Response


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

            return Response(
                data={"access": access_token, "refresh": refresh_token},
                status=201,
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

            return Response(
                data={"access": access_token, "refresh": refresh_token},
                status=200,
            )


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get("refresh"))
            print(request.data.get("refresh"))
            token.blacklist()
            return Response(
                status=204,
            )

        except Exception as e:
            return Response({"message": "이미 로그아웃 되었어요."}, status=400)


class CustomTokenVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            data={"id": user.id, "nickname": user.nickname, "photo": user.photo.url},
            status=200,
        )


class ProfileDetailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        return Response(
            data=UserSerializer(user, context=self.get_serializer_context()).data,
            status=200,
        )
