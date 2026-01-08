# services/rag_loader.py

from pathlib import Path


def _read_file_safely(path: Path) -> list[str]:
    """
    Read text file safely handling RBI / PDF encodings.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        # RBI PDFs usually fall here
        with open(path, "r", encoding="latin-1") as f:
            return f.readlines()


def load_qa_files(folder_path="data/rag"):
    """
    Load RBI FAQ Q/A pairs.
    Expected format:
    Q: question
    A: answer (may span multiple lines)
    """

    qa_pairs = []

    for file in Path(folder_path).glob("*.txt"):
        raw_lines = _read_file_safely(file)

        # clean empty lines
        lines = [l.strip() for l in raw_lines if l.strip()]

        question = None
        answer_lines = []

        for line in lines:

            # --------------------
            # QUESTION
            # --------------------
            if line.startswith("Q:"):
                if question and answer_lines:
                    qa_pairs.append({
                        "question": question,
                        "answer": " ".join(answer_lines),
                        "source": file.name
                    })

                question = line.replace("Q:", "").strip()
                answer_lines = []

            # --------------------
            # ANSWER
            # --------------------
            elif line.startswith("A:"):
                answer_lines.append(line.replace("A:", "").strip())

            # --------------------
            # MULTI-LINE ANSWER
            # --------------------
            elif question:
                answer_lines.append(line)

        # save last QA
        if question and answer_lines:
            qa_pairs.append({
                "question": question,
                "answer": " ".join(answer_lines),
                "source": file.name
            })

    return qa_pairs
