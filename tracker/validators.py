import re
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_url(value: str) -> bool:
    """Validate URL."""
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ["t.me", "www.t.me"]:
        raise ValidationError(
            f"Invalid URL, only t.me allowed. Received: {parsed_url.netloc}"
        )
    return True


def validate_channel_exists(value: str) -> bool:
    """Validate URL and check if it returns 200."""
    token = settings.BOT_TOKEN
    match = re.search(r"t\.me/([a-zA-Z0-9_]+)", value)
    if match:
        channel_username = match.group(1)
    else:
        raise ValidationError("Invalid URL.")

    url = f"https://api.telegram.org/bot{token}/getChat"
    params = {"chat_id": f"@{channel_username}"}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValidationError(f"@{channel_username} is not a valid channel.")
    return True


def validate_admin_bot(value: str) -> bool:
    """
    Validate if the bot is an admin in the channel and can post messages.

    :param value: URL of the channel.
    """
    bot_token = settings.BOT_TOKEN
    match = re.search(r"t\.me/([a-zA-Z0-9_]+)", value)
    if match:
        channel_username = match.group(1)
    else:
        raise ValidationError("Invalid URL.")

    url = f"https://api.telegram.org/bot{bot_token}/getChatMember"

    params = {
        "chat_id": f"@{channel_username}",
        "user_id": bot_token.split(":")[0],
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError(
            f"API returns error: {response.status_code}, {response.text}"
        )

    data = response.json()
    if not data.get("ok", False):
        raise ValueError(
            f"API returns error: {data.get('description', 'Unknown error')}"
        )

    result = data.get("result", {})
    status = result.get("status")
    can_post_messages = result.get("can_post_messages", False)

    if status != "administrator":
        raise ValidationError(f"Bot is not an admin in @{channel_username}.")
    if not can_post_messages:
        raise ValidationError(
            f"Bot can't post messages in @{channel_username}."
        )

    return True


def validate_source_target_unique(
    instance: object, action, pk_set, **kwargs
) -> str:
    """
    Validate if source_link of SourceChannel is unique in TargetChannel.
    """
    from tracker.models import TargetChannel

    if action == "pre_add":
        for target in pk_set:
            if not isinstance(target, int):
                target = target.pk
            target = TargetChannel.objects.get(pk=target)
            if instance.source_link == target.source_link:
                return f"{instance.source_link} not unique,\
                         {target.name} has {target.source_link}"

    return ""
