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

# Strips the common header and footer text from the page text.
# Documents often have confidential plastered across the top and bottom of each page, which can interfere with the quality of the extracted text.
            text = _clean_page_text(text)

            if text.strip():
                pages.append({
                    "text": text, 
                    "page_number": i + 1, # indexed the number of the page starting from 1, which is more intuitive for users than starting from 0.
                    "source": source_name, 
                    "file_type": "pdf"
                })
                
        return_pages

# The following code is for the DOCX loader, which extracts text from DOCX files using the python-docx library.

def load_docx(file_path:str) -> list[dict[str, any]]: 
    """ The load_docx function is designed to extract text from a DOCX file and organize it into virtual pages based on a specified page size. It uses the python-docx library to read the DOCX file and iterates through its paragraphs to accumulate text until it reaches the defined virtual page size. Each virtual page is then stored as a dictionary containing the text, page number, source name, and file type. Finally, the function returns a list of these virtual pages."""

    source_name = Path(file_path).name
    doc = Document(file_path)


    pages = []
    current_text = []
    current_length = 0
    virtual_page_number = 1
    virtual_page_size = 3000 #Characters per the virtual page, which is a common size for LLMs to process effectively. This can be adjusted based on the specific requirements of the application or the capabilities of the LLM being used.

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        current_text.append(text)
        current_length += len(text)
# Once the accumulated text reaches or exceeds the defined virtual page size, it creates a new virtual page by joining the accumulated text and appending it to the pages list as a dictionary. The current text and length are then reset, and the virtual page number is incremented for the next page. This process continues until all paragraphs have been processed, and any remaining text is added as a final virtual page if it exists.
        if current_length >= virtual_page_size:
            pages.append({
                "text": "\n".join(current_text), 
                "page_number": virtual_page_number, 
                "source": source_name, 
                "file_type": "docx"
            }) 
 # Flush any remaining text as a final page if it exists. This ensures that any text that did not reach the virtual page size threshold is still included in the output as a separate page.
            current_text = []
            current_length = 0
            virtual_page_number += 1

    if current_text: 
        pages.append({
                "text": "\n".join(current_text), 
                "page_number": virtual_page_number, 
                "source": source_name, 
                "file_type": "docx"
            }) 
        
    return pages

# The following code is for the main loader function, which determines the file type and calls the appropriate loader function based on the file extension. It also includes a function to load all supported documents from a directory.

def load_document(file_path: str) -> list[dict[str, any]]: 

    path = Path(file_path)

    if not path.exists(): 
        raise FileNotFoundError(f"Document not found: {file_path}")
    suffix = path.suffix.lower()

    if suffix == ".pdf": 
        return load_pdf(file_path)
    
    elif suffix in (".docx", ".doc"):
        return load_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    
def load_directory(dir_path: str) -> list[dict[str, any]]:
    dir_path = Path(dir_path)
    all_pages = []
    supported_extensions = {".pdf", ".docx", ".doc"}

    files = [
        f for f in dir_path.iterdir()
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]

    if not files: 
        raise ValueError(f"No supported files found in directory: {dir_path}")
    
    for file in sorted(files):
        print(f" Loading: {file.name}")
        pages = load_document(str(file))
        all_pages.extend(pages)
        print(f"    → {len(pages)} pages extracted")
    
    return all_pages

# Helper function to clean page text by removing common headers and footers. This is a simple implementation that can be expanded based on specific document formats or patterns.
