from AudioProcessor import AudioProcessor
from Autoencoder import VAE
from Train import TrainModel
import librosa
import numpy as np



# Load the model
autoencoder = VAE(
  spectrogram_dim=(1024, 128, 1),
  conv_filters=(512, 256, 128, 64, 32),
  conv_kernels=(3, 3, 3, 3, 3),
  conv_strides=(2, 2, 2, 2, (2, 1)),
  latent_space_dim=128
)

autoencoder.summary()
autoencoder.compile(learning_rate=0.0005)

processor = AudioProcessor(VAE=autoencoder)
train_model = TrainModel()


train_file_path = "./data/train"
test_file_path = "./data/test"

data, labels = train_model.load_data(train_file_path, test_file_path)
data, labels = train_model.reshape_data(data, labels)

x_train, y_train = data, labels


should_train = True

if should_train:
  autoencoder = train_model.train(x_train, y_train, autoencoder, batch_size=8, epochs=2)
  autoencoder.save("./model")
else:
  autoencoder = autoencoder.load("./model")


# predict_data = data[0][np.newaxis, ...]
predict_data = data[0:8]

# Predict the model
predictions, laten_space = processor.generate(predict_data)

# scale the predictions up
predictions = predictions * 100
print(f"min: {np.min(predictions)}, max: {np.max(predictions)}")

processor.save_audio(predictions, "./")

