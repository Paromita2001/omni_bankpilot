# services/memory.py

conversation_history = []

def get_history():
    """
    Returns full conversation history
    """
    return conversation_history

def add_to_history(user_text, bot_text):
    """
    Stores user and bot messages
    """
    conversation_history.append(f"User: {user_text}")
    conversation_history.append(f"Bot: {bot_text}")
