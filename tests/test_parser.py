# tests/test_parser.py
from app.parser import process_discharge_summary

def test_parser_basic_case():
    text = "The patient was diagnosed with pneumonia and prescribed azithromycin."
    result = process_discharge_summary(text)

    assert "diagnoses" in result and "medications" in result
    assert any("pneumonia" in d["text"].lower() for d in result["diagnoses"])
    assert any("azithromycin" in m["text"].lower() for m in result["medications"])
    assert all("cui" in d for d in result["diagnoses"])
    assert all("cui" in m for m in result["medications"])