"""
- Retrieve YOLO inference
- Mapping class -> severity score
- Compare severity score against thresholds
- Auto sent Slack notification if thresholds qualified
"""

THRESHOLDS = {
    "dent": {
        "min": 0.0,
        "max": 0.8,
    },
    "rust": {
        "min": 0.0,
        "max": 1.0,
    },
    "broken_door": {
        "min": 0.0,
        "max": 0.7,
    },
    "leak": {
        "min": 0.0,
        "max": 2.0,
    },
}
