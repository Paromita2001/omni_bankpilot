from pipeline.input_router import is_direct_bank_command

"""
Intent Engine
-------------
Input  : Structured meaning + entities + raw user text
Output : System intent + sub_intent

Rules:
- NO stopword removal here
- NO NLP here
- Strict rule-based routing
"""

def run(
    meaning: dict,
    entities: dict | None = None,
    user_text: str = ""
) -> dict:

    entities = entities or {}
    user_text = user_text.lower()

    # ==================================================
    # 1️⃣ HIGHEST PRIORITY — OTP CONFIRMATION
    # ==================================================
    if "otp" in entities:
        return {
            "intent": "bank_action",
            "sub_intent": "money_transfer"
        }

    # ==================================================
    # 2️⃣ EXTRACT MEANING
    # ==================================================
    action = meaning.get("action", "unknown")
    obj = meaning.get("object", "unknown")
    owner = meaning.get("owner", "unknown")

    # ==================================================
    # 3️⃣ HARD BANK OVERRIDE (KEYWORD SAFETY)
    # ==================================================
    if is_direct_bank_command(user_text):
        if "balance" in user_text:
            return {
                "intent": "bank_action",
                "sub_intent": "balance_check"
            }

        if "transaction" in user_text or "history" in user_text:
            return {
                "intent": "bank_action",
                "sub_intent": "transaction_history"
            }

    # ==================================================
    # 4️⃣ BANK ACTIONS (STRICT MEANING)
    # ==================================================
    if action == "check" and owner == "self" and obj == "balance":
        return {
            "intent": "bank_action",
            "sub_intent": "balance_check"
        }

    if action == "check" and owner == "self" and obj in [
        "transactions", "transaction_history"
    ]:
        return {
            "intent": "bank_action",
            "sub_intent": "transaction_history"
        }

    if action == "transfer" and owner == "self":
        return {
            "intent": "bank_action",
            "sub_intent": "money_transfer"
        }

    # ==================================================
    # 5️⃣ REMINDER INTENTS (BEFORE RAG)
    # ==================================================
    if action == "set_reminder" and owner == "self":
        return {
            "intent": "reminder",
            "sub_intent": "set_reminder"
        }

    if action == "check" and obj == "reminder" and owner == "self":
        return {
            "intent": "reminder",
            "sub_intent": "show_reminder"
        }

    if action == "delete_reminder" and owner == "self":
        return {
            "intent": "reminder",
            "sub_intent": "delete_reminder"
        }

    # ==================================================
    # 6️⃣ INFORMATIONAL — RAG
    # ==================================================
    if owner == "general":
        return {
            "intent": "info",
            "sub_intent": "general_info"
        }

    # ==================================================
    # 7️⃣ OPEN-DOMAIN — LLM
    # ==================================================
    if action == "unknown" and owner == "unknown":
        return {
            "intent": "info",
            "sub_intent": "open_domain"
        }

    # ==================================================
    # 8️⃣ FINAL FALLBACK
    # ==================================================
    return {
        "intent": "fallback",
        "sub_intent": "unknown"
    }
