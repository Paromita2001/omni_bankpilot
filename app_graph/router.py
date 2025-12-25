# app_graph/router.py

from agents.bank_agent import BankAgent
from agents.rag_agent import handle as rag_agent
from agents.reminder_agent import handle as reminder_agent
from agents.fallback_agent import handle as fallback_agent

# Single instance (important for state consistency)
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
    Central router that sends request to correct agent
    """

    main_intent = intent.get("intent")

    # =========================
    # BANK ACTIONS (SECURE)
    # =========================
    if main_intent == "bank_action":
        return bank_agent.handle(
            user_id=user_id,
            intent=intent,
            entities=entities      # ✅ MUST be `entities`
        )

    # =========================
    # INFORMATIONAL (RAG)
    # =========================
    if main_intent == "info":
        return rag_agent(context)

    # =========================
    # REMINDER AGENT
    # =========================
    if main_intent == "reminder":
        return reminder_agent(context)

    # =========================
    # FALLBACK
    # =========================
    return fallback_agent(context)
