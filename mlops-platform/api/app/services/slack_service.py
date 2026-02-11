import requests
from app.config import settings


# Create a fuction for slack service to send notifications
def send_slack_notification(result: dict):
    if not settings.SLACK_WEBHOOK_URL:
        return 
    
    models = result['models']
    consensus = result['model_consensus']
    yolo = result['detection_yolo']
    rag = result['RAG_assesment']

    model_lines = []
    for name, info in models.items():
        model_lines.append(
            f"• *{name}*: {info['risk_probability']:.3f} → `{info['decision']}`"
        )

    slack_payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 HIGH RISK SHIPMENT DETECTED",
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*📦 Image*\n{result['image']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Shipment ID*\n{result['shipment_id']}",
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*🧠 Model Predictions*\n" + "\n".join(model_lines),
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": (
                            "*📊 Model Consensus*\n"
                            f"Average Risk Probability: *{consensus['average_risk_probability']:.3f}*\n"
                            f"Final Decision: `{consensus['final_decision']}`"
                        ),
                    }
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": (
                            "*👁️ Visual Damage Detection (YOLO)*\n"
                            f"Damage Detected: *{yolo['damage_detected']}*\n"
                            f"Confidence: *{yolo['confidence']}*\n"
                            f"Bounding Boxes: *{yolo['bbox_count']}*\n"
                            f"Classes: `{', '.join(yolo['classes'])}`"
                        ),
                    }
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "*🧠 RAG Assessment*\n"
                        f"> {rag['summary']}\n\n"
                        f"*🚫 Recommendation:* `{rag['recommendation']}`"
                    ),
                },
            },
        ]
    }

    requests.post(settings.SLACK_WEBHOOK_URL, json=slack_payload, timeout=5)