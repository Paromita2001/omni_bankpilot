import os
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(user_query: str) -> str:
    """
    You are a helpful banking assistant.
    RULES:
    - Keep answers SHORT (4–6 lines max)
    - Be clear and informative
    - Do NOT write long explanations
    - Avoid unnecessary examples
    - Use simple language
    - If the question is factual, answer directly
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. "
                        "Answer clearly, briefly, and in simple English. "
                        "Do not mention internal systems, RAG, or databases."
                    )
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature=0.3,
            max_tokens=200,
            timeout=6
        )

        return response.choices[0].message.content.strip()

    except Exception:
        # Safety fallback
        return "Sorry, I am unable to answer this question right now."
