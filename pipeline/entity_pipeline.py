import re

def extract_entities(text: str, meaning: dict | None = None) -> dict:
    """
    Extract entities like amount, receiver, OTP from user text.
    """
    entities = {}
    clean_text = text.strip()

    # =========================
    # OTP (highest priority)
    # =========================
    # If user enters only a 4–6 digit number, treat it as OTP
    otp_match = re.fullmatch(r"\d{4,6}", clean_text)
    if otp_match:
        entities["otp"] = otp_match.group()
        return entities   # 🔴 IMPORTANT: stop further extraction

    # =========================
    # AMOUNT
    # =========================
    # Extract numbers like 500, 2000 etc.
    amt_match = re.search(r"\b\d+\b", clean_text)
    if amt_match:
        entities["amount"] = int(amt_match.group())

    # =========================
    # RECEIVER
    # =========================
    # Handles: "to Rahul", "to Rahul Sharma"
    if " to " in clean_text.lower():
        receiver = clean_text.lower().split(" to ", 1)[-1]
        receiver = receiver.strip()

        # remove trailing numbers if any
        receiver = re.sub(r"\b\d+\b", "", receiver).strip()

        if receiver:
            entities["receiver"] = receiver.title()

    return entities
