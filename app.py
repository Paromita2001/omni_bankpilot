from app_graph.graph_builder import build_graph
from db.reminder_db import get_due_reminders
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


# def run_pipeline(user_text: str, user_id: int):
#     print("🟡 run_pipeline START")
#     print("USER TEXT:", user_text)

#     try:
#         # meaning
#         meaning = meaning_pipeline.run(user_text)
#         print("🟢 MEANING:", meaning)

#         # entities
#         entities = extract_entities(user_text)
#         print("🟢 ENTITIES:", entities)

#         # intent
#         intent = intent_pipeline.run(meaning, entities)
#         print("🟢 INTENT:", intent)

#         # route
#         response = route(
#             user_id=user_id,
#             intent=intent,
#             context=user_text,
#             meaning=meaning,
#             entities=entities
#         )

#         print("🟢 RESPONSE:", response)
#         print("🟡 run_pipeline END")
#         return response

#     except Exception as e:
#         print("🔴 ERROR in run_pipeline:", e)
#         return "❌ Internal error occurred."




def run_pipeline(user_text: str, user_id: int):
    print("🟡 run_pipeline START")
    print("USER TEXT:", user_text)

    # ==================================================
    # 0️⃣ CHECK DUE REMINDERS (SKIP FOR REMINDER COMMANDS)
    # ==================================================
    lower_text = user_text.lower()

    is_reminder_command = any(
        kw in lower_text
        for kw in ["remind","reminder","delete reminder","remove reminder","show reminder"]
    )

    if not is_reminder_command:
        due_reminders = get_due_reminders(user_id)

        if due_reminders:
            reminder_msgs = []
            for task, frequency, day in due_reminders:
                reminder_msgs.append(f"🔔 Reminder: {task}")

            return "\n".join(reminder_msgs)


    # 1. Meaning (RAW TEXT)
    meaning = meaning_pipeline.run(user_text)
    print("🟢 MEANING:", meaning)

    # 2. Entities (RAW TEXT)
    entities = extract_entities(user_text)
    print("🟢 ENTITIES:", entities)

    # 3. Intent (RAW TEXT)
    intent = intent_pipeline.run(
        meaning=meaning,
        entities=entities,
        user_text=user_text
    )
    print("🟢 INTENT:", intent)

    # 4. Route
    response = route(
        user_id=user_id,
        intent=intent,
        context=user_text,   # RAW text
        meaning=meaning,
        entities=entities
    )

    print("🟢 RESPONSE:", response)
    print("🟡 run_pipeline END")
    return response
