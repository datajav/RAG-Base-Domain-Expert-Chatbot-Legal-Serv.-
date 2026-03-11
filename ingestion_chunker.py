import re #used for regular expressions
from typing import Literal #anything types, does not allow restricitions 

# This section is for the regex patterns for the legal section detection
#____________________________________________________________________________
# Matches: "1.", "1.1", "1.1.1", "Article 1", "Section 3.2", "SECTION IV"
section_patterns = [
    # Numbered: 1. or 1.1 or 1.1.2
    re.compile(r"^(\d+\.(?:\d+\.?)*)\s+([A-Z][^\n]{0,80})", re.MULTILINE),
    # "Article 3" or "Section 4.1"
    re.compile(r"^(Article|Section|ARTICLE|SECTION)\s+(\d+\.?\d*\.?\d*)\s*[:\-–]?\s*([A-Z][^\n]{0,80})?", re.MULTILINE),
    # ALL-CAPS headings (common in contracts): "INDEMNIFICATION", "GOVERNING LAW"
    re.compile(r"^([A-Z][A-Z\s]{4,60})$", re.MULTILINE),
]

#This section is for the chunker for the document, which will break the document into smaller sections for easier processing
#____________________________________________________________________________

def chunk_legal_document(
    pages: list[dict[str, any]], #variable for the pages of the document, each page is a dictionary with keys 'text' and 'page_number'
    max_chunk_size: int = 2000,
    min_chunk_size: int = 500,
    overlap_sentences: int  = 2,
) -> list[dict[str, any]]:


 """ 

Conversion of the legal document into chunks based on the section headings and the specified chunk size parameters.

    Args:
        pages:              Output from ingestion/loader.py
        max_chunk_size:     Max characters per chunk (larger than generic RAG
                            because legal clauses need more context)
        min_chunk_size:     Ignore chunks shorter than this (usually headers)
        overlap_sentences:  How many sentences to repeat between chunks
                            for continuity (replaces character-based overlap)

    Returns:
        List of chunk dicts (see module docstring for schema

 """

all_chunks = []
chunk_index = 0 

for page in pages: 
    page_chunks = chunk_page(
        page_text=page["text"],
        source=page["source"],
        page_number=page["page_number"],
        max_chunk_size=max_chunk_size,
        min_chunk_size=min_chunk_size, 
        overlap_sentences=overlap_sentences,
        start_chunk_index=chunk_index, 
    )

    all_chunks.extend(page_chunks)
    chunk_index += len(page_chunks)





