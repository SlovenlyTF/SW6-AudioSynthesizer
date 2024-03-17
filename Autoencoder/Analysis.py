from Audio_to_spectrogram import AudioProcessor
from Autoencoder import VAE
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

processor = AudioProcessor()

# Load the data
train_file_path = "./data/train"
test_file_path = "./data/test"
train_data = processor.create_spectrogram_from_dir(train_file_path)
train_data = np.array(train_data)
test_data = processor.create_spectrogram_from_dir(test_file_path)
test_data.append(test_data[0])
test_data = np.array(test_data)

# reshape the data
train_data = train_data.reshape((-1, train_data.shape[2], train_data.shape[3]))
train_data = train_data[..., np.newaxis]

test_data = test_data.reshape((-1, test_data.shape[2], test_data.shape[3]))
test_data = test_data[..., np.newaxis]


print(f"Train Data shape: {train_data.shape}")
print(f"Test Data shape: {test_data.shape}")



# Train the model
autoencoder.train(train_data, train_data, num_epochs=10, batch_size=2)


# Predict the model
predictions = autoencoder.predict(train_data[0])


# Denormalize the data
denormalized_predictions = processor.denormalize(predictions)
denormalized_test_data = processor.denormalize(train_data[0])


# Spectrogram of predicted data and original data
librosa.display.specshow(denormalized_predictions, sr=22050, x_axis='time', y_axis='log')
librosa.display.specshow(denormalized_test_data, sr=22050, x_axis='time', y_axis='log')



