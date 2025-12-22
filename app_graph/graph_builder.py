from pipeline.context_pipeline import build_context
from pipeline.meaning_pipeline import run as meaning_pipeline
from pipeline.intent_pipeline import detect_intent
from app_graph.router import route


class SimpleGraph:
    def invoke(self, data):
        user_input = data["input"]

        context = build_context(user_input, history=[])

        meaning_text = meaning_pipeline(context)

        intent = detect_intent(meaning_text)

        response = route(intent, meaning_text)

        return {
            "response": response
        }


def build_graph():
    return SimpleGraph()
