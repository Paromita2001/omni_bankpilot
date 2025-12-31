# services/text_utils.py

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

STOPWORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

def normalize_for_rag(text: str) -> str:
    """
    Used ONLY inside RAG agent.
    Never use for intent or meaning detection.
    """

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    tokens = []
    for word in text.split():
        if word not in STOPWORDS:
            tokens.append(LEMMATIZER.lemmatize(word))

    return " ".join(tokens)
