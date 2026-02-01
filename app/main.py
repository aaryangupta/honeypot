from fastapi import FastAPI, Header, HTTPException
from datetime import datetime

from app.models import IncomingRequest
from app.config import API_KEY
from app.session import get_or_create_session
from app.detection import score_message
from app.llm import llm_confirm_scam_intent
from app.agent import generate_agent_reply
from app.extractors import extract_intelligence
from app.callback import send_final_callback

from app.agent_llm import generate_agent_reply_llm


app = FastAPI(title="Agentic Honeypot API")


@app.post("/api/honeypot/message")
def handle_message(
    payload: IncomingRequest,
    x_api_key: str = Header(None)
):
    # --------------------------------------------------
    # 1. API KEY VALIDATION
    # --------------------------------------------------
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # --------------------------------------------------
    # 2. BASIC VALIDATION
    # --------------------------------------------------
    if payload.message.sender not in ["scammer", "user"]:
        raise HTTPException(status_code=400, detail="Invalid sender")

    if not payload.message.text.strip():
        raise HTTPException(status_code=400, detail="Empty message text")

    # --------------------------------------------------
    # 3. SESSION HANDLING
    # --------------------------------------------------
    session = get_or_create_session(payload.sessionId)

    session["messages"].append({
        "sender": payload.message.sender,
        "text": payload.message.text,
        "timestamp": payload.message.timestamp
    })

    session["total_messages"] += 1

    # --------------------------------------------------
    # 4. SCAM DETECTION (RULES + LLM)
    # --------------------------------------------------
    risk = score_message(payload.message.text)
    session["risk_score"] += risk

    if not session["scam_detected"] and session["risk_score"] >= 3:
        if llm_confirm_scam_intent(payload.message.text):
            session["scam_detected"] = True

    # --------------------------------------------------
    # 5. INTELLIGENCE EXTRACTION (SCAMMER ONLY)
    # --------------------------------------------------
    if payload.message.sender == "scammer":
        extracted = extract_intelligence(payload.message.text)

        for key, values in extracted.items():
            for value in values:
                if value not in session["intelligence"][key]:
                    session["intelligence"][key].append(value)

    # --------------------------------------------------
    # 6. AGENT REPLY (HONEYPOT ENGAGEMENT)
    # --------------------------------------------------
    agent_reply = None

    if session["scam_detected"]:
        if session["agent_turns"] < 6:
            agent_reply = generate_agent_reply_llm(session["messages"])
            session["agent_turns"] += 1
    # --------------------------------------------------
    # 7. FINAL GUVI CALLBACK (MANDATORY)
    # --------------------------------------------------
    if (
        session["scam_detected"]
        and not session["final_report_sent"]
        and session["agent_turns"] >= 3
        and (
            session["intelligence"]["upiIds"]
            or session["intelligence"]["bankAccounts"]
            or session["intelligence"]["phishingLinks"]
        )
    ):
        send_final_callback(payload.sessionId, session)
        session["final_report_sent"] = True

    # --------------------------------------------------
    # 8. METRICS
    # --------------------------------------------------
    engagement_duration = int(
        (datetime.utcnow() - session["start_time"]).total_seconds()
    )

    # --------------------------------------------------
    # 9. RESPONSE (STRICT FORMAT)
    # --------------------------------------------------
    return {
        "status": "success",
        "scamDetected": session["scam_detected"],
        "engagementMetrics": {
            "engagementDurationSeconds": engagement_duration,
            "totalMessagesExchanged": session["total_messages"]
        },
        "extractedIntelligence": session["intelligence"],
        "agentNotes": (
            f"Agent responded: {agent_reply}"
            if agent_reply
            else "Agent monitoring"
        )
    }
