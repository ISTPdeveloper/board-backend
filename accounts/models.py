from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from config.settings.base import DEFAULT_PROFILE_IMAGE

from core.models.base import BaseModel
from core.s3_options import profile_image_path
from core.validations import (
    name_validate,
    password_validate,
    phone_number_validate,
    username_validate,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None, **extra_fields):
        superuser = self.create_user(
            username=username, password=password, **extra_fields
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        validators=[username_validate],
        verbose_name="아이디",
    )
    password = models.CharField(
        max_length=255, validators=[password_validate], verbose_name="비밀번호"
    )
    name = models.CharField(max_length=4, validators=[name_validate], verbose_name="이름")
    nickname = models.CharField(max_length=12, default="익명", verbose_name="별명")
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=False,
        blank=False,
        validators=[phone_number_validate],
        verbose_name="전화번호",
    )
    photo = models.FileField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        verbose_name="사진",
        default=DEFAULT_PROFILE_IMAGE,
    )
    is_verified = models.BooleanField(default=False, verbose_name="문자인증 유무")
    is_superuser = models.BooleanField(default=False, verbose_name="관리자 권한 유무")
    is_staff = models.BooleanField(default=False, verbose_name="매니저 권한 유무")
    is_active = models.BooleanField(default=True, verbose_name="계정 활성화 유무")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="마지막 로그인한 시간")
    email = None
    date_joined = None
    first_name = None
    last_name = None

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "nickname", "phone_number"]

    class Meta:
        db_table = "user"
        ordering = ["created_at"]
        verbose_name = "회원"
        verbose_name_plural = "게시판 회원"

    def __str__(self):
        return str(self.id)

    is_verified.boolean = True
