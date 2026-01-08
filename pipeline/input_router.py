# pipeline/input_router.py

BANK_KEYWORDS = [
    "send", "transfer", "balance", "transaction", "history", "otp"
]

def is_direct_bank_command(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in BANK_KEYWORDS)
