from .models import SourceChannel, TargetChannel
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SourceChannel, TargetChannel
from .tasks import (  # noqa
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
