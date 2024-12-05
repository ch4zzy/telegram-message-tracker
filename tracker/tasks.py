from core.celery import app
from tracker.validators import validate_status_200


@app.task
def async_validate_status_200(value) -> None:
    validate_status_200(value)
    return None
