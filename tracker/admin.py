from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Post, SourceChannel, TargetChannel, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(TargetChannel)
class TargetChannelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "source_link",
        "created_at",
        "auto_post",
        "verified_status",
        "admin_status",
    )
    search_fields = ("name", "source_link")
    list_filter = ("auto_post",)


@admin.register(SourceChannel)
class SourceChannelAdmin(admin.ModelAdmin):
    from .forms import SourceChannelForm

    form = SourceChannelForm
    list_display = (
        "name",
        "source_link",
        "created_at",
        "active_following",
        "verified_status",
    )
    search_fields = ("name", "source_link")
    list_filter = ("active_following",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("channel", "created_at", "edited_at", "status")
    search_fields = ("title", "source_channel")
    list_filter = ("status",)
