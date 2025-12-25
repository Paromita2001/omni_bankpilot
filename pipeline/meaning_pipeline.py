import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT = """
You are a meaning extraction engine for an English-only banking assistant.

Your task is ONLY to understand what the user wants to do.
Do NOT perform actions. Do NOT assume missing details.

Rules:
- Use action = "check" when the user is asking for information.
- Use action = "transfer" ONLY when the user wants to send or move money.
- Ignore spelling mistakes.
- Do NOT guess missing details.
- If intent is unclear, use "unknown".

Action–Object Rules:
- If action is "transfer", object MUST be "general_info".
- "balance" can ONLY be used with action "check".
- Never output object = "balance" when action = "transfer".
- If rules conflict, prefer "general_info".

Allowed actions:
- check
- explain
- transfer
- set_reminder
- unknown

Allowed objects:
- balance
- account
- fixed_deposit
- interest_rate
- emi
- general_info
- unknown

Allowed owner values:
- self
- general
- unknown

Examples:
User: send money
Output: {"action":"transfer","object":"general_info","owner":"self"}

User: what is my balance
Output: {"action":"check","object":"balance","owner":"self"}

User: what is my balence
Output: {"action":"check","object":"balance","owner":"self"}

Output ONLY valid JSON. No explanation.
"""


def run(clean_text: str) -> dict:
    """
    Meaning Extraction using FREE Groq LLM
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # OK for meaning extraction
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": clean_text}
        ],
        temperature=0,
        #max_tokens=100,
        timeout=6  
    )


    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        # safety fallback
        return {
            "action": "unknown",
            "object": "general_info",
            "owner": "unknown"
        }
