from AudioProcessor import AudioProcessor
from Cyclegan import train
from DataProcessor import DataProcessor
import os
import numpy as np
import datetime

def main():

  processor = AudioProcessor()
  data_processor = DataProcessor()
  log = True

  if log is True:
    # Comment out the following lines to remove logging of data
    log_path = f"./predict/output_no_model_log/{datetime.datetime.now()}"
    log_path = log_path.replace(" ", "_").replace(":", "-")
    os.makedirs(log_path)
    log_file = open(f"{log_path}/Log.txt", "a")
    log = [log_path, log_file]
  else:
    log = None


  predict_files_path = "./predict/input"
  predict_data, _ = data_processor.load_data(data_file_path=predict_files_path, log=log)

  prediction_signal = processor.convert_spectrogram_to_signal(predict_data, log=log)

  # prediction_signal = prediction_signal * 4
  print(f"min: {np.min(prediction_signal)}, max: {np.max(prediction_signal)}")

  processor.save_audio(prediction_signal, log[0])

  log[1].close()

if __name__ == "__main__":
  main()
