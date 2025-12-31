# # app_graph/router.py

# from agents.bank_agent import BankAgent
# from agents.rag_agent import handle as rag_agent
# from agents.reminder_agent import handle as reminder_agent
# from agents.fallback_agent import handle as fallback_agent

# # Single instance (important for OTP / DB consistency)
# bank_agent = BankAgent()


# def route(
#     *,
#     user_id: int,
#     intent: dict,
#     context: str,
#     meaning: dict | None = None,
#     entities: dict | None = None
# ):
#     """
#     Central router that sends request to the correct agent.

#     Parameters:
#     - user_id   : logged-in user id
#     - intent    : output of intent_pipeline
#     - context   : RAW user text
#     - meaning   : structured meaning
#     - entities  : extracted entities
#     """

#     main_intent = intent.get("intent")

#     # =========================
#     # 1️⃣ BANK ACTIONS (SECURE)
#     # =========================
#     if main_intent == "bank_action":
#         return bank_agent.handle(
#             user_id=user_id,
#             intent=intent,
#             entities=entities
#         )

#     # =========================
#     # 2️⃣ INFORMATIONAL (RAG / LLM)
#     # =========================
#     if main_intent == "info":
#         return rag_agent(
#             context=context,
#             meaning=meaning
#         )

#     # =========================
#     # 3️⃣ REMINDER AGENT
#     # =========================
#     if main_intent == "reminder":
#         return reminder_agent(
#             context=context,
#             user_id=user_id,
#             intent=intent
#             )

#     # =========================
#     # 4️⃣ FINAL FALLBACK
#     # =========================
#     return fallback_agent(context)




# app_graph/router.py

from agents.bank_agent import BankAgent
from agents.rag_agent import handle as rag_agent
from agents.reminder_agent import handle as reminder_agent
from agents.fallback_agent import handle as fallback_agent

# Single instance (important for OTP / DB consistency)
bank_agent = BankAgent()


def route(
    *,
    user_id: int,
    intent: dict,
    context: str,
    meaning: dict | None = None,
    entities: dict | None = None
):
    """
    Central router that sends request to the correct agent.

    Parameters:
    - user_id   : logged-in user id
    - intent    : output of intent_pipeline
    - context   : RAW user text (never cleaned here)
    - meaning   : structured meaning
    - entities  : extracted entities
    """

    main_intent = intent.get("intent")
    entities = entities or {}   # 🔥 SAFETY FIX

    # =========================
    # 1️⃣ BANK ACTIONS (SECURE)
    # =========================
    if main_intent == "bank_action":
        return bank_agent.handle(
            user_id=user_id,
            intent=intent,
            entities=entities
        )

    # =========================
    # 2️⃣ INFORMATIONAL (RAG / LLM)
    # =========================
    if main_intent == "info":
        return rag_agent(
            context=context,
            meaning=meaning
        )

    # =========================
    # 3️⃣ REMINDER AGENT
    # =========================
    if main_intent == "reminder":
        return reminder_agent(
            context=context,
            user_id=user_id,
            intent=intent
        )

    # =========================
    # 4️⃣ FINAL FALLBACK (LLM)
    # =========================
    return fallback_agent(context)
