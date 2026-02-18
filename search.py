import re

def google_search(text):
    """
    Offline heuristic-based search simulation
    (Safe for cloud deployment)
    """

    text = text.lower()

    suspicious_signals = [
        "telegram",
        "whatsapp only",
        "pay registration",
        "no interview",
        "quick money",
        "limited slots",
        "dm me",
        "processing fee"
    ]

    found = []
    for word in suspicious_signals:
        if word in text:
            found.append(word)

    if found:
        return {
            "risk": "High",
            "signals": found
        }
    else:
        return {
            "risk": "Low",
            "signals": []
        }
