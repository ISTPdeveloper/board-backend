import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일자")

    class Meta:
        abstract = True
