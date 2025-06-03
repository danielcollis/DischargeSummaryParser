# app/parser.py
import spacy
import scispacy
from app.utils import clean_text

# Load the SciSpaCy model
nlp = spacy.load("en_ner_bc5cdr_md")  # Handles diseases and chemicals

def process_discharge_summary(text: str) -> dict:
    """Process a discharge summary and return extracted medical entities."""
    cleaned = clean_text(text)
    # names entities in the discharge summary
    doc = nlp(cleaned)

    results = {
        "diagnoses": [],
        "medications": []
    }

    for ent in doc.ents:
        # goes through the doc object and assigns diseases and medications to the corresponding spot in the results dictionary
        if ent.label_.upper() == "DISEASE":
            results["diagnoses"].append(ent.text)
        elif ent.label_.upper() == "CHEMICAL":
            results["medications"].append(ent.text)

    return results