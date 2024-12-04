from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_url(value: str) -> None:
    """Validate URL."""
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ["t.me", "www.t.me"]:
        raise ValidationError("URL is not from Telegram.")
