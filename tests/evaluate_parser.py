import json
import requests
from collections import defaultdict
from sklearn.metrics import precision_score, recall_score, f1_score
import os

# --- Configuration ---
API_URL = "http://localhost:8000/parse"
EVAL_FILE = os.path.join(os.path.dirname(__file__), "evaluation_set.json")

# --- Load Evaluation Data ---
with open(EVAL_FILE, "r") as f:
    eval_data = json.load(f)

# --- Initialize Metrics ---
y_true = {"diagnoses": [], "medications": []}
y_pred = {"diagnoses": [], "medications": []}

# --- Normalize helper ---
def normalize_entity(ent):
    return (ent["text"].lower(), ent.get("cui", "").lower())

# --- Evaluate Each Sample ---
for sample in eval_data:
    text = sample["text"]
    expected = sample["expected"]

    try:
        response = requests.post(API_URL, json={"summary": text})
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(f"Error processing sample {sample['id']}: {e}")
        continue

    for category in ["diagnoses", "medications"]:
        expected_set = {normalize_entity(e) for e in expected.get(category, [])}
        predicted_set = {normalize_entity(e) for e in result.get(category, [])}

        # Record for metrics: one-hot entity match list
        all_entities = list(expected_set.union(predicted_set))
        for ent in all_entities:
            y_true[category].append(int(ent in expected_set))
            y_pred[category].append(int(ent in predicted_set))

# --- Calculate & Print Scores ---
for category in ["diagnoses", "medications"]:
    p = precision_score(y_true[category], y_pred[category])
    r = recall_score(y_true[category], y_pred[category])
    f1 = f1_score(y_true[category], y_pred[category])
    print(f"\nCategory: {category.capitalize()}")
    print(f"Precision: {p:.2f}")
    print(f"Recall:    {r:.2f}")
    print(f"F1 Score:  {f1:.2f}")
