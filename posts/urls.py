from django.urls import path

from posts.views import PostAPIView, PostDetailAPIView
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "post"
urlpatterns = [
    path("post/", PostAPIView.as_view(), name="게시판"),
    path("post/<str:pk>/", PostDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
