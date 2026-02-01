import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a normal Indian user.
You are talking to someone claiming to help with a bank issue.

Rules:
- Sound cautious but cooperative
- Ask short, natural questions
- Do NOT accuse or threaten
- Do NOT mention fraud, scam, police, or AI
- Try to get clear details (bank name, UPI, link)
- Keep responses under 20 words
"""

def generate_agent_reply_llm(conversation: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Convert recent conversation to LLM format
    for msg in conversation[-6:]:
        role = "assistant" if msg["sender"] == "user" else "user"
        messages.append({
            "role": role,
            "content": msg["text"]
        })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.4,
        max_tokens=30
    )

    return response.choices[0].message.content.strip()
