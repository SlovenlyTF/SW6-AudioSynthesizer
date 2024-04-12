from AudioProcessor import AudioProcessor
from Autoencoder import VAE
from Train import TrainModel
from Questions import questions
import os
import numpy as np
import tensorflow as tf


physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
  tf.config.experimental.set_memory_growth(physical_devices[0], True)


data_files_path = "./data/data"
label_files_path = "./data/label"

processed_data_file_path = "./data/processed_data.npy"
processed_label_file_path = "./data/processed_label.npy"

model_weights_path = "./model/weights.h5"
model_params_path = "./model/parameters.pkl"


# Load the model
autoencoder = VAE(
  spectrogram_dim=(1024, 128, 1),
  conv_filters=(512, 256, 128, 64, 32),
  conv_kernels=(3, 3, 3, 3, 3),
  conv_strides=(2, 2, 2, 2, (2, 1)),
  latent_space_dim=256
)


processor = AudioProcessor(model=autoencoder)
train_model = TrainModel()
questions = questions(processed_data_file_path, processed_label_file_path, model_weights_path, model_params_path)


autoencoder.summary()

# Ask the user some questions
load_saved_model, should_train, learning_rate, batch_size, epochs, load_saved_training_data = questions.ask()

print(f"model dir path: {os.path.dirname(model_weights_path)}")


if load_saved_model:
  autoencoder = autoencoder.load(os.path.dirname(model_weights_path))

autoencoder.compile(learning_rate=learning_rate)


# Load the data
if load_saved_training_data:
  print("Loading processed data")
  data = np.load(processed_data_file_path)
  labels = np.load(processed_label_file_path)
else:
  data, labels = train_model.load_data(data_files_path, label_files_path)
  data, labels = train_model.reshape_data(data, labels)
  np.save(processed_data_file_path, data)
  np.save(processed_label_file_path, labels)

x_train, y_train = data, labels



if should_train:
  autoencoder = train_model.train(x_train, y_train, autoencoder, batch_size=batch_size, epochs=epochs)
  autoencoder.save("./model")
else:
  autoencoder = autoencoder.load("./model")


# predict_data = data[0][np.newaxis, ...]
predict_data = data[0:8]

# Predict the model
predictions, laten_space = processor.generate(predict_data)

# scale the predictions up
predictions = predictions * 4
print(f"min: {np.min(predictions)}, max: {np.max(predictions)}")

processor.save_audio(predictions, "./")

