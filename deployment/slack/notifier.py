"""Notification Logic (Core Applied ML Layer) for business use-case via Slack."""

from slack.thresholds import THRESHOLD_VERSION
from .slack_client import send_message


def send_alert(
    shipment_id: str,
    severity_score: float,
    alert_level: str,
    class_name: str,
    damage_counts: dict,
    sop_recommendation: str,
    image_name: str,
):

    # -----------------------
    # Emoji mapping
    # -----------------------

    emoji_map = {"CRITICAL": "🚨", "WARNING": "⚠️", "INFO": "ℹ️"}
    emoji = emoji_map.get(alert_level, "🔎")

    # -----------------------
    # Detection summary text
    # -----------------------

    # Create text summary if damage_counts (example: "rust: 2, dent: 1")
    summary_text = ", ".join([f"{k}: {v}" for k, v in damage_counts.items()])
    if not summary_text:
        summary_text = "No damages detected."

    # -----------------------
    # Slack Block Payload
    # -----------------------

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Container Damage Alert: {alert_level}",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Shipment ID:*\n`{shipment_id}`"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity Score:*\n`{severity_score:.4f}`",
                    },
                ],
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Detections Summary:*\n{summary_text}",
                    },
                    {"type": "mrkdwn", "text": f"*File Name:*\n{image_name}"},
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📋 SOP Recommendation:*\n{sop_recommendation}",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Model: YOLOv8 + Severity Engine | Threshold: {THRESHOLD_VERSION}",
                    }
                ],
            },
        ]
    }

    return send_message(payload)
