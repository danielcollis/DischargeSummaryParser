# app/parser.py
import spacy
import scispacy
from scispacy.umls_linking import UmlsEntityLinker
from app.utils import clean_text

# Load the SciSpaCy model
nlp = spacy.load("en_ner_bc5cdr_md")  # Handles diseases and chemicals

# Register the extension attribute
if not spacy.tokens.Span.has_extension("umls_ents"):
    spacy.tokens.Span.set_extension("umls_ents", default=None)

# adds the umls entity linker to the pipeline
if "scispacy_linker" not in nlp.pipe_names:
    linker = UmlsEntityLinker(
        resolve_abbreviations=True,
        max_entities_per_mention=3,
        threshold=0.7,  # Lower threshold to get more matches
        filter_for_definitions=False  # Don't filter out entities without definitions
    )
    nlp.add_pipe("scispacy_linker", config={
        "resolve_abbreviations": True,
        "max_entities_per_mention": 3,
        "threshold": 0.7,
        "filter_for_definitions": False
    })


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
        cui = None
        if ent._.umls_ents:
            # Get the first UMLS entity with its score
            umls_ent = ent._.umls_ents[0]
            cui = umls_ent[0]  # The CUI is the first element
            score = umls_ent[1]  # The score is the second element
            
        item = {
            "text": ent.text,
            "cui": cui,
            "type": ent.label_
        }
        
        # goes through the doc object and assigns diseases and medications to the corresponding spot in the results dictionary
        if ent.label_.upper() == "DISEASE":
            results["diagnoses"].append(item)
        elif ent.label_.upper() == "CHEMICAL":
            results["medications"].append(item)

    return results