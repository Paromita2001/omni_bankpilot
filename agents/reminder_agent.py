# agents/reminder_agent.py

# Simulated reminder store
REMINDER_DB = {
    "emi": {
        "day": 1,
        "status": "active"
    }
}


def handle(intent: dict, context: str):
    sub_intent = intent["sub_intent"]

    # -------------------------
    # SET REMINDER
    # -------------------------
    if sub_intent == "set":
        REMINDER_DB["emi"] = {
            "day": 1,
            "status": "active"
        }
        return "Your EMI reminder has been set successfully."

    # -------------------------
    # MODIFY REMINDER
    # -------------------------
    if sub_intent == "modify":
        if "emi" not in REMINDER_DB:
            return "No existing EMI reminder found to modify."

        REMINDER_DB["emi"]["day"] = 5  # example change
        return "Your EMI reminder has been updated."

    # -------------------------
    # DELETE REMINDER
    # -------------------------
    if sub_intent == "delete":
        if "emi" not in REMINDER_DB:
            return "No EMI reminder found to delete."

        del REMINDER_DB["emi"]
        return "Your EMI reminder has been deleted."

    return "Reminder action not supported."
