# from services.rag_loader import load_qa_files
# from services.text_utils import normalize_for_rag
# from services.meaning_utils import meaning_to_rag_query
# from services.llm import ask_llm

# QA_DATA = load_qa_files()
# CONFIDENCE_THRESHOLD = 0.2


# def handle(context: str, meaning: dict):
#     """
#     NLP-based RAG with confidence scoring.
#     Falls back to LLM if confidence is low.
#     """

#     # 1️⃣ Build canonical query
#     rag_query = meaning_to_rag_query(meaning, context)

#     if not rag_query:
#         print("🧠 RAG | no canonical query → LLM")
#         return ask_llm(context)

#     print(f"🧠 RAG | canonical query: {rag_query}")

#     query = normalize_for_rag(rag_query)
#     query_tokens = set(query.split())

#     best_match = None
#     best_score = 0.0

#     # 2️⃣ Compare against RBI FAQ questions
#     for item in QA_DATA:
#         q = normalize_for_rag(item["question"])
#         q_tokens = set(q.split())

#         if not q_tokens:
#             continue

#         overlap = len(query_tokens & q_tokens)
#         confidence = overlap / len(q_tokens)

#         if confidence > best_score:
#             best_score = confidence
#             best_match = item

#     print(f"🧠 RAG | best confidence = {round(best_score, 2)}")

#     # 3️⃣ Confidence decision
#     if best_match and best_score >= CONFIDENCE_THRESHOLD:
#         print(f"🧠 RAG | source = {best_match['source']}")
#         return best_match["answer"]

#     print("🧠 RAG | low confidence → LLM")
#     return ask_llm(context)



# agents/rag_agent.py




# agents/rag_agent.py

from services.rag_loader import load_qa_files
from services.text_utils import normalize_for_rag
from services.llm import ask_llm

QA_DATA = load_qa_files()

# Absolute token overlap threshold (NOT percentage)
MIN_TOKEN_OVERLAP = 3


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

    # ✅ STRONG MATCH → RBI ANSWER
    if best_match and best_overlap >= MIN_TOKEN_OVERLAP:
        print(f"🧠 RAG | matched from: {best_match['source']}")
        return best_match["answer"]

    # ❌ Weak / no match → LLM
    print("🧠 RAG | fallback → LLM")
    return ask_llm(raw_query)
