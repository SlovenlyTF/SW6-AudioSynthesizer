import numpy as np
from AudioProcessor import AudioProcessor
import math

class DataProcessor:
  def __init__(self):
    self.processor = AudioProcessor()

  def load_data_from_signal(self, signal, sr, log = None):
    data = None
    labels = None

    data = self.processor.file_processor(signal, sr, log=log)

    data, _ = self.reshape_data(data, labels, log=log)

    data = np.array(data)
    return data

  def load_data(self, data_file_path = None, label_file_path = None, log = None):
    data = None
    labels = None

    if data_file_path is not None:
      print()
      print("---Loading data---")
      data = self.processor.create_spectrogram_from_dir(data_file_path, log=log)
    if label_file_path is not None:
      print()
      print("---Loading labels---")
      labels = self.processor.create_spectrogram_from_dir(label_file_path, log=log)

    data, labels = self.reshape_data(data, labels, log=log)

    labels = np.array(labels)
    data = np.array(data)

    return data, labels


  def reshape_data(self, data_1, labels_1, log):
    data = []
    if data_1 is not None:
      print("Reshaping data")
      for i in range(len(data_1)):
        for j in range(len(data_1[i])):
          data.append(data_1[i][j])
    data = np.array(data)
    data = data[..., np.newaxis]

    labels = []
    if labels_1 is not None:
      print("Reshaping labels")
      for i in range(len(labels_1)):
        for j in range(len(labels_1[i])):
          labels.append(labels_1[i][j])
    labels = np.array(labels)
    labels = labels[..., np.newaxis]

    print(f"Data shape: {data.shape}, Labels shape: {labels.shape}")

    if log is not None:
      log[1].write("reshaping the data\n")
      log[1].write(f"Data shape: {data.shape}, Labels shape: {labels.shape}\n")

      if data_1 is not None:
        log[1].write(f"Data min: {np.min(data)}, Data max: {np.max(data)}\n")
      if labels_1 is not None:
        log[1].write(f"Labels min: {np.min(labels)}, Labels max: {np.max(labels)}\n")
      log[1].write("\n\n")

    return data, labels


  def split_data(data, labels):
    num_samples = len(data)
    num_train_samples = int(num_samples * 0.8)
    data_train = data[:num_train_samples]
    labels_train = labels[:num_train_samples]
    data_test = data[num_train_samples:]
    labels_test = labels[num_train_samples:]
    return data_train, labels_train, data_test, labels_test

  def save_data_in_chunks(self, data_file_path, label_file_path, data, labels, chunk_size = 1000):
    for i in range(math.ceil(len(data) / chunk_size)):
      np.save(data_file_path + i + ".npy", data[i*chunk_size:(i+1)*chunk_size])
      np.save(label_file_path + i + ".npy", labels[i*chunk_size:(i+1)*chunk_size])
    print("Data saved")

  def load_data_chuck(self, data_file_path, chunk = 1):
    data = np.load(data_file_path + chunk + ".npy")
    return data

  def load_label_chunk(self, label_file_path, chunk = 1):
    labels = np.load(label_file_path + chunk + ".npy")
    return labels