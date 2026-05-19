import numpy as np
import math

def extract_features(data):

    byte_array = np.frombuffer(data, dtype=np.uint8)
    length = len(byte_array)

    # Guard against empty input
    if length == 0:
        return [0.0] * 43

    features = []

    # =========================
    # BASIC FEATURES
    # =========================
    features.append(np.mean(byte_array))
    features.append(np.std(byte_array))
    features.append(length)
    features.append(len(set(byte_array)))
    features.append(np.max(byte_array))
    features.append(np.min(byte_array))

    # =========================
    # ENTROPY (IMPORTANT)
    # =========================
    hist, _ = np.histogram(byte_array, bins=256, range=(0, 255))
    prob = hist / np.sum(hist)
    entropy = -sum(p * math.log2(p) for p in prob if p > 0)
    features.append(entropy)

    # =========================
    # BLOCK SIZE FEATURES 🔥
    # =========================
    features.append(length % 8)   # DES / 3DES
    features.append(length % 16)  # AES

    # =========================
    # BYTE DISTRIBUTION FEATURES
    # =========================
    features.append(np.percentile(byte_array, 25))
    features.append(np.percentile(byte_array, 50))
    features.append(np.percentile(byte_array, 75))

    # =========================
    # HISTOGRAM (REDUCED BUT SMART)
    # =========================
    hist, _ = np.histogram(byte_array, bins=32, range=(0, 255))
    features.extend(hist)

    return features