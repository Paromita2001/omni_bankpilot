# pipeline/context_pipeline.py

def build_context(clean_text: str, history=None):
    """
    Very simple context builder for now.
    """
    history = history or []

    if not history:
        return clean_text

    recent = " ".join(history[-4:])
    return f"{recent} {clean_text}"
