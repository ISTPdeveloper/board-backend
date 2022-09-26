from urllib import request
from django.db import models
from accounts.models import User

from core.models.base import BaseModel
from posts.models import Post


class Comment(BaseModel):
    content = models.TextField
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
