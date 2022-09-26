from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User
from config.settings.base import DEFAULT_PROFILE_IMAGE
from core.redis_connection import RedisConnection


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password1": {"write_only": True}}

    try:

        def validate(self, data):
            self.rd = RedisConnection()
            auth = self.rd.conn.hgetall(data["phone_number"])
            if not auth:
                raise serializers.ValidationError({"phone_number": "휴대폰 인증이 필요해요"})
            is_verified = auth["is_verified"]
            if is_verified != str(1):
                raise serializers.ValidationError({"phone_number": "인증이 완료되지 않았어요"})
            if data["photo"] is None:
                data["photo"] = DEFAULT_PROFILE_IMAGE
            return data

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data["username"],
                password=validated_data["password"],
                name=validated_data["name"],
                nickname=validated_data["nickname"],
                phone_number=validated_data["phone_number"],
                photo=validated_data["photo"],
                is_verified=1,
            )
            print(user)
            return user

    except:
        raise serializers.ValidationError("일시적인 오류가 발생했어요")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            user.last_login = datetime.now()
            user.save()
            return user
        raise serializers.ValidationError("아이디 혹은 비밀번호가 일치하지 않아요")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
