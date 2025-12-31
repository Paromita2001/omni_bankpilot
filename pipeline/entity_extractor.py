# pipeline/entity_extractor.py
import re

def extract_entities(text: str, meaning: dict) -> dict:
    entities = {}

    # -------- Amount --------
    amount_match = re.search(r'\b(\d+)\b', text)
    if amount_match:
        entities["amount"] = int(amount_match.group(1))

    # -------- Receiver name --------
    if meaning.get("action") == "transfer":
        name_match = re.search(r'to\s+([A-Za-z ]+)', text)
        if name_match:
            entities["receiver"] = name_match.group(1).strip()

    return entities
