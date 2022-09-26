from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from comments.views import CommentAPIView

app_name = "comments"
urlpatterns = [
    path("comment/", CommentAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
