from Autoencoder import VAE
import numpy as np
from AudioProcessor import AudioProcessor

class TrainModel:
  def __init__(self):
    self.processor = AudioProcessor()

  def load_data(self, data_file_path, label_file_path):
    print()
    print("---Loading train data---")
    data = self.processor.create_spectrogram_from_dir(data_file_path)
    data = np.array(data)
    print()
    print("---Loading test labels---")
    labels = self.processor.create_spectrogram_from_dir(label_file_path)
    labels = np.array(labels)
    return data, labels


  def reshape_data(self, data_1, labels_1):
    data = []
    for i in range(len(data_1)):
      for j in range(len(data_1[i])):
        data.append(data_1[i][j])
    data = np.array(data)
    data = data[..., np.newaxis]

    labels = []
    for i in range(len(labels_1)):
      for j in range(len(labels_1[i])):
        labels.append(labels_1[i][j])
    labels = np.array(labels)
    labels = labels[..., np.newaxis]

    print(f"Data shape: {data.shape}, Labels shape: {labels.shape}")
    return data, labels


  def split_data(data, labels):
    num_samples = len(data)
    num_train_samples = int(num_samples * 0.8)
    data_train = data[:num_train_samples]
    labels_train = labels[:num_train_samples]
    data_test = data[num_train_samples:]
    labels_test = labels[num_train_samples:]
    return data_train, labels_train, data_test, labels_test


  def train(self, data, label, autoencoder = None, batch_size=8, epochs=10):
    autoencoder.train(data, label, batch_size, epochs)
    print("Training complete")
    
    return autoencoder
  
  def test(self, data, label, autoencoder):
    autoencoder.test(data, label)
    print("Testing complete")