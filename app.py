from app_graph.graph_builder import build_graph
from pipeline import meaning_pipeline
from pipeline import intent_pipeline
from pipeline.entity_pipeline import extract_entities
from app_graph.router import route


graph = build_graph()

# def run_pipeline(user_input, user_id=1):
#     """
#     user_input: raw text from UI (typed or spoken)
#     """

#     result = graph.invoke({
#         "input": user_input,
#         "user_id": user_id
#     })

#     return result["response"]


def run_pipeline(user_text: str, user_id: int):
    print("🟡 run_pipeline START")
    print("USER TEXT:", user_text)

    try:
        # meaning
        meaning = meaning_pipeline.run(user_text)
        print("🟢 MEANING:", meaning)

        # entities
        entities = extract_entities(user_text)
        print("🟢 ENTITIES:", entities)

        # intent
        intent = intent_pipeline.run(meaning, entities)
        print("🟢 INTENT:", intent)

        # route
        response = route(
            user_id=user_id,
            intent=intent,
            context=user_text,
            meaning=meaning,
            entities=entities
        )

        print("🟢 RESPONSE:", response)
        print("🟡 run_pipeline END")
        return response

    except Exception as e:
        print("🔴 ERROR in run_pipeline:", e)
        return "❌ Internal error occurred."
