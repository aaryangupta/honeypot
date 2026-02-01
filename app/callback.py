import requests

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(session_id: str, session: dict):
    payload = {
        "sessionId": session_id,
        "scamDetected": session["scam_detected"],
        "totalMessagesExchanged": session["total_messages"],
        "extractedIntelligence": {
            "bankAccounts": session["intelligence"]["bankAccounts"],
            "upiIds": session["intelligence"]["upiIds"],
            "phishingLinks": session["intelligence"]["phishingLinks"],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        },
        "agentNotes": "Automated agent engagement completed"
    }

    try:
        requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
    except Exception:
        # Never crash main API
        pass
