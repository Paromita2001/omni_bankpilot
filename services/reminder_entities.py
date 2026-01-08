import re

def extract_reminder_entities(text: str) -> dict:
    entities = {}
    clean_text = text.lower().strip()

    # -------------------------
    # TASK (CLEANED)
    # -------------------------
    # Remove command words
    clean_text = re.sub(
        r"(set|delete|remove|cancel)?\s*(a)?\s*reminder\s*(to)?",
        "",
        clean_text
    ).strip()

    # Now extract meaningful task
    task_match = re.search(r"(.*?)( every | daily | on |$)", clean_text)
    if task_match:
        entities["task"] = task_match.group(1).strip()

    # -------------------------
    # FREQUENCY
    # -------------------------
    if "daily" in text:
        entities["frequency"] = "daily"
    elif "every month" in text:
        entities["frequency"] = "monthly"

    # -------------------------
    # DAY
    # -------------------------
    day_match = re.search(r"(\d+)(st|nd|rd|th)", text)
    if day_match:
        entities["day"] = int(day_match.group(1))

    return entities
