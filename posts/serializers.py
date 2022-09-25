from accounts.serializers import UserSerializer
from posts.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
