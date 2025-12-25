from db.banking_db import make_transfer
from services.otp_store import verify_otp, clear_otp

class OTPAgent:

    def handle(self, user_id: int, otp_input: str):
        success, result = verify_otp(user_id, otp_input)

        if not success:
            return result

        receiver = result["receiver"]
        amount = result["amount"]

        ok, msg = make_transfer(user_id, receiver, amount)

        clear_otp(user_id)

        return msg
