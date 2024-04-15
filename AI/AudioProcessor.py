import numpy as np
import librosa
import os
import math
import soundfile as sf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from torchvision.utils import save_image
import torch


class AudioProcessor:
  def __init__(self, sample_rate=22050, n_fft=2048, hop_length=512, n_mels=128, duration=2.97, mono=True, mode="constant", model=None):
    self.sample_rate = sample_rate
    self.n_fft = n_fft
    self.hop_length = hop_length
    self.n_mels = n_mels
    self.duration = duration
    self.mono = mono
    self.mode = mode
    self.normalize_min = 0
    self.normalize_max = 1
    self.model = model
    self.signal_max = 100
    self.signal_min = -100


  def log_spectrogram(self, signal, idx, log):
    stft = librosa.stft(signal, n_fft=self.n_fft, hop_length=self.hop_length)[:-1]
    spectrogram = np.abs(stft)
    log_spectrogram = librosa.amplitude_to_db(spectrogram)

    if log is not None:
      self._plot_spectrogram_from_signal(signal, False, f"segment_{idx+1}", log)

      log[1].write(f"Spectrogram min: {spectrogram.min()}, Spectrogram max: {spectrogram.max()}\n")
      log[1].write(f"Log Spectrogram min: {log_spectrogram.min()}, Log Spectrogram max: {log_spectrogram.max()}\n")
      log[1].write("\n\n")
    return log_spectrogram


  def right_pad(self, signal, duration, sr):
    num_missing_items = int(sr * duration) - len(signal)
    padded_signal = np.pad(signal, (0, num_missing_items), mode=self.mode)
    return padded_signal


  def load_signal(self, file_path, log):
    signal, sr = librosa.load(file_path, mono=self.mono)
    if sr != self.sample_rate:
      signal = librosa.resample(signal, sr, self.sample_rate)
      if log is not None:
        log[1].write(f"Resampling signal from {sr} to {self.sample_rate}\n")
        log[1].write(f"\n\n")
    return signal


  def split_signal(self, signal, duration, sr):
    audio_duration = len(signal) / sr
    segments = []
    for i in range(math.ceil(audio_duration / duration)):
      segments.append(signal[int(i * (sr * duration)):int((i + 1) * (sr * duration))])
    return segments

  
  def _plot_spectrogram_from_signal(self, signal, already_spectrogram, name, log):
    if not already_spectrogram:
      stft = librosa.stft(signal, n_fft=self.n_fft, hop_length=self.hop_length)[:-1]
      spectrogram = np.abs(stft)
      log_spectrogram = librosa.amplitude_to_db(spectrogram)
    else:
      log_spectrogram = signal

    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    p = librosa.display.specshow(log_spectrogram, ax=ax, y_axis='log', x_axis='time')
    fig.savefig(f"{log[0]}/{name}.png")


  def _file_processor(self, file_path, log):
    signal = self.load_signal(file_path, log=log)
    segments = self.split_signal(signal, self.duration, self.sample_rate)

    if log is not None:
      self._plot_spectrogram_from_signal(signal, False, "Pre_nomalize_full_signal", log)

      plot_segments = segments[0:-1]
      plot_segments = np.concatenate(plot_segments, axis=0)
      self._plot_spectrogram_from_signal(plot_segments, False, "Pre_nomalize_no_pad_segments", log)

      log[1].write(f"Pre_nomalize_Full signal of file {file_path}\n")
      log[1].write(f"Signal min: {signal.min()}, Signal max: {signal.max()}\n")
      log[1].write(f"Length of signal: {len(signal)}\n")
      log[1].write(f"Duration of signal: {len(signal) / self.sample_rate}\n")
      log[1].write(f"Number of segments: {len(segments)}\n")
      log[1].write(f"Duration of last segment: {len(segments[-1]) / self.sample_rate}\n")
      log[1].write("\n\n")

    # Pad the last segment if it is shorter than the rest
    # if len(segments[-1]) < self.sample_rate * self.duration:
    #   segments.pop()
    segment_length = len(segments)
    segments[-1] = self.right_pad(segments[-1], self.duration, self.sample_rate)

    spectrograms = [self.log_spectrogram(segment, idx, log=log) for idx, segment in enumerate(segments)]
    for i in range(len(spectrograms)):
      spectrograms[i] = self.normalizer(spectrograms[i], i, log=log)
    return spectrograms

  
  def create_spectrogram_from_dir(self, dir_path, log):
    spectrograms = []
    for i, file in enumerate(os.listdir(dir_path)):
      file_path = os.path.join(dir_path, file)
      spectrogram = self._file_processor(file_path, log=log)
      spectrograms.append(spectrogram)
      print(f"({i + 1} of {len(os.listdir(dir_path))}) Processed: {file}")
    return spectrograms
  

  def save_audio(self, signal, file_path):
    file_path_name = os.path.join(file_path, "generated_audio.wav")
    sf.write(file_path_name, signal, self.sample_rate)
    print(f"Audio saved at {file_path}")


  def normalizer(self, signal, idx, log):
    if (signal.max() - signal.min()) == 0:
      print("Warning: Normalization failed. Returning original signal.")
      return signal
    normalized_signal = (signal - self.signal_min) / (self.signal_max - self.signal_min)
    normalized_signal = normalized_signal * (self.normalize_max - self.normalize_min) + self.normalize_min
    # normalized_signal = (signal - signal.min()) / (signal.max() - signal.min())
    # normalized_signal = normalized_signal * (self.normalize_max - self.normalize_min) + self.normalize_min

    if log is not None:
      log[1].write(f"Normalization of segment {idx+1}\n")
      log[1].write(f"Signal min: {signal.min()}, Signal max: {signal.max()}\n")

      if (signal.max() - signal.min()) == 0:
        log[1].write(f"Warning: Normalization failed. Returning original signal.\n")
      else:
        log[1].write(f"Self.signal min: {self.signal_min}, Self.signal max: {self.signal_max}\n")
        log[1].write(f"Normalized signal min: {normalized_signal.min()}, Normalized signal max: {normalized_signal.max()}\n")
      
      log[1].write("\n\n")


      # reshape numpy array from (1024, 128, 1) to list of tensor with shape (1, 1024, 128)
      np_arr = normalized_signal.reshape(1024, 128)
      tensor = torch.from_numpy(np_arr)
      if tensor.dtype == torch.int:
        tensor = tensor.float()  # Convert integers to float if necessary
      save_image(tensor + 0.5, f"{log[0]}/orignal_signal_grayscale_segment_{idx+1}.png")

    return normalized_signal
  

  def denormalize(self, normalized_signal, idx, log):
    denormalized_signal = (normalized_signal - self.normalize_min) / (self.normalize_max - self.normalize_min)
    denormalized_signal = denormalized_signal * (self.signal_max - self.signal_min) + self.signal_min

    if log is not None:
      log[1].write(f"Denormalization of segment {idx+1}\n")
      log[1].write(f"Normalized signal min: {normalized_signal.min()}, Normalized signal max: {normalized_signal.max()}\n")
      log[1].write(f"Self.signal min: {self.signal_min}, Self.signal max: {self.signal_max}\n")
      log[1].write(f"Denormalized signal min: {denormalized_signal.min()}, Denormalized signal max: {denormalized_signal.max()}\n")
      log[1].write("\n\n")

    return denormalized_signal


  def generate(self, spectrograms):
    if self.model is None:
      print("Model not found. Please provide a model.")
      return None
    generated_spectrograms, latent_space = self.model.reconstruct(spectrograms)
    signals = self.convert_spectrogram_to_signal(generated_spectrograms)
    return signals, latent_space

  

  def convert_spectrogram_to_signal(self, spectrograms, log = None):
    spec = []
    for idx, spectrogram in enumerate(spectrograms):
      log_spectrogram = spectrogram[:, :, 0]
      denomilized_spectrogram = self.denormalize(log_spectrogram, idx, log=log)

      spec.append(denomilized_spectrogram)
    spec = np.array(spec)
    spec_full = np.concatenate(spec, axis=1)
    spec_full = librosa.db_to_amplitude(spec_full)

    if spec_full.dtype == np.float16:
      spec_full = spec_full.astype(np.float32)

    signal = librosa.istft(spec_full, hop_length=self.hop_length)

    if log is not None:
      self._plot_spectrogram_from_signal(signal, False, "denomalized_ISTFT_full_signal", log)
      
      plot_segments = spec[0:-1]
      plot_segments = np.concatenate(plot_segments, axis=1)
      self._plot_spectrogram_from_signal(plot_segments, True, "denomalize_no_pad_segments", log)

      log[1].write(f"Denomalized full signal\n")
      log[1].write(f"Signal min: {signal.min()}, Signal max: {signal.max()}\n")
      log[1].write(f"Length of signal: {len(signal)}\n")
      log[1].write("\n\n")

    return signal