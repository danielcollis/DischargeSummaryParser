# app/parser.py

import spacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker
from app.utils import clean_text

# Load the NER model – BC5CDR specializes in DISEASE and CHEMICAL recognition
nlp = spacy.load("en_ner_bc5cdr_md")

# Add abbreviation detector (if not already in the pipeline)
if "abbreviation_detector" not in nlp.pipe_names:
    nlp.add_pipe("abbreviation_detector")

# Add UMLS Entity Linker (if not already in the pipeline)
if "scispacy_linker" not in nlp.pipe_names:
    nlp.add_pipe("scispacy_linker", config={"linker_name": "umls", "resolve_abbreviations": True})
    
# Access the linker component directly
linker = nlp.get_pipe("scispacy_linker")

def process_discharge_summary(text: str) -> dict:
    """Extract diseases and medications with UMLS concept linking from discharge summary."""
    cleaned = clean_text(text)
    doc = nlp(cleaned)

    results = {
        "diagnoses": [],
        "medications": []
    }

    for ent in doc.ents:
        # Extract top UMLS CUI if available
        cui = None
        name = None
        if ent._.kb_ents:
            cui = ent._.kb_ents[0][0]
            name = linker.kb.cui_to_entity[cui].canonical_name

        structured_entity = {
            "text": ent.text,
            "cui": cui,
            "umls_name": name
        }

        if ent.label_.upper() == "DISEASE":
            results["diagnoses"].append(structured_entity)
        elif ent.label_.upper() == "CHEMICAL":
            results["medications"].append(structured_entity)

    return results