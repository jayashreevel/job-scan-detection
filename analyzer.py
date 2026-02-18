import re
from urllib.parse import urlparse

# Scam keyword list
SCAM_KEYWORDS = [
    "registration fee", "pay fee", "earn money fast",
    "work from home", "limited slots", "urgent hiring",
    "no interview", "instant joining", "whatsapp only"
]

def check_keywords(text):
    text = text.lower()
    score = 0
    found = []

    for word in SCAM_KEYWORDS:
        if word in text:
            score += 2
            found.append(word)

    return score, found

def domain_age_check(url):
    """
    Simple heuristic:
    - Short URLs
    - Free hosting
    - IP-based URLs
    """
    try:
        domain = urlparse(url).netloc.lower()

        suspicious_patterns = [
            "bit.ly", "tinyurl", "blogspot", "wordpress",
            "000webhost", "free", ".xyz", ".tk"
        ]

        if any(p in domain for p in suspicious_patterns):
            return True

        if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
            return True

        return False
    except:
        return True
