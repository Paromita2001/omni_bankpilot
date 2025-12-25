import random
import time

# In-memory OTP store
OTP_STORE = {}

OTP_EXPIRY_SECONDS = 120  # 2 minutes


def generate_otp(user_id, transfer_data):
    otp = str(random.randint(100000, 999999))

    OTP_STORE[user_id] = {
        "otp": otp,
        "data": transfer_data,
        "created_at": time.time()
    }

    return otp


def verify_otp(user_id, entered_otp):
    record = OTP_STORE.get(user_id)

    if not record:
        return False, "❌ No pending transaction found."

    if time.time() - record["created_at"] > OTP_EXPIRY_SECONDS:
        OTP_STORE.pop(user_id, None)
        return False, "❌ OTP expired. Please initiate transfer again."

    if record["otp"] != entered_otp:
        return False, "❌ Invalid OTP."

    return True, record["data"]


def clear_otp(user_id):
    OTP_STORE.pop(user_id, None)
