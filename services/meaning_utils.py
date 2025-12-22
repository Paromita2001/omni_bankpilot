def meaning_to_rag_query(meaning: dict) -> str:
    """
    Convert structured meaning into a canonical query
    for RAG matching
    """

    action = meaning.get("action")
    obj = meaning.get("object")

    if action == "explain" and obj != "unknown":
        return obj.replace("_", " ")

    return ""
