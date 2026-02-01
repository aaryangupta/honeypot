import re

UPI_REGEX = re.compile(r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b")
BANK_REGEX = re.compile(r"\b\d{9,18}\b")
URL_REGEX = re.compile(r"https?://\S+")


def extract_intelligence(text: str) -> dict:
    return {
        "upiIds": list(set(UPI_REGEX.findall(text))),
        "bankAccounts": list(set(BANK_REGEX.findall(text))),
        "phishingLinks": list(set(URL_REGEX.findall(text))),
    }
