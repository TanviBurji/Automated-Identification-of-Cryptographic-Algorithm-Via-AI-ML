--> Automated Identification of Cryptographic Algorithms via AI/ML
An intelligent Machine Learning-based system that automatically identifies cryptographic algorithms from encrypted or hashed text samples using feature extraction and classification techniques.

📌 Project Overview
In modern cybersecurity systems, encrypted and hashed data are widely used to protect sensitive information. However, identifying the cryptographic algorithm used to generate a ciphertext or hash is often challenging because most outputs appear random and unreadable.
This project proposes an automated solution using Artificial Intelligence and Machine Learning techniques to classify cryptographic algorithms based on patterns and statistical properties extracted from ciphertext samples.
The system supports prediction of multiple cryptographic and hashing algorithms through a user-friendly web interface built with Flask.

🚀 Features
🔐 Automatic Cryptographic Algorithm Identification
🤖 AI/ML-Based Prediction System
📊 Feature Extraction from Ciphertext
🌐 Flask-Based Web Interface
📁 Dataset Generation and Training Support
📈 Ensemble Machine Learning Models
🧠 High Accuracy Classification
💻 Easy-to-Use User Interface
📚 Documentation Page Included

🛠️ Technologies Used
--> Backend
Python
Flask
Machine Learning
Scikit-learn
XGBoost
Random Forest
Support Vector Machine (SVM)
K-Nearest Neighbors (KNN)
Dataset & Processing
Pandas
NumPy

📂 Project Structure
crypto_algo_identifier/
│
├── dataset/
│   └── crypto_samples.csv
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── predict.html
│   └── documentation.html
│
├── app.py
├── train_model.py
├── predict_algorithm.py
├── feature_extraction.py
├── dataset_generator.py
├── model.pkl
├── scaler.pkl
├── final_model.pkl
├── dataset.csv
└── README.md
⚙️ Working Principle

--> The system works in the following stages:
1. Ciphertext Collection : Encrypted and hashed samples are collected/generated using different algorithms.
2. Feature Extraction : Statistical features such as entropy, character frequency, length, randomness, and distribution are extracted.
3. Model Training : Machine Learning algorithms are trained using extracted features.
4. Prediction : User inputs ciphertext/hash through the web interface.
The trained model predicts the most probable cryptographic algorithm.

🔍 Supported Algorithms
The project can identify algorithms such as:
AES
DES
RSA
Blowfish
MD5
SHA-1
SHA-256
Base64

🧠 Machine Learning Models Used
✅ Random Forest : Used as the primary ensemble learning model for high accuracy and robustness.

✅ Support Vector Machine (SVM) : Used for boundary-based classification.

✅ K-Nearest Neighbors (KNN) : Used for similarity-based prediction.

✅ XGBoost : Used for boosting and improved classification performance.

📊 Feature Extraction Parameters
The following features are extracted from ciphertext:

Text Length
Entropy
Character Frequency
Uppercase Count
Numeric Ratio
Symbol Ratio
Randomness Score
Distribution Patterns

💻 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/TanviBurji/Automated-Identification-of-Cryptographic-Algorithm-Via-AI-ML.git
2️⃣ Navigate to Project Directory
cd Automated-Identification-of-Cryptographic-Algorithm-Via-AI-ML
3️⃣ Create Virtual Environment (Optional)
python -m venv venv
4️⃣ Activate Virtual Environment
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
5️⃣ Install Dependencies
pip install -r requirements.txt
If requirements.txt is unavailable:
pip install flask pandas numpy scikit-learn xgboost
▶️ Running the Project
Run Flask Application
python app.py

Then open:
http://127.0.0.1:5000/
🏋️ Training the Model

To retrain the model:
python train_model.py

📈 Future Enhancements
Deep Learning Integration
Real-Time Packet Analysis
Larger Cryptographic Dataset
API-Based Detection System
Cloud Deployment
Blockchain Security Integration
Live Traffic Monitoring
Improved Accuracy with Hybrid Models

🎯 Applications
Cybersecurity Analysis
Digital Forensics
Threat Intelligence
Cryptographic Research
Malware Investigation
Security Auditing
Educational Research
