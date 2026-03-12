# The following modules and libraries are used for file handling and document processing.
import os 
from pathlib import Path
from typing import Any

import pdfplumber 
from docx import Document

#The following code is for the PDF loader, which extracts text from PDF files using the pdfplumber library.

def load_pdf(file_path: str) -> list[dict[str, any]]:

   "Starts with an extraction of text from a PDF file. "
   "It uses the pdfplumber library to open the PDF and iterate through its pages. "
   "For each page, it extracts the text and checks if it is not empty or just whitespace. "
   "If the text is valid, it cleans the text using the _clean_page_text function and appends a dictionary containing the cleaned text, page number, source name, and file type to the pages list. Finally, it returns the list of pages."
   
   
   pages = []
   with pdfplumber.open(file_path) as pdf: 
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            # pdfplomber returns None for the image-only pages
            if not text or not text.strip():
                continue


            text = _clean_page_text(text)

            if text.strip():
                pages.append({
                    "text": text, 
                    "page_number": i + 1, 
                    "source": source_name, 
                    "file_type": "pdf"
                })
                
        return_pages