import numpy as np
import librosa
import os
import math
import soundfile as sf


class AudioProcessor:
  def __init__(self, sample_rate=22050, n_fft=2048, hop_length=512, n_mels=128, duration=2.97, mono=True, mode="constant", normalize_min=0, normalize_max=1, VAE=None):
    self.sample_rate = sample_rate
    self.n_fft = n_fft
    self.hop_length = hop_length
    self.n_mels = n_mels
    self.duration = duration
    self.mono = mono
    self.mode = mode
    self.normalize_min = normalize_min
    self.normalize_max = normalize_max
    self.vae = VAE


  def log_spectrogram(self, signal):
    stft = librosa.stft(signal, n_fft=self.n_fft, hop_length=self.hop_length)[:-1]
    spectrogram = np.abs(stft)
    log_spectrogram = librosa.amplitude_to_db(spectrogram)
    return log_spectrogram


  def right_pad(self, signal, duration, sr):
    num_missing_items = int(sr * duration) - len(signal)
    padded_signal = np.pad(signal, (0, num_missing_items), mode=self.mode)
    return padded_signal
  
  
  def load_signal(self, file_path):
    signal = librosa.load(file_path, sr=self.sample_rate, mono=self.mono)[0]
    return signal


  def split_signal(self, signal, duration, sr):
    audio_duration = len(signal) / sr
    segments = []
    for i in range(math.ceil(audio_duration / duration)):
      segments.append(signal[int(i * (sr * duration)):int((i + 1) * (sr * duration))])
    return segments


  def _file_processor(self, file_path):
    signal = self.load_signal(file_path)
    segments = self.split_signal(signal, self.duration, self.sample_rate)

    # Pad the last segment if it is shorter than the rest
    segment_length = len(segments)
    segments[segment_length-1] = self.right_pad(segments[segment_length-1], self.duration, self.sample_rate)

    spectrograms = [self.log_spectrogram(segment) for segment in segments]
    
    for i in range(len(spectrograms)):
      spectrograms[i] = self.normalizer(spectrograms[i])

    return spectrograms

  
  def create_spectrogram_from_dir(self, dir_path):
    spectrograms = []
    for file in os.listdir(dir_path):
      print(f"Processing {file}...")
      file_path = os.path.join(dir_path, file)
      spectrogram = self._file_processor(file_path)
      spectrograms.append(spectrogram)
      print(f"processed.")
    return spectrograms
  

  def save_audio(self, signal, file_path):
    file_path_name = os.path.join(file_path, "generated_audio.wav")
    sf.write(file_path_name, signal, self.sample_rate)
    print(f"Audio saved at {file_path}")


  def normalizer(self, signal):
    normalized_signal = (signal - signal.min()) / (signal.max() - signal.min())
    normalized_signal = normalized_signal * (self.normalize_max - self.normalize_min) + self.normalize_min
    return normalized_signal
  

  def denormalize(self, normalized_signal, original_signal_max=40, original_signal_min=-40):
    denormalized_signal = (normalized_signal - self.normalize_min) / (self.normalize_max - self.normalize_min)
    denormalized_signal = denormalized_signal * (original_signal_max - original_signal_min) + original_signal_min
    return denormalized_signal


  def generate(self, spectrograms):
    generated_spectrograms, latent_space = self.vae.reconstruct(spectrograms)
    signals = self.convert_spectrogram_to_signal(generated_spectrograms)
    return signals, latent_space


  def convert_spectrogram_to_signal(self, spectrograms):
    signals = []
    for spectrogram in spectrograms:
      log_spectrogram = spectrogram[:, :, 0]
      denomilized_spectrogram = self.denormalize(log_spectrogram)
      spec = librosa.db_to_amplitude(denomilized_spectrogram)
      signal = librosa.istft(spec, hop_length=self.hop_length)
      signals.append(signal)
    signals = np.array(signals)
    signals = np.concatenate(signals, axis=0)
    print(f"min: {np.min(signals)}, max: {np.max(signals)}")
    print(f"Generated {len(signals)} samples.")
    return signals