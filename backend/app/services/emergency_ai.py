def classify_emergency(text: str) -> str:
    text = text.lower()

    if "not breathing" in text or "collapsed" in text:
        return "CARDIAC_ARREST"
    if "choking" in text:
        return "CHOKING"
    if "bleeding" in text:
        return "SEVERE_BLEEDING"
    
    return "UNKNOWN"


def generate_guidance(emergency_type: str) -> str:
    if emergency_type == "CARDIAC_ARREST":
        return (
            "Call emergency services immediately. "
            "Start chest compressions. "
            "Push hard and fast in the center of the chest."
        )

    if emergency_type == "CHOKING":
        return (
            "Ask if the person can speak. "
            "If not, perform abdominal thrusts."
        )

    return "Please call emergency services immediately."
