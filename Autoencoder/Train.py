from Autoencoder import VAE
import numpy as np

LEARNING_RATE = 0.0005
BATCH_SIZE = 32
EPOCHS = 10


def load_data():
  x = np.load('x.npy')
  y = np.load('y.npy')
  return x, y


def split_data(x, y):
  num_samples = len(x)
  num_train_samples = int(num_samples * 0.8)
  x_train = x[:num_train_samples]
  y_train = y[:num_train_samples]
  x_test = x[num_train_samples:]
  y_test = y[num_train_samples:]
  return x_train, y_train, x_test, y_test


def load_model(autoencoder = None):
  autoencoder = VAE(
      spectrogram_dim=(128, 128, 1),
      conv_filters=(32, 64, 64, 64),
      conv_kernels=(3, 3, 3, 3),
      conv_strides=(1, 2, 2, 1),
      latent_space_dim=128
  )
  autoencoder.summary()
  autoencoder.compile(LEARNING_RATE)
  return autoencoder


def train(x_train, y_train, autoencoder = None):
  autoencoder.train(x_train, y_train, BATCH_SIZE, EPOCHS)
  print("Training complete")
  return autoencoder


def test(x_test, y_test, autoencoder = None):
  if autoencoder is not None:
    autoencoder.test(x_test, y_test)
    print("Testing complete")
  else:
    print("No model to test")


if __name__ == "__main__":
  autoencoder = None
  x_train, y_train, x_test, y_test = split_data(*load_data())
  autoencoder = load_model(autoencoder)
  autoencoder = train(x_train, y_train, autoencoder)
  test(x_test, y_test, autoencoder)
  