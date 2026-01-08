from services.rag_loader import load_qa_files
from services.text_utils import normalize_for_rag
from services.llm import ask_llm
import re


QA_DATA = load_qa_files()

# Absolute token overlap threshold (NOT percentage)
MIN_TOKEN_OVERLAP = 3


ACRONYM_MAP = {
    "kyc": "know your customer",
    "fd": "fixed deposit",
    "rd": "recurring deposit",
    "atm": "automated teller machine",
    "ifsc": "indian financial system code"
}

def expand_acronyms(text: str) -> str:
    """
    Expands banking acronyms for better RAG recall
    """
    for short, full in ACRONYM_MAP.items():
        pattern = rf"\b{short}\b"
        if re.search(pattern, text):
            text = re.sub(pattern, f"{short} {full}", text)
    return text


def handle(context: str, meaning: dict):
    """
    RBI FAQ RAG handler.
    - NLP matching only happens here
    - If no strong match → fallback to LLM
    """

    raw_query = context

    query = normalize_for_rag(context)
    query_tokens = set(query.split())

    best_match = None
    best_overlap = 0

    for item in QA_DATA:
        question = normalize_for_rag(item["question"])
        question_tokens = set(question.split())

        overlap = len(query_tokens & question_tokens)

        if overlap > best_overlap:
            best_overlap = overlap
            best_match = item

    # 🔍 Debug visibility (VERY IMPORTANT)
    print(f"🧠 RAG | token overlap = {best_overlap}")
    print(f"🧠 RAG | normalized query: {query}")


    effective_threshold = 3 if len(query_tokens) <= 5 else MIN_TOKEN_OVERLAP

    
    # ✅ STRONG MATCH → RBI ANSWER
    if best_match and best_overlap >= effective_threshold:
        print(f"🧠 RAG | matched from: {best_match['source']}")
        return best_match["answer"]

    # ❌ Weak / no match → LLM
    print("🧠 RAG | fallback → LLM")
    return ask_llm(raw_query)





