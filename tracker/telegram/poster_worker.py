from asgiref.sync import sync_to_async
from django.conf import settings

from tracker.telegram.telethon_client import TelethonClient

telethon_client = TelethonClient(
    api_id=settings.API_BOT_ID,
    api_hash=settings.API_BOT_HASH,
    session=settings.BOT_TELEGRAM_SESSION,
)

telethon_client.set_client()


@sync_to_async
def get_post(post_id: int) -> None:
    from tracker.models import Post

    return Post.objects.get(id=post_id)


@sync_to_async
def save_post(post) -> None:
    post.status = "posted"
    post.save()


@sync_to_async
def get_channels(post: object) -> None:
    return post.channel.target_channel.filter(
        verified_status=True,
        admin_status=True,
    )


async def post_message(client: TelethonClient, post_id: int) -> None:
    post = await get_post(post_id)
    channels = await get_channels(post)

    async for channel in channels:
        await client.send_message(channel.source_link, post.content)

    await save_post(post)
