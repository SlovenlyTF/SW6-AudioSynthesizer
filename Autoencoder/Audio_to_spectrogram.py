import numpy as np
import matplotlib.pyplot as plt
import librosa


class AudioToSpectrogram:
  def __init__(self, n_fft=2048, hop_length=512, n_mels=128):
    self.n_fft = n_fft
    self.hop_length = hop_length
    self.n_mels = n_mels

  def __call__(self, audio):
    spectrogram = librosa.feature.melspectrogram(
        audio, n_fft=self.n_fft, hop_length=self.hop_length, n_mels=self.n_mels
    )
    spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    spectrogram = spectrogram.astype(np.float32)
    return spectrogram

  def plot(self, audio, spectrogram):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    librosa.display.waveshow(audio, alpha=0.5)
    plt.title("Wave")
    plt.subplot(1, 2, 2)
    librosa.display.specshow(spectrogram, x_axis="time", y_axis="mel")
    plt.title("Mel Spectrogram")
    plt.show()