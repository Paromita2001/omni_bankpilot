from db.banking_db import login_user, get_transaction_history, get_balance

email = input("Enter email: ")
password = input("Enter password: ")

user_id, message = login_user(email, password)
print(message)

if user_id:
    # Balance
    balance = get_balance(user_id)
    print(f"\n💰 Current Balance: ₹{balance}")

    # Transactions
    print("\n📄 Last 10 Transactions:\n")
    transactions = get_transaction_history(user_id)

    for sent_to, amount, date in transactions:
        print(f"Sent ₹{abs(amount)} to {sent_to} on {date}")
