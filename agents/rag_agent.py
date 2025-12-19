# agents/rag_agent.py

# Temporary knowledge base (replace with your 6 Q&A)
KB = {
    "fd kya hota hai": "FD (Fixed Deposit) ek investment option hota hai jisme aap paisa fixed time ke liye bank me rakhte ho aur interest milta hai.",
    "interest rate kya hai": "Current FD interest rate bank ke policy ke hisaab se vary karta hai.",
    "bank timing kya hai": "Bank Monday se Friday, 9 AM se 5 PM tak open rehta hai.",
}

def handle(context):
    """
    Handles informational queries using simple Q&A matching
    """
    query = context.lower()

    for question, answer in KB.items():
        if question in query:
            return answer

    return "Sorry, is question ka answer abhi available nahi hai."
