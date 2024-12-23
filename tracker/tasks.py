import asyncio

from django.core.exceptions import ValidationError

from core.celery import app
from tracker.telegram.listener_worker import fetch_new_posts
from tracker.telegram.poster_worker import post_message
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


@app.task(queue="listener")
def fetch_new_posts_task() -> None:
    from tracker.telegram.listener_worker import telethon_client

    client = telethon_client.get_client()
    loop = telethon_client.get_loop()
    if loop.is_running():
        asyncio.create_task(fetch_new_posts(client))
    else:
        loop.run_until_complete(fetch_new_posts(client))


@app.task(queue="poster")
def post_message_task(post_id) -> None:
    from tracker.telegram.poster_worker import telethon_client

    client = telethon_client.get_client()
    loop = telethon_client.get_loop()
    if loop.is_running():
        asyncio.create_task(post_message(client, post_id))
    else:
        loop.run_until_complete(post_message(client, post_id))
