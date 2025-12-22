# agents/bank_agent.py

def handle(context):
    """
    Handles banking-related actions like balance check, transfer, etc.
    """
    # For now, dummy response
    return "Your current balance is ₹50,000."
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="banking_assistant"
    )

def handle(intent: dict, context: str):
    sub_intent = intent["sub_intent"]
    user_id = 1  # assume logged-in user (session later)

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # -------------------------
    # BALANCE CHECK
    # -------------------------
    if sub_intent == "balance_check":
        cursor.execute(
            "SELECT balance FROM accounts WHERE user_id=%s",
            (user_id,)
        )
        row = cursor.fetchone()
        return f"Your current balance is ₹{row['balance']}."

    # -------------------------
    # TRANSACTION HISTORY
    # -------------------------
    if sub_intent == "transaction_history":
        cursor.execute(
            """
            SELECT date, amount, description
            FROM transactions
            WHERE user_id=%s
            ORDER BY date DESC
            LIMIT 5
            """,
            (user_id,)
        )
        rows = cursor.fetchall()

        if not rows:
            return "No transactions found."

        response = "Here are your last transactions:\n"
        for r in rows:
            response += f"{r['date']} | ₹{r['amount']} | {r['description']}\n"

        return response

    return "Bank action not supported."
