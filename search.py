def google_search(text):
    """
    Offline heuristic-based job scam signal checker
    Safe for Render / cloud deployment
    """

    text = text.lower()

    suspicious_signals = [
        "telegram",
        "whatsapp",
        "dm me",
        "pay registration",
        "registration fee",
        "processing fee",
        "no interview",
        "quick money",
        "earn daily",
        "limited slots",
        "work from home",
        "contact immediately",
        "join fast",
        "guaranteed income"
    ]

    detected = []

    for signal in suspicious_signals:
        if signal in text:
            detected.append(signal)

    if detected:
        return {
            "risk": "High",
            "signals": detected
        }
    else:
        return {
            "risk": "Low",
            "signals": []
        }
