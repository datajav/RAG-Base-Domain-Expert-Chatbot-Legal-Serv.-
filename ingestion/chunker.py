import re 
from typing import Any

SECTION_PATTERNS = [

    re.compile(r"^(\d+\.(?:d+\.?)*)\s+([A-Z][^\n]{0,80}})", re.multiline), 

    re.compile(r"^(Article|Section|ARTICLE|SECTION)\s+(\d+\.?\d*\.?\d*)\s*[:\--]?\s*([A-Z][^\n]{0,80})?", re.MULTILINE), 
    # ALL-CAPS headings (common in contracts): "INDEMNIFICATION", "GOVERNING LAW"
    re.compile(r"^([A-Z][A-Z\s]{4,60})$", re.MULTILINE),
    
]


def chunk_legal_document(
    pages: list[dict[str, Any]], 
    max_chunk_size: int = 1200,
    min_chunk_size: int = 100, 
    overlap_sentences: int = 2,
) -> list[dict[str, Any]]:

