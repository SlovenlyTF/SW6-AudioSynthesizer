TimeStep = 2.97

# Importing libraries
import tensorflow as tf
from scipy.io.wavfile import write
import numpy as np
import librosa
import librosa.display

from keras.metrics import F1Score
from tensorflow.keras import models, layers, metrics
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from os.path import exists
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

import math
import matplotlib.pyplot as plt

def audio_to_spectrograms(audio_file, timestep):

    # Load audio file
    y, sr = librosa.load(audio_file)

    # Extract frequencies
    audio_duration = len(y) / sr  # Assuming y and sr are already defined
    samples = []

    for i in range(math.ceil(audio_duration / timestep)):
        if i == math.ceil(audio_duration / timestep) - 1:
            samples.append(y[int(i * (sr * timestep)):])
            for j in range(int((i + 1) * (sr * timestep)) - len(y)):
                samples[i] = np.append(samples[i], 0)
        else:
            samples.append(y[int(i * (sr * timestep)):int((i + 1) * (sr * timestep))])

    # Compute spectrogram
    spect = []
    for i in range(len(samples)):
        spect.append(librosa.feature.melspectrogram(y=samples[i], sr=sr))
        # stft = librosa.stft(samples[i])
        # spect.append(librosa.amplitude_to_db(abs(stft), ref=np.max))
        print(spect[i].shape, end=' | ')

    spect = np.array(spect)

    return spect

# Loading the data
# Loading the data
Input = audio_to_spectrograms("./Data/Jingle Bells 1 Mads Synced.wav", timestep=TimeStep)
Input_Append = audio_to_spectrograms("./Data/Jingle Bells 1 Toby Synced.wav", timestep=TimeStep)

# Data
Result = audio_to_spectrograms("./Data/Jingle Bells 1 Synced.wav", timestep=TimeStep)

# Concatenate the data
Input = np.concatenate((Input, Input_Append), axis=0)
Input = np.array([x.reshape((128, 128, 1)) for x in Input])

Result = np.concatenate((Result, Result), axis=0)

     
def build_crnn(data, labels, epoch, batchsize):
    # Reshape data and labels

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1), padding='same'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))

    # Up-sampling layers
    model.add(layers.Conv2DTranspose(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.UpSampling2D((2, 2)))
    model.add(layers.Conv2DTranspose(32, (3, 3), activation='relu', padding='same'))
    model.add(layers.UpSampling2D((2, 2)))

    # Output layer with sigmoid activation since you're dealing with binary classification
    model.add(layers.Conv2DTranspose(1, (3, 3), activation='sigmoid', padding='same'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics='accuracy')

    early_stopper = EarlyStopping(monitor='accuracy', min_delta=0.05, patience=3)
    reduce_lr = ReduceLROnPlateau(monitor='loss', patience=2, cooldown=0)

    callbacks = [reduce_lr, early_stopper]

    model.fit(data, labels, epochs=epoch, batch_size=batchsize, callbacks=callbacks)

    return model


model = build_crnn(Input, Result, 10, 64)

Test = audio_to_spectrograms("./Data/TobyHumNote.wav", timestep=TimeStep)
Input = np.array([x.reshape((128, 128, 1)) for x in Test])

Test_Result = []

for i in range(len(Test)):
	Test_Result.append(model.predict(Test[i]))
	librosa.display.specshow(Test_Result[i], sr=22050, x_axis='time', y_axis='log')