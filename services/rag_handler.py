# services/rag_handler.py

from services.rag_loader import load_qa_files
from services.text_utils import normalize_for_rag
from services.llm import ask_llm
import re

# Load RBI FAQ / QA data once
QA_DATA = load_qa_files()

# Banking acronyms
ACRONYM_MAP = {
    "kyc": "know your customer",
    "fd": "fixed deposit",
    "rd": "recurring deposit",
    "atm": "automated teller machine",
    "ifsc": "indian financial system code"
}


def expand_acronyms(text: str) -> str:
    """
    Expands banking acronyms to improve exact-match recall
    Example: 'kyc' -> 'kyc know your customer'
    """
    for short, full in ACRONYM_MAP.items():
        pattern = rf"\b{short}\b"
        if re.search(pattern, text):
            text = re.sub(pattern, f"{short} {full}", text)
    return text


def handle(context: str, meaning: dict):
    """
    RAG handler (STRICT MODE)

    Rule:
    - Use RAG ONLY if query is exact / near-exact match with FAQ
    - Otherwise fallback to LLM
    """

    # Keep original query for LLM fallback
    raw_query = context

    # ---- Normalize & expand QUERY ----
    query = expand_acronyms(context.lower())
    query = normalize_for_rag(query)
    query_tokens = set(query.split())

    best_match = None
    best_overlap = 0

    # ---- Compare against FAQ questions ----
    for item in QA_DATA:
        question = expand_acronyms(item["question"].lower())
        question = normalize_for_rag(question)
        question_tokens = set(question.split())

        overlap = len(query_tokens & question_tokens)

        if overlap > best_overlap:
            best_overlap = overlap
            best_match = item

    # ---- Debug logs ----
    print(f"🧠 RAG | normalized query: {query}")
    print(f"🧠 RAG | token overlap = {best_overlap}")

    # ---- STRICT exact / near-exact match check ----
    if best_match:
        similarity_ratio = best_overlap / max(len(query_tokens), 1)

        if similarity_ratio >= 0.8:
            print(f"🧠 RAG | exact match from: {best_match['source']}")
            return best_match["answer"]

    # ---- Fallback to LLM ----
    print("🧠 RAG | not exact → fallback to LLM")
    return ask_llm(raw_query)
