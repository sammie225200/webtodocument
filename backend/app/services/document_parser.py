from io import BytesIO

from pypdf import PdfReader


def parse_document(filename: str, content: bytes):

    filename = filename.lower()

    if filename.endswith(".txt"):

        return content.decode(
            "utf-8",
            errors="ignore"
        )

    if filename.endswith(".pdf"):

        reader = PdfReader(
            BytesIO(content)
        )

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    return ""