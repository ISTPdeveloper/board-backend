from unicodedata import name
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User
from posts.models import Post


class UserAdmin(BaseUserAdmin):
    ordering = ["created_at"]
    list_display = [
        "username",
        "name",
        "nickname",
        "phone_number",
        "is_verified",
        "created_at",
        "last_login",
    ]
    fieldsets = (
        (("회원정보"), {"fields": ("username",)}),
        (
            ("개인정보"),
            {
                "fields": (
                    "name",
                    "nickname",
                    ("phone_number", "is_verified"),
                    "photo",
                ),
            },
        ),
        (
            ("권한"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (("시간"), {"classes": ("collapse",), "fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            ("회원정보"),
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            ("개인정보"),
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "nickname",
                    ("phone_number", "is_verified"),
                    "photo",
                ),
            },
        ),
        (
            ("권한"),
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("id", "username", "name", "nickname", "phone_number")
    list_filter = ("is_verified", "is_active", "is_staff", "is_superuser")


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    ordering = ["created_at"]
    list_display = [
        "title",
        "content",
        "category",
        "status",
        "created_at",
        "author",
    ]
    fieldsets = (
        (
            ("게시물 작성"),
            {
                "fields": (
                    "title",
                    "content",
                    "photo",
                    "category",
                )
            },
        ),
        (("공개 / 비공개"), {"fields": ("status",)}),
    )

    search_fields = (
        "title",
        "content",
    )
    list_filter = (
        "category",
        "status",
    )


admin.site.register(Post, PostAdmin)
