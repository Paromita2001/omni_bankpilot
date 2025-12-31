# from db.reminder_db import (
#     add_reminder,
#     get_reminders,
#     delete_reminder,
#     find_reminders_by_task   # ⬅️ NEW helper
# )
# from services.reminder_entities import extract_reminder_entities


# def handle(context: str, user_id: int, intent: dict):
#     entities = extract_reminder_entities(context)
#     sub_intent = intent.get("sub_intent")

#     # =========================
#     # SET REMINDER
#     # =========================
#     if sub_intent == "set_reminder":
#         task = entities.get("task")
#         frequency = entities.get("frequency")
#         day = entities.get("day")

#         if not task:
#             return "Please tell me what to remind."

#         if not frequency:
#             return "How often should I remind you?"

#         add_reminder(user_id, task, frequency, day)

#         if day:
#             return f"✅ Reminder set to {task} ({frequency} on day {day})"
#         return f"✅ Reminder set to {task} ({frequency})"

#     # =========================
#     # SHOW REMINDERS
#     # =========================
#     if sub_intent == "show_reminder":
#         reminders = get_reminders(user_id)

#         if not reminders:
#             return "📭 You have no reminders."

#         reply = "📅 Your reminders:\n"
#         for r_id, task, freq, day, _ in reminders:
#             if day:
#                 reply += f"- ({r_id}) {task} → {freq} on day {day}\n"
#             else:
#                 reply += f"- ({r_id}) {task} → {freq}\n"

#         return reply

#     # =========================
#     # DELETE REMINDER
#     # =========================
#     if sub_intent == "delete_reminder":
#         reminder_id = entities.get("reminder_id")
#         task = entities.get("task")

#         # 1️⃣ Delete by ID
#         if reminder_id:
#             delete_reminder(reminder_id, user_id)
#             return "🗑️ Reminder deleted successfully."

#         # 2️⃣ Delete by TASK (natural language)
#         if task:
#             matches = find_reminders_by_task(user_id, task)

#             if not matches:
#                 return f"❌ I couldn’t find any reminder for '{task}'."

#             if len(matches) == 1:
#                 r_id, task_name = matches[0]
#                 delete_reminder(r_id, user_id)
#                 return f"🗑️ Reminder '{task_name}' deleted."

#             # Multiple matches
#             reply = "I found multiple reminders:\n"
#             for r_id, task_name in matches:
#                 reply += f"- ({r_id}) {task_name}\n"
#             reply += "Please specify the reminder ID to delete."

#             return reply

#         # 3️⃣ Nothing provided
#         return "Please tell me which reminder you want to delete."

#     return "I could not understand the reminder request."






from db.reminder_db import (
    add_reminder,
    get_reminders,
    delete_reminder,
    find_reminders_by_task
)
from services.reminder_entities import extract_reminder_entities


def _best_task_match(task: str, reminders: list):
    """
    Pick the closest reminder based on full semantic match.
    """
    task = task.lower().strip()

    # Highest confidence: full substring match
    for r_id, r_task in reminders:
        if task in r_task.lower():
            return r_id, r_task

    return None


def handle(context: str, user_id: int, intent: dict):
    entities = extract_reminder_entities(context)
    sub_intent = intent.get("sub_intent")

    # =========================
    # SET REMINDER
    # =========================
    if sub_intent == "set_reminder":
        task = entities.get("task")
        frequency = entities.get("frequency")
        day = entities.get("day")

        if not task:
            return "Please tell me what to remind."

        if not frequency:
            return "How often should I remind you?"

        add_reminder(user_id, task, frequency, day)

        if day:
            return f"✅ Reminder set to {task} ({frequency} on day {day})"
        return f"✅ Reminder set to {task} ({frequency})"

    # =========================
    # SHOW REMINDERS
    # =========================
    if sub_intent == "show_reminder":
        reminders = get_reminders(user_id)

        if not reminders:
            return "📭 You have no reminders."

        reply = "📅 Your reminders:\n"
        for r_id, task, freq, day, _ in reminders:
            if day:
                reply += f"- ({r_id}) {task} → {freq} on day {day}\n"
            else:
                reply += f"- ({r_id}) {task} → {freq}\n"

        return reply

    # =========================
    # DELETE REMINDER
    # =========================
    if sub_intent == "delete_reminder":
        reminder_id = entities.get("reminder_id")
        task = entities.get("task")

        # 1️⃣ Delete by ID
        if reminder_id:
            delete_reminder(reminder_id, user_id)
            return "🗑️ Reminder deleted successfully."

        # 2️⃣ Delete by TASK (natural language)
        if task:
            matches = find_reminders_by_task(user_id, task)

            if not matches:
                return f"❌ I couldn’t find any reminder for '{task}'."

            # 🔥 Try best semantic match first
            best = _best_task_match(task, matches)
            if best:
                r_id, task_name = best
                delete_reminder(r_id, user_id)
                return f"🗑️ Reminder '{task_name}' deleted."

            # 3️⃣ Still ambiguous → ask user
            reply = "I found multiple reminders:\n"
            for r_id, task_name in matches:
                reply += f"- ({r_id}) {task_name}\n"
            reply += "Please specify the reminder ID to delete."

            return reply

        return "Please tell me which reminder you want to delete."

    return "I could not understand the reminder request."
