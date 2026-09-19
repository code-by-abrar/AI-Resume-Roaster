"""
parser.py
---------
Resume PDF se text extract karne ka module.
Primary: pdfplumber (better accuracy)
Fallback: PyPDF2
"""

import pdfplumber
import PyPDF2
import io


def extract_text_pdfplumber(pdf_bytes: bytes) -> str:
    """
    pdfplumber se text extract karo.
    Tables aur complex layouts ke saath better kaam karta hai.
    """
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"pdfplumber error: {str(e)}")
    return text.strip()


def extract_text_pypdf2(pdf_bytes: bytes) -> str:
    """
    PyPDF2 fallback extractor.
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"PyPDF2 error: {str(e)}")
    return text.strip()


def parse_resume(pdf_bytes: bytes) -> str:
    """
    Main parser function.
    pdfplumber try karo, fail ho toh PyPDF2 use karo.
    """
    # First attempt: pdfplumber
    try:
        text = extract_text_pdfplumber(pdf_bytes)
        if text and len(text) > 50:
            return text
    except Exception:
        pass

    # Fallback: PyPDF2
    try:
        text = extract_text_pypdf2(pdf_bytes)
        if text and len(text) > 50:
            return text
    except Exception:
        pass

    raise ValueError("Resume se text extract nahi ho saka. PDF valid hai?")
