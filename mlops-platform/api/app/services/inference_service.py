from app.services.slack_service import send_slack_notification

# Build slack notification features
def build_and_notifty(
        shipment_id: str,
        image_url: str,
        tabular_output: dict,
        yolo_output: dict,
        rag_output: dict
):
    """
     tabular_outputs example:
    {
        "XGBoost": 0.948,
        "LogisticRegression": 1.0,
        "DecisionTree": 1.0
    }
    """
    
    # --- Model predictions ----
    models_info = {}
    for model, model_name in tabular_output.items():
        decision = "HIGH RISK" if model_name >= 0.5 else "LOW RISK"
        models_info[model] = {
            "risk_probability": model_name,
            "decision": decision
        }

    # --- Model consensus ----
    avg_risk_prob = sum(tabular_output.values()) / len(tabular_output)
    final_decision = "HIGH RISK" if avg_risk_prob >= 0.5 else "LOW RISK"
    consensus_info = {
        "average_risk_probability": avg_risk_prob,
        "final_decision": final_decision
    }
    # --- Build final payload ----
    result = {
        "shipment_id": shipment_id,
        "image": image_url,
        "models": models_info,
        "model_consensus": consensus_info,
        "detection_yolo": yolo_output,
        "RAG_assesment": rag_output
    }
    # --- Send Slack notification ----
    send_slack_notification(result)

    return result