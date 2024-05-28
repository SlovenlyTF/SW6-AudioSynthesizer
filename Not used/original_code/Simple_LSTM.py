# Importing libraries
import tensorflow as tf
import wav_to_timeseperated_arrays as wtta
from scipy.io.wavfile import write
import numpy as np

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
Input = wtta.audio_to_arrays("./Data/Jingle Bells 1 Mads Synced.wav", timestep=0.5)
Input_Append = (wtta.audio_to_arrays("./Data/Jingle Bells 1 Toby Synced.wav", timestep=0.5))
for i in range(len(Input_Append)):
	Input.append(Input_Append[i])


# Data
result = wtta.audio_to_arrays("./Data/Jingle Bells 1 Synced.wav", timestep=0.5)
for i in range(len(result)):
	result.append(result[i])


# Builds the LSTM model
def build_LSTM(Data, Labels, Epoch, BatchSize):

	model = tf.keras.Sequential([
		tf.keras.layers.Reshape((11025, 1), input_shape=(11025,)),
		tf.keras.layers.LSTM(units=256, return_sequences=True),
		tf.keras.layers.LSTM(units=256, return_sequences=True),
		tf.keras.layers.LSTM(units=256, return_sequences=True),
		tf.keras.layers.LSTM(units=512, return_sequences=False),
		tf.keras.layers.Dense(11025)
	])

	early_stopper = EarlyStopping( monitor = 'accuracy' , min_delta = 0.05, patience = 3 )

	reduce_lr = ReduceLROnPlateau( monitor = 'loss' , patience = 2 , cooldown = 0)

	callbacks = [reduce_lr, early_stopper]

	# Compile the model
	model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', F1Score()])

	# Convert list of arrays to numpy arrays
	Data = np.array(Data)
	Labels = np.array(Labels)

	model.fit(Data, Labels, epochs=Epoch, batch_size=BatchSize, callbacks=callbacks)

	# Return the model
	return model

model = build_LSTM(Input, result, 10, 64)

Test = wtta.audio_to_arrays("./Data/TobyHum.wav", timestep=0.5)

Test_Result = []

for i in range(len(Test)):
	Test_Result.append(model.predict(Test[i]))


# Save the result
wav_object = './Data/TobyHumToPiano.wav'
write(wav_object, 11025, Test_Result)