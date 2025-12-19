from pipeline.context_pipeline import build_context
from pipeline.intent_pipeline import detect_intent
from app_graph.router import route  


class SimpleGraph:
    def invoke(self, data):
        user_input = data["input"]  

        context = build_context(user_input, history=[])
        intent = detect_intent(user_input, context)
        response = route(intent, context)

        return {"response": response}


def build_graph():
    return SimpleGraph()
