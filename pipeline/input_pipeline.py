"""
INPUT HANDLING LAYER

Responsibilities:
- Lowercase input text
- Correct spelling errors (generic + banking-domain)
- Preserve full semantic content

Output:
{
    "clean_text": "<normalized text>"
}
"""

import re
from spellchecker import SpellChecker

spell = SpellChecker()

# Small, high-frequency banking typo corrections
# (NOT training, just normalization)
DOMAIN_CORRECTIONS = {
    "balence": "balance",
    "balnce": "balance",
    "acount": "account",
    "accout": "account",
    "intrest": "interest",
    "interset": "interest",
    "deposite": "deposit",
}

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return text.lower().strip()

def correct_spelling(text: str) -> str:
    corrected_words = []

    for word in text.split():
        # Keep numbers unchanged
        if word.isdigit():
            corrected_words.append(word)
            continue

        # Strip punctuation for checking
        clean_word = re.sub(r"[^a-z]", "", word)

        if not clean_word:
            corrected_words.append(word)
            continue

        # 1) Domain correction (deterministic)
        if clean_word in DOMAIN_CORRECTIONS:
            corrected_words.append(DOMAIN_CORRECTIONS[clean_word])
            continue

        # 2) Generic NLP spell correction
        corrected = spell.correction(clean_word)
        corrected_words.append(corrected if corrected else clean_word)

    return " ".join(corrected_words)

def run(raw_text: str) -> dict:
    """
    Entry point for the Input Handling Layer.
    Called immediately after STT or text input.
    """
    text = normalize_text(raw_text)
    clean_text = correct_spelling(text)

    return {
        "clean_text": clean_text
    }
