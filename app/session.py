from datetime import datetime

SESSIONS = {}


def get_or_create_session(session_id: str):
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "messages": [],
            "start_time": datetime.utcnow(),
            "total_messages": 0,
            "risk_score": 0,
            "agent_turns": 0,
            "final_report_sent": False,
            "scam_detected": False,
            "agent_active": False,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": []
            }
        }
    return SESSIONS[session_id]
