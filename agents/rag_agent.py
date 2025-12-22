from services.rag_loader import load_qa_files
from services.text_utils import normalize
from services.meaning_utils import meaning_to_rag_query

QA_DATA = load_qa_files()

def handle(context: str, meaning: dict):
    # Use canonical meaning-based query
    rag_query = meaning_to_rag_query(meaning)

    if not rag_query:
        return "I couldn't find this information in our knowledge base."

    query = normalize(rag_query)
    query_tokens = set(query.split())

    best_match = None
    best_score = 0

    for item in QA_DATA:
        question = normalize(item["question"])
        question_tokens = set(question.split())

        score = len(query_tokens & question_tokens)

        if score > best_score:
            best_score = score
            best_match = item

    if best_match and best_score >= 1:
        return best_match["answer"]

    return "I couldn't find this information in our knowledge base."
