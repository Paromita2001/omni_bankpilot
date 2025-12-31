from services.llm import ask_llm

def handle(context: str):
    """
    Fallback agent.
    Uses LLM to answer open-domain or unclear queries.
    """

    return ask_llm(context)
