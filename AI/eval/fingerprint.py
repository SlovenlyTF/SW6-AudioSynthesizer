#Fully made with chatgpt 3.5

import librosa
import numpy as np
from scipy.spatial.distance import cosine

def generate_fingerprint(audio_file):
    try:
        # Load audio file using librosa
        y, sr = librosa.load(audio_file, sr=None)

        # Extract features (e.g., Mel-frequency cepstral coefficients (MFCC))
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        # Calculate mean and standard deviation of MFCC along columns
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        # Combine mean and std into a single fingerprint
        fingerprint = np.concatenate((mfcc_mean, mfcc_std))

        # Normalize the fingerprint
        fingerprint = fingerprint / np.linalg.norm(fingerprint)

        return fingerprint
    except Exception as e:
        print(f"Error processing {audio_file}: {e}")
        return None

def compute_cosine_similarity(fingerprint1, fingerprint2):
    # Compute cosine similarity
    similarity_score = 1 - cosine(fingerprint1, fingerprint2)
    return similarity_score

# Example usage:
if __name__ == "__main__":
    audio_file1 = 'audio/postprocess/griffin_lim_mario.wav'  # Replace with your .wav file path
    audio_file2 = 'audio/postprocess/istft_mario.wav'  # Replace with your .wav file path

    fingerprint1 = generate_fingerprint(audio_file1)
    fingerprint2 = generate_fingerprint(audio_file2)

    if fingerprint1 is not None and fingerprint2 is not None:
        print("Audio fingerprint1:", fingerprint1)
        print("Audio fingerprint2:", fingerprint2)

        similarity_score = compute_cosine_similarity(fingerprint1, fingerprint2)
        print("Cosine similarity between the fingerprints:", similarity_score)
    else:
        print("Error generating fingerprints.")
