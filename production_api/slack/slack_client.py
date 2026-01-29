import requests
from .config import SLACK_WEBHOOK_URL, SLACK_CHANNEL, SLACK_USERNAME


def send_slack_message(text: str):

    payload = {"username": SLACK_USERNAME, "channel": SLACK_CHANNEL, "text": text}

    response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)

    if response.status_code != 200:
        raise Exception(f"Slack error: {response.status_code}, {response.text}")
