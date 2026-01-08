<<<<<<< HEAD
# app_graph/router.py

from services import rag_handler
from agents.bank_agent import BankAgent
=======
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
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
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
<<<<<<< HEAD
    Central router that sends request to the correct handler.
    """

    main_intent = intent.get("intent")
    entities = entities or {}

    # =========================
    # 1️⃣ BANK ACTIONS
=======
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
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
    # =========================
    if main_intent == "bank_action":
        return bank_agent.handle(
            user_id=user_id,
            intent=intent,
            entities=entities
        )

    # =========================
<<<<<<< HEAD
    # 2️⃣ INFORMATIONAL (RAG → LLM fallback)
    # =========================
    if main_intent == "info":
        return rag_handler.handle(
=======
    # 2️⃣ INFORMATIONAL (RAG / LLM)
    # =========================
    if main_intent == "info":
        return rag_agent(
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
            context=context,
            meaning=meaning
        )

    # =========================
<<<<<<< HEAD
    # 3️⃣ REMINDERS
=======
    # 3️⃣ REMINDER AGENT
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
    # =========================
    if main_intent == "reminder":
        return reminder_agent(
            context=context,
            user_id=user_id,
            intent=intent
        )

    # =========================
<<<<<<< HEAD
    # 4️⃣ FINAL FALLBACK
=======
    # 4️⃣ FINAL FALLBACK (LLM)
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
    # =========================
    return fallback_agent(context)
