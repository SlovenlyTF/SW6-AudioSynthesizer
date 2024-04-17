from AudioProcessor import AudioProcessor
from Cyclegan import train
from DataProcessor import DataProcessor
from Questions import questions
import os
import numpy as np
import tensorflow as tf
from Cyclegan import predict
import torch
import datetime
from torchvision.utils import save_image

def AI_convert(signal, sr):
  physical_devices = tf.config.experimental.list_physical_devices('GPU')
  if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


  model_path = ["./model/genh.pth.tar", "./model/genz.pth.tar", "./model/critich.pth.tar", "./model/criticz.pth.tar"]


  processor = AudioProcessor()
  data_processor = DataProcessor()
  log = True

  if log is True:
    log_path = f"./predict/output_model_log/{datetime.datetime.now()}"
    log_path = log_path.replace(" ", "_").replace(":", "-")
    os.makedirs(log_path)
    log_file = open(f"{log_path}/Log.txt", "a")
    log = [log_path, log_file]
  else:
    log = None

  # Train the model
  print("Load the model")
  trainer = train.trainer()
  gen_1, gen_2 = trainer.run(load_saved_model, False, epochs)
  print("Loading done")

  predict_data, _ = data_processor.load_data_from_signal(signal = signal, sr = sr, log=log)

  predictions = predict.predictionClass(gen_1, predict_data).predict()
  
  # Save the predictions in grayscale
  if log is not None:
    for i in range(predictions.shape[0]):
      np_arr = predictions[i].reshape(1024, 128)
      tensor = torch.from_numpy(np_arr)
      if tensor.dtype == torch.int:
        tensor = tensor.float()  # Convert integers to float if necessary
      save_image(tensor + 0.5, f"{log[0]}/prediction_grayscale_segment_{i+1}.png")

  prediction_signal = processor.convert_spectrogram_to_signal(predictions, log=log)

  if log is not None:
    processor.save_audio(prediction_signal, log_path)
    log_file.close()

  return prediction_signal, 22050
