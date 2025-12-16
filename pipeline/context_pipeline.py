# pipeline/context_pipeline.py

def build_context(user_input, history):
    """
    Builds conversational context using previous messages
    """
    if not history:
        return user_input

    last_turns = history[-4:]  # last 2 user-bot exchanges
    context = " | ".join(last_turns)
    return f"{context} | Current: {user_input}"
