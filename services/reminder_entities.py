# import re


# def extract_reminder_entities(text: str) -> dict:
#     """
#     Extract reminder-related entities from user text.
#     Supported:
#     - daily / weekly / monthly / yearly
#     - day of month (1st, 2nd, 15th etc.)
#     - delete reminder <id>
#     """

#     text = text.lower()
#     entities = {
#         "task": None,
#         "frequency": None,
#         "day": None,
#         "reminder_id": None
#     }

#     # -------------------------
#     # DELETE REMINDER ID
#     # -------------------------
#     match_id = re.search(r"\bdelete reminder (\d+)\b", text)
#     if match_id:
#         entities["reminder_id"] = int(match_id.group(1))
#         return entities

#     # -------------------------
#     # FREQUENCY
#     # -------------------------
#     if "daily" in text:
#         entities["frequency"] = "daily"
#     elif "weekly" in text:
#         entities["frequency"] = "weekly"
#     elif "monthly" in text:
#         entities["frequency"] = "monthly"
#     elif "yearly" in text or "annually" in text:
#         entities["frequency"] = "yearly"

#     # -------------------------
#     # DAY (for monthly / yearly)
#     # -------------------------
#     day_match = re.search(r"\b(\d{1,2})(st|nd|rd|th)?\b", text)
#     if day_match:
#         entities["day"] = int(day_match.group(1))

#     # -------------------------
#     # TASK CLEANING
#     # -------------------------
#     cleaned = text

#     cleaned = re.sub(r"set reminder to", "", cleaned)
#     cleaned = re.sub(r"remind me to", "", cleaned)
#     cleaned = re.sub(r"\bevery\b.*", "", cleaned)

#     # remove "on 1st", "on 15th"
#     cleaned = re.sub(r"\bon\s+\d{1,2}(st|nd|rd|th)?\b", "", cleaned)

#     # remove frequency words
#     cleaned = re.sub(
#         r"\bdaily\b|\bweekly\b|\bmonthly\b|\byearly\b|\bannually\b",
#         "",
#         cleaned
#     )

#     cleaned = re.sub(r"\s+", " ", cleaned).strip()

#     if cleaned:
#         entities["task"] = cleaned.capitalize()

#     return entities




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
