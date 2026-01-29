"""Notification Logic (Core Applied ML Layer)"""

from .thresholds import THRESHOLDS
from .slack_client import send_slack_message


# Create function to check computed severity against thresholds
def compute_severity(confidence, bbox_area_ratio):
    """Compute severity score based on confidence config and bounding box area ratio object size."""
    return round(confidence * bbox_area_ratio, 3)


# Create function to should notify based on thresholds severity score
def should_notify(label, severity_score):

    if label not in THRESHOLDS:
        return False

    rule = THRESHOLDS[label]

    min_v = rule["min"]
    max_v = rule["max"]

    return min_v < severity_score < max_v


# Create function to notify via Slack
def notify_slack(
    image_name,
    label,
    confidence,
    bbox_area_ratio,
):

    # Compute severity score
    severity = compute_severity(confidence=confidence, bbox_area_ratio=bbox_area_ratio)
    if should_notify(label, severity):
        message = f"""
        🚨 *Inspection Alert*

        Image: '{image_name}'
        Defect: *{label}*
        Confidence: '{confidence:.2f}'
        Area Ratio: '{bbox_area_ratio:.3f}'
        Severity Score: *{severity}*

        Action Required ⚠️
        """

        send_slack_message(message)
        return True

    return False
