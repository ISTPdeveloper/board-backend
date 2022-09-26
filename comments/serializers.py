from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author"]

    def get_reply(self, instance):
        serializer = self.__class__(instance.parent, many=True)
        serializer.bind("", self)
        return serializer.data
