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
    search_fields = ["title", "content"]
    # pagination_class = PostPageNumberPagination

    def get_queryset(self):
        queryset = Post.objects.filter(status="public").order_by("-created_at")
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def list(self, request):
    #     queryset = self.set_filters(self.get_queryset(), request)

    #     serializer = self.get_serializer(queryset, many=True)

    #     return Response(serializer.data)

    # def list(self, request):
    #     if "category" in request.GET:
    #         category = request.GET.get("category", None)
    #         queryset = Post.objects.filter(category=category, status="public").order_by(
    #             "-created_at"
    #         )
    #     else:
    #         queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def set_filters(self, queryset, request):
    #     category = request.query_params.get("category", None)
    #     title = request.query_params.get("title", None)
    #     content = request.query_params.get("description", None)

    #     if category is not None:
    #         queryset = queryset.filter(category=category)

    #     if title is not None:
    #         queryset = queryset.filter(title=title)

    #     if content is not None:
    #         queryset = queryset.filter(content=content)

    #     return queryset


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
