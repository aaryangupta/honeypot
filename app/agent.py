import random

AGENT_RESPONSES = [
    "I am not very sure about this. Can you explain?",
    "Why will my account be blocked?",
    "I have never faced this before. What should I do now?",
    "Is this from my bank only?",
    "I am outside right now, please tell me quickly."
]

def generate_agent_reply() -> str:
    return random.choice(AGENT_RESPONSES)
