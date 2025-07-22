# AI-Driven Discharge Summary Parser

## 🧠 Overview

The **AI-Driven Discharge Summary Parser** is a web-based NLP tool that extracts structured clinical data (diagnoses, medications, etc.) from unstructured hospital discharge summaries. Using **spaCy**, **SciSpaCy**, and **UMLS** linking, the system standardizes medical information to support interoperability across healthcare systems.

Built with a **FastAPI backend** and **React frontend**, the parser takes user input in natural language and returns structured JSON containing:

- Extracted clinical entities (e.g., diseases, medications)
- Corresponding UMLS Concept Unique Identifiers (CUIs)
- Entity types (e.g., Diagnosis, Drug)

---

## 🚀 Features

- 🔎 Named Entity Recognition using `en_ner_bc5cdr_md` and `en_core_sci_md`
- 🔗 Entity linking with SciSpaCy’s UMLS EntityLinker
- 🧼 Text cleaning and abbreviation expansion
- 📦 FastAPI backend with `/ping` and `/parse` endpoints
- 🖥️ Simple React interface (Vite) for testing the parser
- 🧪 Unit tested with `pytest`

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/discharge-summary-parser.git
cd discharge-summary-parser
```

### 2. Set Up a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

> Ensure that `en_ner_bc5cdr_md` and `en_core_sci_md` are downloaded from their provided URLs.

### 4. Start the Backend

```bash
uvicorn app.main:app --reload
```

### 5. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Example Output

Paste a discharge summary like this:

```
The patient was diagnosed with community-acquired pneumonia and discharged on azithromycin.
```

You will receive structured JSON output:

```json
{
  "entities": [
    {
      "text": "community-acquired pneumonia",
      "umls_cui": "C0004626",
      "umls_name": "Pneumonia",
      "type": "Diagnosis"
    },
    {
      "text": "azithromycin",
      "umls_cui": "C0678222",
      "umls_name": "Azithromycin",
      "type": "Medication"
    }
  ]
}
```

---

## 🧪 Testing

Run unit tests with:

```bash
pytest
```

Tests include:

- Parsing pipeline validation
- Entity linking edge cases
- API endpoint integration

---

## 📝 Research Paper

This project is academically grounded. You can find the full research paper in the [`/docs`](docs) folder:

👉 [ResearchPaper.pdf](docs/ResearchPaper.pdf)

---

## 📌 Future Improvements

- Add export to CSV/FHIR
- Improve entity disambiguation and negation detection
- Enhance evaluation with expert-annotated datasets
- Deploy to a HIPAA-compliant cloud service

---

## 👨‍⚕️ Disclaimer

This is a proof-of-concept academic project. It is **not** intended for clinical use without medical expert oversight.

---

## 📚 References

Key technologies and papers referenced in this project:

- [SciSpaCy Documentation](https://allenai.github.io/scispacy/)
- [UMLS Knowledge Base](https://www.nlm.nih.gov/research/umls/)
- Siepmann et al., Healthcare Analytics, 2025
- Navarro et al., IJMI, 2023

---

## 🧑‍💻 Author

Daniel Collis\
Senior Project – University of North Georgia

