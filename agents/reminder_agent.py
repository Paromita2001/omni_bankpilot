from datetime import date
from db.reminder_db import (
    add_reminder,
    get_reminders,
    delete_reminder,
    find_reminders_by_task,
    parse_natural_date
)
from services.reminder_entities import extract_reminder_entities


# -------------------------
# HELPERS
# -------------------------
def detect_frequency_from_text(text: str):
    """
    Infer frequency from raw user text
    """
    text = text.lower()

    if "every month" in text or "monthly" in text:
        return "monthly"

    if "every day" in text or "daily" in text:
        return "daily"

    if "every week" in text or "weekly" in text:
        return "weekly"

    return None


def _best_task_match(task: str, reminders: list):
    """
    Pick the closest reminder based on substring match.
    """
    task = task.lower().strip()

    for r_id, r_task in reminders:
        if task in r_task.lower():
            return r_id, r_task

    return None


# -------------------------
# MAIN HANDLER
# -------------------------
def handle(context: str, user_id: int, intent: dict):
    entities = extract_reminder_entities(context)
    sub_intent = intent.get("sub_intent")
    text = context.lower()

    # =========================
    # SET REMINDER
    # =========================
    if sub_intent == "set_reminder":
        task = entities.get("task")
        frequency = entities.get("frequency")
        day = entities.get("day")
        date_text = entities.get("date")

        if not task:
            return "Please tell me what you want to be reminded about."

        # 🔥 Infer frequency if not extracted
        if not frequency:
            frequency = detect_frequency_from_text(text)

        # 🔹 Try natural date (today / tomorrow / exact date)
        scheduled_date = None
        if date_text:
            scheduled_date = parse_natural_date(date_text)

        # =========================
        # MONTHLY REMINDER
        # =========================
        if frequency == "monthly":
            if not day:
                return "Please tell me which day of the month."

            add_reminder(
                user_id=user_id,
                task=task,
                frequency="monthly",
                day=day
            )
            return f"Monthly reminder set on {day}th to {task}."

        # =========================
        # DAILY REMINDER
        # =========================
        if frequency == "daily":
            add_reminder(
                user_id=user_id,
                task=task,
                frequency="daily"
            )
            return f"Daily reminder set to {task}."

        # =========================
        # ONE-TIME REMINDER (today / tomorrow / date)
        # =========================
        if scheduled_date:
            add_reminder(
                user_id=user_id,
                task=task,
                frequency="once",
                scheduled_date=scheduled_date
            )
            return f"Reminder set for {scheduled_date.isoformat()} to {task}."

        # =========================
        # MISSING INFO
        # =========================
        return "When should I remind you?"

    # =========================
    # SHOW REMINDERS
    # =========================
    if sub_intent == "show_reminder":
        reminders = get_reminders(user_id)

        if not reminders:
            return " You have no reminders."

        reply = "Your reminders:\n"
        for r_id, task, freq, scheduled_date, day, _ in reminders:
            if freq == "monthly":
                reply += f"- ({r_id}) {task} → monthly on day {day}\n"
            elif freq == "daily":
                reply += f"- ({r_id}) {task} → daily\n"
            elif freq == "once":
                reply += f"- ({r_id}) {task} → on {scheduled_date}\n"

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
            return "Reminder deleted successfully."

        # 2️⃣ Delete by task text
        if task:
            matches = find_reminders_by_task(user_id, task)

            if not matches:
                return f"I couldn't find any reminder for '{task}'."

            best = _best_task_match(task, matches)
            if best:
                r_id, task_name = best
                delete_reminder(r_id, user_id)
                return f"Reminder '{task_name}' deleted."

            reply = "I found multiple reminders:\n"
            for r_id, task_name in matches:
                reply += f"- ({r_id}) {task_name}\n"
            reply += "Please tell me the reminder ID to delete."

            return reply

        return "Please tell me which reminder you want to delete."

    return "I could not understand the reminder request."
