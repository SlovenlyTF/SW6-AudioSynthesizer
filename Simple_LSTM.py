# Importing libraries
import tensorflow as tf
import numpy as np
import pickle
import json
import librosa
import librosa.display
import math
import wav_to_timeseperated_arrays as wtta
from scipy.io.wavfile import write

from keras.metrics import Accuracy, Precision, Recall, F1Score
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
from os.path import exists
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

# Plotting
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd


# Loading the data
Input = wtta.audio_to_arrays("./Data/Jingle Bells 1 Mads Synced.wav", timestep=0.5)

print('Input1', len(Input))
Input_Append = (wtta.audio_to_arrays("./Data/Jingle Bells 1 Toby Synced.wav", timestep=0.5))

for i in range(len(Input_Append)):
	Input.append(Input_Append[i])

print('Input2:', len(Input))


# Data
result = wtta.audio_to_arrays("./Data/Jingle Bells 1 Synced.wav", timestep=0.5)

print('Result1:', len(result))
for i in range(len(result)):
	result.append(result[i])

print('Result2:', len(result))



# Builds the LSTM model
def build_LSTM(Data, Labels, Epoch, BatchSize):
  
	# model = tf.keras.Sequential()
	# model.add(tf.keras.layers.LSTM(64, input_shape=(11025, 1)))
	# model.add(tf.keras.layers.LSTM(128, return_sequences=True, return_state=True))
	# model.add(tf.keras.layers.Dense(11025))

	input = np.reshape(Input, (Data[0].shape, Data[1].shape, 1))

	model = tf.keras.Sequential([
		tf.keras.layers.Embedding(input_dim=128, output_dim=64, input_shape=(11025, 1)),
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

	model.fit(input, Labels, epochs=Epoch, batchsize=BatchSize, callbacks=callbacks)

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