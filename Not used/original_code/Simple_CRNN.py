TimeStep = 2

# Importing libraries
import tensorflow as tf
import audio_to_spectrogram as ats
from scipy.io.wavfile import write
import numpy as np
import librosa
import librosa.display

from keras.metrics import F1Score
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from os.path import exists
from keras.callbacks import ReduceLROnPlateau, EarlyStopping


# Explicitly specify GPU device
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Index of the GPU to use

# Limit GPU memory usage
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
	try:
		tf.config.experimental.set_memory_growth(gpus[0], True)
	except RuntimeError as e:
		print(e)


# Loading the data
Input = ats.audio_to_spectrograms("./Data/Jingle Bells 1 Mads Synced.wav", timestep=TimeStep)
Input_Append = ats.audio_to_spectrograms("./Data/Jingle Bells 1 Toby Synced.wav", timestep=TimeStep)
for i in range(len(Input_Append)):
	Input.append(Input_Append[i])

# Data
result = ats.audio_to_spectrograms("./Data/Jingle Bells 1 Synced.wav", timestep=TimeStep)
for i in range(len(result)):
	result.append(result[i])


# Build the CRNN model
def build_crnn(data, labels, epoch, batchsize):

	data = np.expand_dims(data, axis=0)
	labels = np.expand_dims(labels, axis=0)

	model = models.Sequential()
	model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(400, 200, 3)))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.Flatten())
	model.add(layers.Dense(64, activation='relu'))
	model.add(layers.Dense(10))

	model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', F1Score()])

	early_stopper = EarlyStopping( monitor = 'accuracy' , min_delta = 0.05, patience = 3 )

	reduce_lr = ReduceLROnPlateau( monitor = 'loss' , patience = 2 , cooldown = 0)

	callbacks = [reduce_lr, early_stopper]

	model.fit(data, labels, epochs=epoch, batch_size=batchsize, callbacks=callbacks)

	return model
	


model = build_crnn(Input, result, 10, 64)

Test = ats.audio_to_spectrograms("./Data/TobyHum.wav", timestep=TimeStep)

Test_Result = []

for i in range(len(Test)):
	Test_Result.append(model.predict(Test[i]))
	librosa.display.specshow(Test_Result[i], sr=22050, x_axis='time', y_axis='log')