from AudioProcessor import AudioProcessor
from Autoencoder import VAE
from Train import TrainModel
from Questions import questions
import os
import numpy as np
import tensorflow as tf
import soundfile as sf
import librosa


physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
  tf.config.experimental.set_memory_growth(physical_devices[0], True)


data_files_path = "./test/data"
label_files_path = "./test/label"


processor = AudioProcessor()
train_model = TrainModel()

data, labels = train_model.load_data(data_files_path, label_files_path)
data, labels = train_model.reshape_data(data, labels)

audio = processor.convert_spectrogram_to_signal(labels)
audio = audio * 4
processor.save_audio(audio, "./test")

