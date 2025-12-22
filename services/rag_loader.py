from pathlib import Path

def load_qa_files(folder_path="data/rag"):
    qa_pairs = []

    for file in Path(folder_path).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        blocks = content.split("\n\n")
        question, answer = None, None

        for block in blocks:
            block = block.strip()

            if block.startswith("Q:"):
                question = block.replace("Q:", "").strip().lower()

            elif block.startswith("A:"):
                answer = block.replace("A:", "").strip()

            if question and answer:
                qa_pairs.append({
                    "question": question,
                    "answer": answer
                })
                question, answer = None, None

    return qa_pairs
