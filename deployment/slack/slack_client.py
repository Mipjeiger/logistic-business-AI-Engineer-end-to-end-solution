import requests
from .config import SLACK_WEBHOOK_URL


def send_message(payload: dict):

    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL is not set")

    response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)

    return response.status_code
