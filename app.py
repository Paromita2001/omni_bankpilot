# app.py
# Main controller that orchestrates the full pipeline

from pipeline.context_pipeline import build_context
from pipeline.intent_pipeline import detect_intent
from services.memory import get_history, add_to_history
from graph.graph_builder import build_graph

# Build LangGraph once
graph = build_graph()

def run_pipeline(user_text):
    """
    Executes the full pipeline for a single user query
    """

    # 1. Get conversation history
    history = get_history()

    # 2. Build conversational context
    context = build_context(user_text, history)

    # 3. Detect intent
    intent_data = detect_intent(user_text, context)

    # 4. Prepare shared state
    state = {
        "user_input": user_text,
        "context": context,
        "intent": intent_data["intent"],
        "sub_intent": intent_data["sub_intent"],
        "history": history,
        "response": None
    }

    # 5. Invoke LangGraph
    result = graph.invoke(state)

    # 6. Store conversation
    add_to_history(user_text, result["response"])

    return result["response"]
