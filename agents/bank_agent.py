# agents/bank_agent.py

import random
from db.banking_db import (
    get_balance,
    get_transaction_history,
    make_transfer,
    save_otp,
    get_otp,
    delete_otp
)


class BankAgent:
    """
    Handles secure banking operations:
    - balance check
    - transaction history
    - money transfer with OTP (DB-backed)
    """

    def handle(
        self,
        *,
        user_id: int,
        intent: dict,
        entities: dict | None = None
    ):

        sub_intent = intent.get("sub_intent")

        # =========================
        # BALANCE CHECK
        # =========================
        if sub_intent == "balance_check":
            balance = get_balance(user_id)
            return f"💰 Your current balance is ₹{balance:.2f}"

        # =========================
        # TRANSACTION HISTORY
        # =========================
        if sub_intent == "transaction_history":
            txs = get_transaction_history(user_id)

            if not txs:
                return "📄 No recent transactions found."

            reply = "📄 Your recent transactions:\n"
            for desc, amount, date in txs:
                reply += f"- ₹{abs(amount)} to {desc} on {date}\n"

            return reply

        # =========================
        # MONEY TRANSFER (OTP FLOW)
        # =========================
        if sub_intent == "money_transfer":

            entities = entities or {}

            # -------- OTP CONFIRM STEP --------
            if "otp" in entities:
                return self._verify_otp(
                    user_id=user_id,
                    entered_otp=str(entities["otp"])
                )

            receiver = entities.get("receiver")
            amount = entities.get("amount")

            # -------- MISSING DETAILS CHECK --------
            if not receiver and not amount:
                return "❌ Please tell me whom you want to send money to and the amount."

            if not receiver:
                return "❌ Please tell me the receiver name."

            if not amount:
                return "❌ Please tell me the amount you want to transfer."

            # -------- INIT TRANSFER --------
            otp = str(random.randint(100000, 999999))

            save_otp(
                user_id=user_id,
                otp=otp,
                receiver=receiver,
                amount=amount
            )

            return (
                "⚠️ OTP sent to your registered mobile number.\n"
                f"(Demo OTP: {otp})\n"
                "Please enter the OTP to confirm transfer."
            )

        # =========================
        # UNKNOWN
        # =========================
        return "❌ Banking request not understood."

    # --------------------------------------------------
    # OTP VERIFICATION (DB-based)
    # --------------------------------------------------
    def _verify_otp(self, *, user_id: int, entered_otp: str):

        record = get_otp(user_id)

        if not record:
            return "❌ No pending transfer found."

        saved_otp, receiver, amount = record

        if entered_otp != saved_otp:
            return "❌ Invalid OTP. Transfer cancelled."

        success, msg = make_transfer(
            user_id=user_id,
            receiver_name=receiver,
            amount=amount
        )

        # Cleanup OTP after success/failure
        delete_otp(user_id)

        return msg
