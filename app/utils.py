# app/utils.py

import re

def clean_text(text: str) -> str:
    """Simple cleaner to normalize spacing and newlines."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()