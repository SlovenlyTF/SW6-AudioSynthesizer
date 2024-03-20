from Autoencoder import VAE
import numpy as np
from AudioProcessor import AudioProcessor

class TrainModel:
  def __init__(self):
    self.processor = AudioProcessor()

  def load_data(self, data_file_path, label_file_path):
    data = self.processor.create_spectrogram_from_dir(data_file_path)
    data = np.array(data)
    labels = self.processor.create_spectrogram_from_dir(label_file_path)
    labels = np.array(labels)
    return data, labels


  def reshape_data(self, data, labels):
    data = data.reshape((-1, data.shape[2], data.shape[3]))
    data = data[..., np.newaxis]

    labels = labels.reshape((-1, labels.shape[2], labels.shape[3]))
    labels = labels[..., np.newaxis]
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