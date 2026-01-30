"""
- Retrieve YOLO inference
- Mapping class -> severity score
- Compare severity score against thresholds
- Auto sent Slack notification if thresholds qualified
"""

"""
Threshold configuration for Logistic-RAG Alert Engine
"""

THRESHOLD_VERSION = "v1.0.0"

THRESHOLDS = {"low": 0.447, "medium": 0.588, "high": 0.740}

CLASS_WEIGHT = {"dent": 1.0, "rust": 1.2, "leak": 1.5, "broken_door": 1.7}

ALERT_POLICY = {"send_info": False, "send_warning": True, "send_critical": True}


# Create function to get classify alert level based on severity score
def classify_alert(score: float):
    """Classify alert level based on severity score"""
    if score >= THRESHOLDS["high"]:
        return "CRITICAL"
    elif score >= THRESHOLDS["medium"]:
        return "WARNING"
    elif score >= THRESHOLDS["low"]:
        return "INFO"
    else:
        return None


def apply_class_weight(score: float, class_name: str):
    """Apply class weight to severity score"""
    weight = CLASS_WEIGHT.get(class_name, 1.0)
    return score * weight
