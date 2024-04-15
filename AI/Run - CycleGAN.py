from AudioProcessor import AudioProcessor
from Cyclegan import train
from DataProcessor import DataProcessor
from Questions import questions
import os
import numpy as np
import tensorflow as tf
from Cyclegan import predict

def main():
  physical_devices = tf.config.experimental.list_physical_devices('GPU')
  if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


  data_files_path = "./data/train/hum"
  label_files_path = "./data/train/music"

  processed_data_file_path = "./data/processed_data.npy"
  processed_label_file_path = "./data/processed_label.npy"

  model_path = ["./model/genh.pth.tar", "./model/genz.pth.tar", "./model/critich.pth.tar", "./model/criticz.pth.tar"]


  log_path = f"./predict/output_model/{datetime.datetime.now()}"
  log_path = log_path.replace(" ", "_").replace(":", "-")
  os.makedirs(log_path)
  log_file = open(f"{log_path}/Log.txt", "a")
  log = [log_path, log_file]


  processor = AudioProcessor()
  data_processor = DataProcessor()
  questions_class = questions(processed_data_file_path, processed_label_file_path, model_path)


  # Ask the user some questions
  load_saved_model, should_train, epochs, load_saved_training_data = questions_class.ask()


  # Load the data
  x_train = [0]
  y_train = [0]

  if should_train:
    if not load_saved_training_data:
      print("Processing data")
      data, labels = data_processor.load_data(data_files_path, label_files_path)
      print("Saving processed data")
      np.save(processed_data_file_path, data)
      np.save(processed_label_file_path, labels)
    else:
      print("Loading processed data")
      data = np.load(processed_data_file_path)
      labels = np.load(processed_label_file_path)

    x_train, y_train = data, labels



  # Train the model
  print("Training the model")
  trainer = train.trainer(x_train, y_train, x_train[0:1], y_train[0:1])
  gen_1, gen_2 = trainer.run(load_saved_model, should_train, epochs)
  print("Training done")

  predict_files_path = "./predict/input"
  predict_data, _ = data_processor.load_data(data_file_path=predict_files_path, log=log)



  predictions = predict.predictionClass(gen_1, predict_data).predict()

  predictions = processor.convert_spectrogram_to_signal(predictions, log=log)

  # scale the predictions up
  print(f"min: {np.min(predictions)}, max: {np.max(predictions)}")

  processor.save_audio(predictions, "log_path")

  log_file.close()

if __name__ == "__main__":
  main()
