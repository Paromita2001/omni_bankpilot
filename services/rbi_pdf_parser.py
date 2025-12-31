import re
from pathlib import Path
from pypdf import PdfReader


QUESTION_PATTERNS = [
    r"^query\s*\d+[\.\)]\s*(.*)",
    r"^q[\.\s]*\d+[\.\)]\s*(.*)",
    r"^\d+[\.\)]\s*(what.*\?)",
    r"^(what.*\?)"
]

ANSWER_PATTERNS = [
    r"^response[:\-]?\s*(.*)",
    r"^ans[:\-]?\s*(.*)"
]


def is_question(line: str):
    for pattern in QUESTION_PATTERNS:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def is_answer_start(line: str):
    for pattern in ANSWER_PATTERNS:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def load_rbi_faqs(folder_path="data/rag"):
    """
    Robust RBI FAQ loader.
    Handles Query/Response, Q/A, numbered, and plain formats.
    """

    qa_pairs = []

    for pdf in Path(folder_path).glob("*.pdf"):
        reader = PdfReader(pdf)

        lines = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines.extend([l.strip() for l in text.split("\n") if l.strip()])

        current_q = None
        current_a = []

        for line in lines:

            q = is_question(line)
            if q:
                # Save previous Q&A
                if current_q and current_a:
                    qa_pairs.append({
                        "question": current_q.lower(),
                        "answer": " ".join(current_a)
                    })

                current_q = q
                current_a = []
                continue

            ans_start = is_answer_start(line)
            if ans_start:
                current_a.append(ans_start)
                continue

            # Regular answer continuation
            if current_q:
                current_a.append(line)

        # Save last pair
        if current_q and current_a:
            qa_pairs.append({
                "question": current_q.lower(),
                "answer": " ".join(current_a)
            })

    return qa_pairs
