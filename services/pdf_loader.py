from pathlib import Path
from pypdf import PdfReader


def load_pdf_text(folder_path="data/rag"):
    """
    Load all PDF files and return clean text chunks.
    """

    chunks = []

    for pdf_file in Path(folder_path).glob("*.pdf"):
        reader = PdfReader(pdf_file)

        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        # Split into readable chunks (paragraphs)
        paragraphs = [
            p.strip()
            for p in full_text.split("\n")
            if len(p.strip()) > 50
        ]

        for para in paragraphs:
            chunks.append({
                "source": pdf_file.name,
                "text": para.lower()
            })

    return chunks
