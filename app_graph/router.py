# app_graph/router.py

from agents.bank_agent import handle as bank_agent
from agents.rag_agent import handle as rag_agent
from agents.reminder_agent import handle as reminder_agent
from agents.fallback_agent import handle as fallback_agent


def route(intent, context):
    """
    Routes the request to the correct agent
    """
    # intent is a dictionary like:
    # {"intent": "bank_action", "sub_intent": "balance_check"}

    main_intent = intent.get("intent")

    if main_intent == "bank_action":
        return bank_agent(context)

    elif main_intent == "info":
        return rag_agent(context, meaning)

    elif main_intent == "reminder":
        return reminder_agent(context)

    else:
        return fallback_agent(context)
