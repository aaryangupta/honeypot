import re

# Keyword buckets (edit carefully)
URGENCY_WORDS = [
    "urgent", "immediately", "blocked", "suspended", "last warning"
]

AUTHORITY_WORDS = [
    "bank", "customer care", "support", "rbi", "kyc"
]

ACTION_WORDS = [
    "verify", "update", "share", "send", "confirm", "click"
]

FINANCIAL_WORDS = [
    "upi", "account", "otp", "pin", "card"
]


def score_message(text: str) -> int:
    text = text.lower()
    score = 0

    if any(word in text for word in URGENCY_WORDS):
        score += 1

    if any(word in text for word in AUTHORITY_WORDS):
        score += 1

    if any(word in text for word in ACTION_WORDS):
        score += 1

    if any(word in text for word in FINANCIAL_WORDS):
        score += 1

    return score
