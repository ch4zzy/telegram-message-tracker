import re
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_url(value: str) -> None:
    """Validate URL."""
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ["t.me", "www.t.me"]:
        raise ValidationError("URL is not from Telegram.")


def validate_status_200(value: str) -> None:
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
    if response.status_code == 200:
        pass
    else:
        raise ValidationError("Channel does not exist.")
