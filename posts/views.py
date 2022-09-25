from unicodedata import category
from django.shortcuts import render
from rest_framework import generics

# from core.paginations import PostPageNumberPagination
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter


class PostAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["title", "content", "author__nickname"]
    # pagination_class = PostPageNumberPagination

    def get_queryset(self):
        queryset = Post.objects.filter(status="public").order_by("-created_at")
        category = self.request.query_params.get("category", None)
        if category is not None:
            queryset = Post.objects.filter(category=category, status="public").order_by(
                "-created_at"
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
