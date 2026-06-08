# Text extraction from uploaded files.
# Each format has its own extractor function.
# PDF and DOCX use third-party libraries; txt/md/csv/json are decoded directly.
# OCR is not implemented — scanned PDFs will return empty or partial text.
import io
import json

ALLOWED_EXTENSIONS = {"txt", "md", "csv", "json", "pdf", "docx"}


def get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def is_allowed(filename: str) -> bool:
    return get_extension(filename) in ALLOWED_EXTENSIONS


def extract_text(filename: str, data: bytes) -> str:
    """Extract plain text from file bytes. Returns empty string on failure."""
    ext = get_extension(filename)
    extractors = {
        "txt": _extract_plain,
        "md": _extract_plain,
        "csv": _extract_plain,
        "json": _extract_json,
        "pdf": _extract_pdf,
        "docx": _extract_docx,
    }
    extractor = extractors.get(ext)
    if not extractor:
        raise ValueError(f"Unsupported file type: {ext}")
    return extractor(data)


def _extract_plain(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _extract_json(data: bytes) -> str:
    # Pretty-print JSON so the AI can read it more easily
    try:
        parsed = json.loads(data.decode("utf-8", errors="replace"))
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return data.decode("utf-8", errors="replace")


def _extract_pdf(data: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(data))
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def _extract_docx(data: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
