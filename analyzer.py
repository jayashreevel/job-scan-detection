import re
import whois
from datetime import datetime

SCAM_WORDS = [
    "registration fee", "pay upfront", "whatsapp interview",
    "no interview", "easy money", "telegram"
]

def check_keywords(text):
    score = 0
    found = []
    for word in SCAM_WORDS:
        if word in text.lower():
            score += 2
            found.append(word)
    return score, found

def domain_age_check(url):
    try:
        domain = re.sub(r"https?://", "", url).split("/")[0]
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        age = (datetime.now() - creation).days
        return age < 180
    except:
        return True
