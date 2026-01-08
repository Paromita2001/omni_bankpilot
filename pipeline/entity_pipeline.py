import re

def extract_entities(text: str, meaning: dict | None = None) -> dict:
    """
    Extract entities for banking, reminder, and OTP flows.
    """
    entities = {}
    clean_text = text.strip().lower()

    # ==================================================
    # 1️⃣ OTP (HIGHEST PRIORITY)
    # ==================================================
    otp_match = re.fullmatch(r"\d{4,6}", clean_text)
    if otp_match:
        entities["otp"] = otp_match.group()
        return entities   # 🔴 STOP further extraction


    # ==================================================
    # 2️⃣ AMOUNT (used in transfer)
    # ==================================================
    amt_match = re.search(r"\b(\d+)\b", clean_text)
    if amt_match:
        entities["amount"] = int(amt_match.group(1))


    # ==================================================
    # 3️⃣ REMINDER ENTITIES
    # ==================================================
    if "remind" in clean_text or "reminder" in clean_text:

        # ---- TASK ----
        # Example: "set a reminder to pay bill on 10th every month"
        task_match = re.search(r"to (.+?)( on | every |$)", clean_text)
        if task_match:
            entities["task"] = task_match.group(1).strip()

        # ---- DAY ----
        # Matches: 10th, 21st, 3rd
        day_match = re.search(r"(\d+)(st|nd|rd|th)", clean_text)
        if day_match:
            entities["day"] = int(day_match.group(1))

        # ---- FREQUENCY ----
        if "every month" in clean_text:
            entities["frequency"] = "monthly"
        elif "every week" in clean_text:
            entities["frequency"] = "weekly"
        elif "every day" in clean_text:
            entities["frequency"] = "daily"


    # ==================================================
    # 4️⃣ RECEIVER (ONLY FOR TRANSFER)
    # ==================================================
    # Example: "send 500 to rohit sharma"
    if " to " in clean_text and "remind" not in clean_text:
        receiver = clean_text.split(" to ", 1)[-1]
        receiver = re.sub(r"\b\d+\b", "", receiver).strip()

        if receiver:
            entities["receiver"] = receiver.title()


    return entities
