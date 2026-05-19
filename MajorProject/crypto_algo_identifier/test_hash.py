import pandas as pd
import joblib
import os
from feature_extraction import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ LOAD MODEL (THIS WAS MISSING)
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

# ✅ LOAD DATASET
df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "crypto_samples.csv"))

# ✅ Allowed classes
ALLOWED = list(model.classes_)

correct = 0
total = 0

for _, row in df.sample(100).iterrows():

    true_label = row['algorithm']

    # ✅ Skip unknown labels
    if true_label not in ALLOWED:
        continue

    try:
        data = bytes.fromhex(row['output'])
    except:
        continue

    pred = model.predict([extract_features(data)])[0]

    print(f"TRUE: {true_label} | PRED: {pred}")

    if pred == true_label:
        correct += 1

    total += 1

# ✅ Avoid division error
if total > 0:
    print(f"\n✅ Filtered Accuracy: {(correct/total)*100:.2f}%")
else:
    print("❌ No valid samples found")