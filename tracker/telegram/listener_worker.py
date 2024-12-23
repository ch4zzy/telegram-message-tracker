from asgiref.sync import sync_to_async
from django.conf import settings
from telethon.sync import TelegramClient

from tracker.telegram.telethon_client import TelethonClient


class LastMessageTracker:
    def __init__(self):
        self._last_message_time = {}

    def initialize(self, channels):
        self._last_message_time = {channel: None for channel in channels}

    def update(self, channels):
        existing_channels = set(self._last_message_time.keys())
        current_channels = set(channels)

        for channel in current_channels - existing_channels:
            self._last_message_time[channel] = None

        for channel in existing_channels - current_channels:
            del self._last_message_time[channel]

    def get_last_message_time(self, channel):
        return self._last_message_time.get(channel)

    def set_last_message_time(self, channel, date):
        self._last_message_time[channel] = date


telethon_client = TelethonClient(
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    session=settings.TELEGRAM_SESSION,
)

telethon_client.set_client()

message_tracker = LastMessageTracker()


@sync_to_async
def get_active_channels():
    from tracker.models import SourceChannel

    return list(
        SourceChannel.objects.all()
        .filter(active_following=True, verified_status=True)
        .values_list("source_link", flat=True)
    )


@sync_to_async
def save_post(channel, message):
    from tracker.models import Post, SourceChannel

    post = Post.objects.create(
        channel=SourceChannel.objects.get(source_link=channel),
        content=message.message,
    )
    post.save()


async def fetch_new_posts(client: TelegramClient):
    channels = await get_active_channels()

    if not message_tracker._last_message_time:
        message_tracker.initialize(channels)

    message_tracker.update(channels)

    for channel in channels:
        last_time = message_tracker.get_last_message_time(channel)
        if last_time is None:
            async for message in client.iter_messages(channel, limit=1):
                message_tracker.set_last_message_time(channel, message.date)
        else:
            async for message in client.iter_messages(
                channel, offset_date=last_time, reverse=True
            ):
                if message.date > last_time:
                    await save_post(channel, message)
                    message_tracker.set_last_message_time(
                        channel, message.date
                    )
