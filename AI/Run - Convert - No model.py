from AudioProcessor import AudioProcessor
from Cyclegan import train
from DataProcessor import DataProcessor
import os
import numpy as np
import datetime

def main():

  processor = AudioProcessor()
  data_processor = DataProcessor()

  log_path = f"./predict/output_model/{datetime.datetime.now()}"
  log_path = log_path.replace(" ", "_").replace(":", "-")
  os.makedirs(log_path)
  log_file = open(f"{log_path}/Log.txt", "a")
  log = [log_path, log_file]


  # Load the data
  x_train = [0]
  y_train = [0]


  predict_files_path = "./predict/input"
  predict_data, _ = data_processor.load_data(data_file_path=predict_files_path, log=log)

  predictions = processor.convert_spectrogram_to_signal(predict_data, log=log)

  predictions = predictions * 4

  # scale the predictions up
  print(f"min: {np.min(predictions)}, max: {np.max(predictions)}")

  processor.save_audio(predictions, log_path)

  log_file.close()

if __name__ == "__main__":
  main()
