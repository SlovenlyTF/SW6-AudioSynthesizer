import librosa
import numpy as np
import os
import pickle


class Loader:
  """
  This class is responsible for loading the audio files from the disk.
  """

  def __init__(self, sample_rate=22050, duration=5, mono=True):
    self.sample_rate = sample_rate
    self.duration = duration
    self.mono = mono

  def load(self, file_path):
    signal = librosa.load(file_path, sr=self.sample_rate, duration=self.duration, mono=self.mono)[0]
    return signal


class Padder:
  """
  This class is responsible for padding the signal to a fixed length.
  """
  
  def __init__(self, mode="constant"):
    self.mode = mode

  def left_pad(self, signal, num_missing_items):
    padded_signal = np.pad(signal, (num_missing_items, 0), mode=self.mode)
    return padded_signal

  def right_pad(self, signal, num_missing_items):
    padded_signal = np.pad(signal, (0, num_missing_items), mode=self.mode)
    return padded_signal


class MinMaxNormalizer:
  """
  This class is responsible for normalizing the signal.
  """

  def __init__(self, min_val=-1, max_val=1):
    self.min = min_val
    self.max = max_val

  def normalize(self, signal):
    normalized_signal = (signal - signal.min()) / (signal.max() - signal.min())
    normalized_signal = normalized_signal * (self.max - self.min) + self.min
    return normalized_signal
  
  def denormalize(self, normalized_signal, original_signal_max, original_signal_min):
    denormalized_signal = (normalized_signal - self.min) / (self.max - self.min)
    denormalized_signal = normalized_signal * (original_signal_max - original_signal_min) + original_signal_min
    return denormalized_signal


class LogSpectrogram:
  """
  This class is responsible for converting the signal into a log spectrogram.
  """

  def __init__(self, n_fft=2048, hop_length=512):
    self.n_fft = n_fft
    self.hop_length = hop_length

  def __call__(self, signal):
    stft = librosa.stft(signal, n_fft=self.n_fft, hop_length=self.hop_length)[:-1]
    spectrogram = np.abs(stft)
    log_spectrogram = librosa.amplitude_to_db(spectrogram)
    return log_spectrogram
    

class Saver:
  """
  This class is responsible for saving the features and the min max values.
  """

  def __init__(self, feature_save_dir, min_max_values_save_dir):
    self.feature_save_dir = feature_save_dir
    self.min_max_values_save_dir = min_max_values_save_dir


  def save_feature(self, feature, file_path):
    save_path = self._generate_save_path(file_path)
    np.save(save_path, feature)
    return save_path


  def save_min_max_values(self, min_max_values):
    save_path = os.path.join(self.min_max_values_save_dir, "min_max_values.pkl")
    self._save(min_max_values, save_path)


  @staticmethod
  def _save(data, save_path):
    with open(save_path, "wb") as f:
      pickle.dump(data, f)


  def _generate_save_path(self, file_path):
    file_name = os.path.split(file_path)[1]
    save_path = os.path.join(self.feature_save_dir, file_name + ".npy")
    return save_path


class PreprocesingPipeline:
  """
  PreprocessingPipeline processes audio files in a directory, applying
  the following steps to each file:
    1- load a file
    2- pad the signal (if necessary)
    3- extracting log spectrogram from signal
    4- normalise spectrogram
    5- save the normalised spectrogram

  Storing the min max values for all the log spectrograms.
  """

  def __init__(self):
    self._loader = None
    self.padder = None
    self.extractor = None
    self.normalizer = None
    self.saver = None
    self.min_max_values = {}
    self._expected_sample_length = None


  @property
  def loader(self):
    return self._loader
  

  @loader.setter
  def loader(self, loader):
    self._loader = loader
    self._expected_sample_length = int(loader.duration * loader.sample_rate)


  def process(self, path):
    for root, _, files in os.walk(path):
      for file in files:
        file_path = os.path.join(root, file)
        self.process_file(file_path)
        print(f"Processed {file_path}")
    self.saver.save_min_max_values(self.min_max_values)


  def process_file(self, file_path):
    signal = self.loader.load(file_path)
    self._do_padding(signal)
    feature = self.extractor.extract(signal)
    normalized_feature = self.normalizer.normalize(feature)
    save_path = self.saver.save_feature(normalized_feature, file_path)
    self._store_min_max_value(save_path, feature.min(), feature.max())
  

  def _do_padding(self, signal):
    if len(signal) < self.expected_sample_length:
      num_missing_items = self.expected_sample_length - len(signal)
      signal = self.padder.right_pad(signal, num_missing_items)
    return signal
  

  def _store_min_max_value(self, path, min_val, max_val):
    self.min_max_values[path] = {
      "min": min_val,
      "max": max_val
    }


if __name__ == "__main__":
  FRAME_SIZE = 512
  HOP_LENGTH = 256
  DURATION = 0.74  # in seconds
  SAMPLE_RATE = 22050
  MONO = True

  SPECTROGRAMS_SAVE_DIR = "./Autoencoder/Test_data/Spectrograms"
  MIN_MAX_VALUES_SAVE_DIR = "./Autoencoder/Test_data/MinMaxValues"
  FILES_DIR = "./Autoencoder/Test_data"

  # instantiate all objects
  loader = Loader(SAMPLE_RATE, DURATION, MONO)
  padder = Padder()
  log_spectrogram_extractor = LogSpectrogram(FRAME_SIZE, HOP_LENGTH)
  min_max_normaliser = MinMaxNormalizer(0, 1)
  saver = Saver(SPECTROGRAMS_SAVE_DIR, MIN_MAX_VALUES_SAVE_DIR)

  preprocessing_pipeline = PreprocesingPipeline()
  preprocessing_pipeline.loader = loader
  preprocessing_pipeline.padder = padder
  preprocessing_pipeline.extractor = log_spectrogram_extractor
  preprocessing_pipeline.normaliser = min_max_normaliser
  preprocessing_pipeline.saver = saver

  preprocessing_pipeline.process(FILES_DIR)