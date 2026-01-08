# from app_graph.graph_builder import build_graph
# from db.reminder_db import get_due_reminders
# from pipeline import meaning_pipeline
# from pipeline import intent_pipeline
# from pipeline.entity_pipeline import extract_entities
# from app_graph.router import route


# graph = build_graph()
# app.py

from app_graph.graph_builder import build_graph
from pipeline import meaning_pipeline
from pipeline import intent_pipeline
from pipeline.entity_pipeline import extract_entities
from app_graph.router import route



# Build graph once (if you are using LangGraph)
graph = build_graph()


def run_pipeline(user_text: str, user_id: int):
    """
    Main orchestration pipeline.
    Handles:
    - Meaning extraction
    - Entity extraction
    - Intent detection
    - Routing to correct agent
    """

    print("🟡 run_pipeline START")
    print("USER TEXT:", user_text)

    try:
        # ==================================================
        # 1️⃣ MEANING EXTRACTION (RAW TEXT)
        # ==================================================
        meaning = meaning_pipeline.run(user_text)
        print("🟢 MEANING:", meaning)

        # ==================================================
        # 2️⃣ ENTITY EXTRACTION (RAW TEXT)
        # ==================================================
        entities = extract_entities(user_text)
        print("🟢 ENTITIES:", entities)

        # ==================================================
        # 3️⃣ INTENT DETECTION
        # ==================================================
        intent = intent_pipeline.run(
            meaning=meaning,
            entities=entities,
            user_text=user_text
        )
        print("🟢 INTENT:", intent)

        # ==================================================
        # 4️⃣ ROUTE TO CORRECT AGENT
        # ==================================================
        response = route(
            user_id=user_id,
            intent=intent,
            context=user_text,   # ALWAYS raw user text
            meaning=meaning,
            entities=entities
        )

        print("🟢 RESPONSE:", response)
        print("🟡 run_pipeline END")
        return response

    except Exception as e:
        print("🔴 ERROR in run_pipeline:", e)
        return "❌ Internal error occurred."
