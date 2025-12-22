"""
Intent Engine
-------------
Input  : Structured meaning from meaning_pipeline
Output : System intent + sub_intent
Language : English only
"""

def run(meaning: dict) -> dict:
    """
    meaning example:
    {
        "action": "check",
        "object": "balance",
        "owner": "self"
    }
    """

    action = meaning.get("action", "unknown")
    obj = meaning.get("object", "unknown")
    owner = meaning.get("owner", "unknown")

    # =========================
    # BANK ACTIONS (SECURE)
    # =========================

    # ---- Check balance ----
    if action == "check" and owner == "self" and obj == "balance":
        return {
            "intent": "bank_action",
            "sub_intent": "balance_check"
        }

    # ---- Transaction history ----
    if action == "check" and owner == "self" and obj == "transaction_history":
        return {
            "intent": "bank_action",
            "sub_intent": "transaction_history"
        }

    # ---- Money transfer (OTP required) ----
    if action == "transfer" and owner == "self":
        return {
            "intent": "bank_action",
            "sub_intent": "money_transfer"
        }

    # =========================
    # INFORMATIONAL (RAG)
    # =========================

    if action == "explain":
        return {
            "intent": "info",
            "sub_intent": obj
        }

    # =========================
    # REMINDER (OPTIONAL)
    # =========================

    if action == "set_reminder":
        return {
            "intent": "reminder",
            "sub_intent": obj
        }

    # =========================
    # FALLBACK / UNKNOWN
    # =========================

    return {
        "intent": "fallback",
        "sub_intent": "unknown"
    }
