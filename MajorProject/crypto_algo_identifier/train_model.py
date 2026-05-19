# import pandas as pd
# import joblib
# import numpy as np
# import os
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# from feature_extraction import extract_features

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Load dataset
# df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "crypto_samples.csv"))
# df.columns = df.columns.str.lower()

# X = []
# y = []

# for _, row in df.iterrows():
#     try:
#         data = bytes.fromhex(row["output"])
#         features = extract_features(data)
#         X.append(features)
#         y.append(row["algorithm"])
#     except:
#         continue

# X = np.array(X)

# # ✅ SCALE FEATURES
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

# # Split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# # ✅ STRONG MODEL (TUNED)
# model = RandomForestClassifier(
#     n_estimators=500,
#     max_depth=None,
#     min_samples_split=2,
#     random_state=42
# )

# model.fit(X_train, y_train)

# acc = model.score(X_test, y_test)
# print(f"🔥 Final Accuracy: {acc:.4f}")

# # Save
# joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
# joblib.dump(scaler, os.path.join(BASE_DIR, "scaler.pkl"))

# print("✅ model.pkl + scaler.pkl saved")

import pandas as pd
import numpy as np
import joblib
import warnings
import os

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

import xgboost as xgb

from feature_extraction import extract_features

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("🚀 Final Optimized Crypto Classifier")
print("=" * 50)

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv(
    os.path.join(BASE_DIR, "dataset", "crypto_samples.csv")
)

# Convert column names to lowercase
df.columns = df.columns.str.lower()

X = []
y = []

# =========================
# FEATURE EXTRACTION
# =========================
for _, row in df.iterrows():
    try:
        # Your dataset uses "output" + "algorithm"
        data = bytes.fromhex(row["output"])

        features = extract_features(data)

        X.append(features)
        y.append(row["algorithm"])

    except Exception as e:
        continue

X = np.array(X)
y = np.array(y)

print(f"✅ Samples Loaded: {len(X)}")

# =========================
# LABEL ENCODING
# =========================
le = LabelEncoder()
y = le.fit_transform(y)

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# =========================
# FEATURE SCALING
# =========================
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================
# XGBOOST MODEL
# =========================
print("\n⚡ Training XGBoost...")

xgb_model = xgb.XGBClassifier(
    n_estimators=1000,
    max_depth=12,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    eval_metric="mlogloss"
)

xgb_model.fit(X_train, y_train)

# =========================
# RANDOM FOREST MODEL
# =========================
print("🌲 Training Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=600,
    max_depth=30,
    random_state=42
)

rf_model.fit(X_train, y_train)

# =========================
# STACKING FEATURES
# =========================
print("🧠 Building Stacking Ensemble...")

xgb_train_p = xgb_model.predict_proba(X_train)
rf_train_p = rf_model.predict_proba(X_train)

xgb_test_p = xgb_model.predict_proba(X_test)
rf_test_p = rf_model.predict_proba(X_test)

X_train_stack = np.hstack([xgb_train_p, rf_train_p])
X_test_stack = np.hstack([xgb_test_p, rf_test_p])

# =========================
# META MODEL
# =========================
meta_model = RandomForestClassifier(
    n_estimators=400,
    max_depth=20,
    random_state=42
)

meta_model.fit(X_train_stack, y_train)

# =========================
# FINAL PREDICTIONS
# =========================
final_pred = meta_model.predict(X_test_stack)

acc = accuracy_score(y_test, final_pred)

print("\n🎯 FINAL ACCURACY:", round(acc * 100, 2), "%")

print("\n📊 Classification Report:\n")
print(
    classification_report(
        y_test,
        final_pred,
        target_names=le.classes_
    )
)

# =========================
# SAVE EVERYTHING
# =========================
joblib.dump(
    {
        "scaler": scaler,
        "xgb_model": xgb_model,
        "rf_model": rf_model,
        "meta_model": meta_model,
        "label_encoder": le
    },
    os.path.join(BASE_DIR, "final_model.pkl")
)

print("\n✅ final_model.pkl saved successfully")