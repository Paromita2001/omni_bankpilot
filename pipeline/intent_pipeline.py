# pipeline/intent_pipeline.py

def detect_intent(user_input, context):
    text = user_input.lower()

    # Informational queries → RAG
    if "fd" in text or "fixed deposit" in text or "interest" in text:
        return {
            "intent": "info"
        }

    # Reminder related
    if "remind" in text or "emi" in text or "bill" in text:
        return {
            "intent": "reminder"
        }

    # Banking actions
    if "balance" in text or "transfer" in text or "account" in text:
        return {
            "intent": "bank_action"
        }

    # Fallback
    return {
        "intent": "fallback"
    }
