import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT = """
You are a meaning extraction engine for an English-only banking assistant.

The user input will be in English.
If the input is unclear, incomplete, or not in English, return unknown values.

Your task:
1. Understand what the user wants to do.
2. Convert it into structured meaning.
3. Output ONLY valid JSON.
4. Do NOT explain.
5. Do NOT answer the user.

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

If intent is ambiguous or language is unsupported, use "unknown".

JSON format:
{
  "action": "...",
  "object": "...",
  "owner": "..."
}
"""

def run(clean_text: str) -> dict:
    """
    Meaning Extraction using FREE Groq LLM
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": clean_text}
        ],
        temperature=0
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
