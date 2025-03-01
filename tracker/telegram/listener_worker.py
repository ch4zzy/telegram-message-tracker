import pickle

import redis
from django.conf import settings
from telethon.sync import TelegramClient

from tracker.telegram.telethon_client import TelethonClient


class LastMessageTracker:
    def __init__(self):
        self.redis_client = redis.Redis(host="redis", port=6379, db=1)

    def get_last_message_time(self, user_id, channel):
        data = self.redis_client.get(f"last_message_time:{user_id}:{channel}")
        return pickle.loads(data) if data else None

    def set_last_message_time(self, user_id, channel, date):
        self.redis_client.set(
            f"last_message_time:{user_id}:{channel}", pickle.dumps(date)
        )

    def get_all_last_message_time(self):
        keys = self.redis_client.keys("last_message_time:*")
        return {
            key.decode().split(":")[2]: pickle.loads(
                self.redis_client.get(key)
            )
            for key in keys
        }


telethon_client = TelethonClient(
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    session=settings.TELEGRAM_SESSION,
)

telethon_client.set_client()

message_tracker = LastMessageTracker()


def get_active_channels():
    from tracker.models import SourceChannel

    return list(
        SourceChannel.objects.all()
        .filter(active_following=True, verified_status=True)
        .values_list("source_link", "user_id")
    )


def save_post(channel, message, user):
    from tracker.models import Post, SourceChannel

    post = Post.objects.create(
        channel=SourceChannel.objects.get(source_link=channel, user=user),
        content=message.message,
    )
    post.save()


def fetch_new_posts(
    client: TelegramClient, channel: str, last_time: str, user
):
    if last_time is None:
        for message in client.iter_messages(channel, limit=1):
            message_tracker.set_last_message_time(
                user.id, channel, message.date
            )
    else:
        for message in client.iter_messages(
            channel, offset_date=last_time, reverse=True
        ):
            if message.date > last_time:
                message_tracker.set_last_message_time(
                    user.id, channel, message.date
                )
                save_post(channel, message, user)
