import hashlib
import joblib
import os
from feature_extraction import extract_features

from Crypto.Cipher import AES, DES, DES3, Blowfish
from Crypto.PublicKey import RSA, ECC
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

# =========================
# 🔍 Prediction function
# =========================
def predict(hex_data):
    data_bytes = bytes.fromhex(hex_data)
    features = extract_features(data_bytes)
    return model.predict([features])[0]

# =========================
# 🔐 Test Plaintext
# =========================
data = b"Hi you are hacked!"

print("\n===== 🔐 TESTING ALL ALGORITHMS =====\n")

# =========================
# HASH
# =========================
md5 = hashlib.md5(data).hexdigest()
print("MD5:", md5)


sha = hashlib.sha256(data).hexdigest()
print("SHA-256:", sha)


# =========================
# AES
# =========================
aes_key = get_random_bytes(16)
aes_cipher = AES.new(aes_key, AES.MODE_ECB)
aes_ct = aes_cipher.encrypt(pad(data, 16)).hex()

print("AES:", aes_ct)


# =========================
# DES
# =========================
des_key = get_random_bytes(8)
des_cipher = DES.new(des_key, DES.MODE_ECB)
des_ct = des_cipher.encrypt(pad(data, 8)).hex()

print("DES:", des_ct)


# =========================
# 3DES
# =========================
des3_key = DES3.adjust_key_parity(get_random_bytes(24))
des3_cipher = DES3.new(des3_key, DES3.MODE_ECB)
des3_ct = des3_cipher.encrypt(pad(data, 8)).hex()

print("3DES:", des3_ct)


# =========================
# Blowfish
# =========================
blow_key = get_random_bytes(16)
blow_cipher = Blowfish.new(blow_key, Blowfish.MODE_ECB)
blow_ct = blow_cipher.encrypt(pad(data, 8)).hex()

print("Blowfish:", blow_ct)


# =========================
# RSA
# =========================
rsa_key = RSA.generate(1024)
rsa_ct = pow(int.from_bytes(data, 'big'), rsa_key.e, rsa_key.n).to_bytes(128, 'big').hex()

print("RSA:", rsa_ct)


# =========================
# ECC (structured simulation)
# =========================
ecc_key = ECC.generate(curve='P-256')
ecc_ct = ecc_key.public_key().export_key(format='DER')[:64].hex()

print("ECC:", ecc_ct)
