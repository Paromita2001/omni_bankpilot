from app import run_pipeline

print("UI file started")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    response = run_pipeline(user_input)
    print("Bot:", response)
