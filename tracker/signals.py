from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, SourceChannel, TargetChannel
from .tasks import (  # noqa
    post_message_task,
    validate_admin_bot_task,
    validate_link_task,
)


@receiver(post_save, sender=SourceChannel)
@receiver(post_save, sender=TargetChannel)
def channel_verification_signal(sender, instance, created, **kwargs):
    if created:
        validate_link_task.delay(instance.id, sender.__name__)


@receiver(post_save, sender=TargetChannel)
def admin_verification_signal(sender, instance, created, **kwargs):
    if not created and instance.admin_status is False:
        validate_admin_bot_task.delay(instance.id)


@receiver(post_save, sender=Post)
def post_message_signal(sender, instance, created, **kwargs):
    if created and instance.status == "pending":
        target_channels = instance.channel.target_channel.filter(
            auto_post=True, verified_status=True, admin_status=True
        )
        if target_channels.exists():
            post_message_task.delay(instance.id)
