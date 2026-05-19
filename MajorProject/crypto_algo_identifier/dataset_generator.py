import pandas as pd
import os
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import MD5, SHA256
from Crypto.Util.Padding import pad

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = []

def to_hex(b):
    return b.hex()

# AES
for _ in range(200):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    pt = get_random_bytes(32)
    ct = cipher.encrypt(pad(pt, 16))
    data.append([to_hex(ct), "AES"])

# DES
for _ in range(200):
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_ECB)
    pt = get_random_bytes(16)
    ct = cipher.encrypt(pad(pt, 8))
    data.append([to_hex(ct), "DES"])

# RSA
key = RSA.generate(2048)
cipher_rsa = PKCS1_OAEP.new(key.publickey())

for _ in range(200):
    pt = get_random_bytes(32)
    ct = cipher_rsa.encrypt(pt)
    data.append([to_hex(ct), "RSA"])

# MD5
for _ in range(200):
    pt = get_random_bytes(32)
    h = MD5.new(pt)
    data.append([to_hex(h.digest()), "MD5"])

# SHA256
for _ in range(200):
    pt = get_random_bytes(32)
    h = SHA256.new(pt)
    data.append([to_hex(h.digest()), "SHA256"])

df = pd.DataFrame(data, columns=["output", "algorithm"])
dataset_path = os.path.join(BASE_DIR, "dataset", "crypto_samples.csv")
df.to_csv(dataset_path, index=False)

print(f"✅ dataset saved to {dataset_path}")
