from django.db import models
from accounts.models import User

from core.models.base import BaseModel
from core.s3_options import content_image_path

POSTS_CATEGORY_CHOICES = [
    ("etc", "etc"),
    ("game", "game"),
    ("develop", "develop"),
    ("study", "study"),
]
POSTS_STATUS_CHOICES = [("public", "public"), ("private", "private")]


class Post(BaseModel):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=255)
    category = models.CharField(
        max_length=30, choices=POSTS_CATEGORY_CHOICES, default="etc"
    )
    status = models.CharField(
        max_length=7, choices=POSTS_STATUS_CHOICES, default="public"
    )
    photo = models.FileField(
        upload_to=content_image_path, null=True, blank=True, verbose_name="사진"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    class Meta:
        db_table = "post"

    def __str__(self):
        return str(self.id)
