from django.core.exceptions import ValidationError

from core.celery import app
from tracker.validators import validate_admin_bot, validate_channel_exists


@app.task(queue="management")
def validate_link_task(instance_id: int, model_name: str) -> None:
    from .models import SourceChannel, TargetChannel

    Model = SourceChannel if model_name == "SourceChannel" else TargetChannel
    instance = Model.objects.get(id=instance_id)

    try:
        validate_channel_exists(instance.source_link)
        instance.verified_status = True
    except ValidationError:
        instance.verified_status = False

    instance.save()


@app.task(queue="management")
def validate_admin_bot_task(instance_id: int) -> None:
    from .models import TargetChannel

    instance = TargetChannel.objects.get(id=instance_id)

    try:
        validate_admin_bot(instance.source_link)
        instance.admin_status = True
    except ValidationError:
        instance.admin_status = False

    instance.save()
