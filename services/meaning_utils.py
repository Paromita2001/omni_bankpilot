# # services/meaning_utils.py

# def meaning_to_rag_query(meaning: dict, user_text: str = "") -> str:
#     """
#     Convert structured meaning into a canonical RAG query.

#     Rules:
#     - Prefer domain object if available
#     - Otherwise fall back to raw user text
#     """

#     action = meaning.get("action")
#     obj = meaning.get("object")
#     owner = meaning.get("owner")

#     # Banking / RBI domain concepts
#     DOMAIN_OBJECTS = {
#         "account": "account",
#         "fixed_deposit": "fixed deposit",
#         "interest_rate": "interest rate",
#         "emi": "emi",
#         "credit_card": "credit card",
#         "debit_card": "debit card",
#         "kyc": "kyc"
#     }

#     if obj in DOMAIN_OBJECTS:
#         return DOMAIN_OBJECTS[obj]

#     # If general info but still banking-related → use raw query
#     if owner == "general" and action == "check":
#         return user_text

#     return ""


# services/meaning_utils.py

def meaning_to_rag_query(meaning: dict, user_text: str) -> str:
    """
    For RBI FAQs:
    - Always use RAW user text
    - Meaning is NOT reliable for FAQ matching
    """

    return user_text
