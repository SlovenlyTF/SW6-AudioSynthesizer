#Fully made with chatgpt 3.5

import numpy as np
import matplotlib.pyplot as plt
import pywt
import scipy.io.wavfile as wav
import warnings

# Suppress WavFileWarning
warnings.filterwarnings("ignore", category=wav.WavFileWarning)

# Load .wav files
sampling_rate1, signal1 = wav.read('audio/generated_piano_til_ssim.wav')
sampling_rate2, signal2 = wav.read('audio/piano_fra_youtube_til_ssim.wav')

# Convert stereo to mono if necessary
if signal1.ndim > 1:
    signal1 = signal1.mean(axis=1)
if signal2.ndim > 1:
    signal2 = signal2.mean(axis=1)

# Ensure signals are the same length (truncate the longer one)
min_length = min(len(signal1), len(signal2))
signal1 = signal1[:min_length]
signal2 = signal2[:min_length]

# Parameters for Continuous Wavelet Transform
wavelet = 'morl'  # Morlet wavelet
scales = np.arange(1, 128)  # Scales for CWT

# Perform Continuous Wavelet Transform (CWT)
coeffs1, freqs1 = pywt.cwt(signal1, scales, wavelet, sampling_period=1/sampling_rate1)
coeffs2, freqs2 = pywt.cwt(signal2, scales, wavelet, sampling_period=1/sampling_rate2)

# Calculate wavelet coherence
def wavelet_coherence(cwt1, cwt2):
    numerator = np.abs(np.mean(cwt1 * np.conj(cwt2), axis=1))**2
    denominator = np.mean(np.abs(cwt1)**2, axis=1) * np.mean(np.abs(cwt2)**2, axis=1)
    return numerator / denominator

Wxy = wavelet_coherence(coeffs1, coeffs2)

# Plotting
plt.figure(figsize=(10, 6))

# Plot scalograms
plt.subplot(2, 2, 1)
plt.imshow(np.abs(coeffs1), extent=[0, len(signal1)/sampling_rate1, scales.min(), scales.max()], aspect='auto', cmap='jet')
plt.title('Scalogram of Signal 1')
plt.ylabel('Scale')
plt.xlabel('Time (s)')

plt.subplot(2, 2, 3)
plt.imshow(np.abs(coeffs2), extent=[0, len(signal2)/sampling_rate2, scales.min(), scales.max()], aspect='auto', cmap='jet')
plt.title('Scalogram of Signal 2')
plt.ylabel('Scale')
plt.xlabel('Time (s)')

# Plot coherogram (wavelet coherence)
plt.subplot(1, 2, 2)
plt.imshow(Wxy[:, np.newaxis], extent=[0, 1, freqs1.min(), freqs1.max()], aspect='auto', cmap='jet')
plt.title('Wavelet Coherence')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time')

plt.tight_layout()
plt.show()
