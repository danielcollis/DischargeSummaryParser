import json
import requests
from collections import defaultdict
from sklearn.metrics import precision_score, recall_score, f1_score
import os
from sklearn.metrics import precision_recall_fscore_support

# --- Configuration ---
API_URL = "http://localhost:8000/parse"
EVAL_FILE = os.path.join(os.path.dirname(__file__), "evaluation_set_new.json")

# --- Load Evaluation Data ---
with open(EVAL_FILE, "r") as f:
    eval_data = json.load(f)

# --- Initialize Metrics ---
y_true = {"diagnoses": [], "medications": []}
y_pred = {"diagnoses": [], "medications": []}

# --- Normalize helper ---
def normalize_entity(ent):
    return (ent["text"].lower(), (ent.get("cui") or "").lower())

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
        
        # Tally true positives, false positives, false negatives
        tp = len(predicted_set & expected_set)
        fp = len(predicted_set - expected_set)
        fn = len(expected_set - predicted_set)

        # Print per-sample metrics (optional)
        all_entities = list(expected_set.union(predicted_set))
        y_true_vec = [int(ent in expected_set) for ent in all_entities]
        y_pred_vec = [int(ent in predicted_set) for ent in all_entities]
        p, r, f1, _ = precision_recall_fscore_support(y_true_vec, y_pred_vec, average='binary', zero_division=0)

        print(f"{sample['id']} - {category.capitalize()}:")
        print(f"  TP={tp}, FP={fp}, FN={fn}")
        print(f"  Precision={p:.2f}, Recall={r:.2f}, F1={f1:.2f}")

        # Aggregate for global scoring
        y_true[category].extend(y_true_vec)
        y_pred[category].extend(y_pred_vec)


# --- Calculate & Print Scores ---
for category in ["diagnoses", "medications"]:
    p = precision_score(y_true[category], y_pred[category])
    r = recall_score(y_true[category], y_pred[category])
    f1 = f1_score(y_true[category], y_pred[category])
    print(f"\nCategory: {category.capitalize()}")
    print(f"Precision: {p:.2f}")
    print(f"Recall:    {r:.2f}")
    print(f"F1 Score:  {f1:.2f}")