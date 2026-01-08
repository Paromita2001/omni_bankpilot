import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT = """
You are a meaning extraction engine for an English-only banking assistant.

Your task is ONLY to understand what the user wants to do.
Do NOT perform any action.
Do NOT answer the user.
Do NOT assume missing details.

Ignore spelling mistakes and minor grammar issues.

-------------------------
GENERAL RULES
-------------------------
- Use action = "check" when the user is asking for information.
- Use action = "transfer" ONLY when the user wants to send or move money.
- Use action = "set_reminder" ONLY when the user wants to create, modify, or delete a reminder.
- If intent is unclear, use action = "unknown".

-------------------------
<<<<<<< HEAD
ACTION-OBJECT RULES
=======
ACTION–OBJECT RULES
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
-------------------------
- If action is "transfer", object MUST be "general_info".
- "balance" can ONLY be used with action = "check".
- Never output object = "balance" when action = "transfer".
- If rules conflict, prefer object = "general_info".

-------------------------
BANKING-SPECIFIC RULES
-------------------------
- If the user asks about account balance, use:
  action = "check", object = "balance", owner = "self"

- If the user asks about transaction history, transactions, spending history,
  bank statement, or recent transactions, use:
  action = "check", object = "transaction_history", owner = "self"

- If the user asks about savings account, fixed deposit, EMI, or interest rate
  in a general or informational way, use:
  action = "check", object = "general_info", owner = "general"

-------------------------
REMINDER RULES
-------------------------
- If user says "set reminder", "remind me", "create reminder":
  action = "set_reminder", object = "reminder", owner = "self"

- If user says "show reminders", "my reminders":
  action = "check", object = "reminder", owner = "self"

- If user says "delete reminder", "remove reminder":
  action = "delete_reminder", object = "reminder", owner = "self"

-------------------------
ALLOWED ACTIONS
-------------------------
- check
- explain
- transfer
- set_reminder
- unknown

-------------------------
ALLOWED OBJECTS
-------------------------
- balance
- account
- fixed_deposit
- interest_rate
- emi
- transaction_history
- general_info
- unknown

-------------------------
ALLOWED OWNER VALUES
-------------------------
- self
- general
- unknown

-------------------------
EXAMPLES
-------------------------
User: send money
Output:
{"action":"transfer","object":"general_info","owner":"self"}

User: what is my balance
Output:
{"action":"check","object":"balance","owner":"self"}

User: what is my balence
Output:
{"action":"check","object":"balance","owner":"self"}

User: show my transaction history
Output:
{"action":"check","object":"transaction_history","owner":"self"}

<<<<<<< HEAD
User: show my transaction history
Output: {"action":"check","object":"transaction_history","owner":"self"}

User: what is my transaction history
Output: {"action":"check","object":"transaction_history","owner":"self"}

User: show my transactions
Output: {"action":"check","object":"transaction_history","owner":"self"}

User: recent transactions
Output: {"action":"check","object":"transaction_history","owner":"self"}

=======
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
User: what is a savings account
Output:
{"action":"check","object":"general_info","owner":"general"}

User: set a reminder to pay EMI every month
Output:
{"action":"set_reminder","object":"emi","owner":"self"}

User: show reminders
Output: {"action":"check","object":"reminder","owner":"self"}

User: delete reminder 1
Output: {"action":"delete_reminder","object":"reminder","owner":"self"}

-------------------------
OUTPUT FORMAT
-------------------------
Output ONLY valid JSON.
No explanation.
No extra text.
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
