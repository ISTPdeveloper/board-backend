from django.urls import path

from posts.views import PostAPIView, PostByUserAPIView, PostDetailAPIView
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "post"
urlpatterns = [
    path("post/", PostAPIView.as_view(), name="게시판"),
    path("post/my/", PostByUserAPIView.as_view()),
    path("post/<str:pk>/", PostDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
