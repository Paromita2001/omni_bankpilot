# ui.py
print("UI file started")

from app import run_pipeline

print("Imported run_pipeline")

if __name__ == "__main__":
    print("Main block running")

    response1 = run_pipeline("How much money do I have?")
    print("Bot:", response1)

    response2 = run_pipeline("And last month?")
    print("Bot:", response2)
