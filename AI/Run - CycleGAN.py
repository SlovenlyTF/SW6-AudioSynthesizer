from AudioProcessor import AudioProcessor
from Cyclegan import train
from DataProcessor import DataProcessor
from Questions import questions
import os
import numpy as np
import tensorflow as tf

def main():
  physical_devices = tf.config.experimental.list_physical_devices('GPU')
  if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


  data_files_path = "./data/train/hum"
  label_files_path = "./data/train/music"

  processed_data_file_path = "./data/processed_data.npy"
  processed_label_file_path = "./data/processed_label.npy"

  model_weights_path = "./model/weights.h5"
  model_params_path = "./model/parameters.pkl"


  processor = AudioProcessor()
  DataProcessor = DataProcessor()
  # questions = questions(processed_data_file_path, processed_label_file_path, model_weights_path, model_params_path)


  # Ask the user some questions
  # load_saved_model, should_train, learning_rate, batch_size, epochs, load_saved_training_data = questions.ask()


  # Load the data
  # if load_saved_training_data:
  #   print("Loading processed data")
  #   data = np.load(processed_data_file_path)
  #   labels = np.load(processed_label_file_path)
  # else:
  data, labels = DataProcessor.load_data(data_files_path, label_files_path)
  np.save(processed_data_file_path, data)
  np.save(processed_label_file_path, labels)

  x_train, y_train = data, labels



  # Train the model
  print("Training the model")
  trainer = train.trainer(x_train, y_train, x_train, y_train)
  trainer.run()
  print("Training done")


  # # predict_data = data[0][np.newaxis, ...]
  # predict_data = data[0:8]

  # # Predict the model
  # predictions, laten_space = processor.generate(predict_data)

  # # scale the predictions up
  # predictions = predictions * 4
  # print(f"min: {np.min(predictions)}, max: {np.max(predictions)}")

  # processor.save_audio(predictions, "./")

if __name__ == "__main__":
  main()
