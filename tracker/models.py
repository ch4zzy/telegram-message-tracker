from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_url


class User(AbstractUser):
    """Custom user model."""


class TargetChannel(models.Model):
    """
    Target channel model.
    Used to store the target channel information.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="target_channels"
    )
    name = models.CharField(max_length=16)
    source_link = models.URLField(
        max_length=128, unique=True, validators=[validate_url]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    auto_post = models.BooleanField(default=False)

    def __str__(self):
        return f"Target -> {self.name}"


class SourceChannel(models.Model):
    """
    Source channel model.
    Used to store the source channel information.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="source_channels"
    )
    target_channel = models.ManyToManyField(
        TargetChannel, related_name="source_channels"
    )
    name = models.CharField(max_length=16)
    source_link = models.URLField(
        max_length=128, unique=True, validators=[validate_url]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    active_following = models.BooleanField(default=True)

    def __str__(self):
        return f"Source -> {self.name}"


class Post(models.Model):
    """Message model."""

    channel = models.ForeignKey(
        SourceChannel, on_delete=models.CASCADE, related_name="messages"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("posted", "Posted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"{self.channel.user} -> {self.channel}"
