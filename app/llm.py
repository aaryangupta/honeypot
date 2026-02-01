import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a fraud intent detection system.
Your job is to decide if a message is attempting
to manipulate the recipient into sharing money,
financial identifiers, credentials, or clicking
a potentially malicious link.

You must answer ONLY with:
YES or NO
"""

def llm_confirm_scam_intent(text: str) -> bool:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0,
        max_tokens=3,
    )

    answer = response.choices[0].message.content.strip().upper()

    return answer == "YES"

if __name__ == "__main__":
    print(llm_confirm_scam_intent("Your bank account will be blocked today"))
    print(llm_confirm_scam_intent("Hello, are you free for a call?"))
