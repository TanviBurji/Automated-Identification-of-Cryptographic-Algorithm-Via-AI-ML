from flask import Flask, render_template, request
import numpy as np
import joblib
import os
from feature_extraction import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

app = Flask(__name__)

# =========================
# EXPLANATION ENGINE
# =========================
def explain_algorithm(prediction, features):
    explanation = []

    explanation.append(f"Mean: {features[0]:.2f}")
    explanation.append(f"Std Dev: {features[1]:.2f}")
    explanation.append(f"Length: {features[2]}")
    explanation.append(f"Unique Bytes: {features[3]}")
    explanation.append(f"Max Byte: {features[4]}")
    explanation.append(f"Min Byte: {features[5]}")

    if features[1] > 70:
        explanation.append("High variation → Likely encryption (AES/RSA)")
    elif features[1] > 40:
        explanation.append("Moderate variation → Possibly DES")
    else:
        explanation.append("Low variation → Possibly hashing")

    explanation.append(f"Predicted Algorithm: {prediction}")

    return explanation


# =========================
# IDENTIFY FUNCTION
# =========================
def identify(data_bytes):
    features = extract_features(data_bytes)

    X = np.array(features).reshape(1, -1)
    X = scaler.transform(X)

    prediction = model.predict(X)[0]
    probs = model.predict_proba(X)[0]

    labels = model.classes_
    prob_values = probs * 100
    confidence = max(prob_values)

    explanations = explain_algorithm(prediction, features)

    return prediction, confidence, labels, prob_values, explanations


# =========================
# ROUTES
# =========================

# 🏠 HOME PAGE
@app.route("/")
def home():
    return render_template("home.html")


# 🔍 PREDICTION PAGE
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        input_data = request.form.get("cipher", "")
        uploaded_file = request.files.get("file")

        data_bytes = b""

        # File input
        if uploaded_file and uploaded_file.filename != "":
            try:
                data_bytes = uploaded_file.read()
            except Exception as e:
                return render_template("predict.html", error=f"File error: {e}")

        # HEX input
        elif input_data.strip():
            try:
                data_bytes = bytes.fromhex(input_data.strip())
            except:
                return render_template("predict.html", error="Invalid HEX input")

        else:
            return render_template("predict.html", error="Enter HEX or upload file")

        if len(data_bytes) == 0:
            return render_template("predict.html", error="Empty input")

        prediction, confidence, labels, prob_values, explanations = identify(data_bytes)

        return render_template(
            "predict.html",
            result={
                "prediction": prediction,
                "confidence": round(confidence, 2),
                "labels": list(labels),
                "prob_values": [round(v, 2) for v in prob_values],
                "explanations": explanations
            }
        )

    return render_template("predict.html")


# 📚 DOCUMENTATION PAGE
@app.route("/documentation")
def documentation():
    return render_template("documentation.html")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)