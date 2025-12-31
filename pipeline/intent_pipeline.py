# """
# Intent Engine
# -------------
# Input  : Structured meaning + entities + raw user text
# Output : System intent + sub_intent
# Language : English only

# Design principles:
# - Banking actions are rule-based (safe)
# - Informational queries go to RAG
# - Open-domain info falls back to LLM
# """

# def run(
#     meaning: dict,
#     entities: dict | None = None,
#     user_text: str = ""
# ) -> dict:
#     """
#     Decide system intent based on meaning + entities.
#     IMPORTANT:
#     - Do NOT remove stopwords here
#     - Do NOT normalize text here
#     """

#     entities = entities or {}

#     # ==================================================
#     # 1️⃣ HIGHEST PRIORITY — OTP CONFIRMATION
#     # ==================================================
#     # If OTP exists, continue money transfer
#     if "otp" in entities:
#         return {
#             "intent": "bank_action",
#             "sub_intent": "money_transfer"
#         }

#     # ==================================================
#     # 2️⃣ EXTRACT MEANING FIELDS
#     # ==================================================
#     action = meaning.get("action", "unknown")
#     obj = meaning.get("object", "unknown")
#     owner = meaning.get("owner", "unknown")

#     # ==================================================
#     # 3️⃣ BANKING ACTIONS (STRICT)
#     # ==================================================

#     # Balance check
#     if action == "check" and owner == "self" and obj == "balance":
#         return {
#             "intent": "bank_action",
#             "sub_intent": "balance_check"
#         }

#     # Transaction history
#     if action == "check" and owner == "self" and obj in [
#         "transactions",
#         "transaction_history"
#     ]:
#         return {
#             "intent": "bank_action",
#             "sub_intent": "transaction_history"
#         }

#     # Money transfer
#     if action == "transfer" and owner == "self":
#         return {
#             "intent": "bank_action",
#             "sub_intent": "money_transfer"
#         }

#     # ==================================================
#     # 4️⃣ INFORMATIONAL — DOMAIN KNOWLEDGE (RAG)
#     # ==================================================
#     # Example: "what is a savings account"
#     if obj == "general_info" and owner == "general":
#         return {
#             "intent": "info",
#             "sub_intent": "general_info"
#         }

#     # ==================================================
#     # 5️⃣ OPEN-DOMAIN INFORMATION — LLM
#     # ==================================================
#     # Example: "what is food"
#     if action == "unknown" and owner == "unknown":
#         return {
#             "intent": "info",
#             "sub_intent": "open_domain"
#         }

#     # ==================================================
#     # 6️⃣ REMINDER ACTIONS
#     # ==================================================
# # =========================
# # REMINDER INTENTS
# # =========================

#     # Set reminder
#     if action == "set_reminder" and owner == "self":
#         return {
#             "intent": "reminder",
#             "sub_intent": "set_reminder"
#         }
#     # Show reminders
#     if action == "check" and obj == "reminder" and owner == "self":
#         return {
#             "intent": "reminder",
#             "sub_intent": "show_reminder"
#        }

#     # Delete reminder
#     if action == "delete_reminder" and owner == "self":
#         return {
#             "intent": "reminder",
#             "sub_intent": "delete_reminder"
#         }

#     # ==================================================
#     # 7️⃣ FINAL FALLBACK (TRULY UNKNOWN)
#     # ==================================================
#     return {
#         "intent": "fallback",
#         "sub_intent": "unknown"
#     }



# pipeline/intent_pipeline.py

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
