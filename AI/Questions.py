import inquirer
import os

class questions:
  def __init__(self, processed_data_file_path, processed_label_file_path, model_path):
    self.load_saved_model = False
    self.should_train = True
    self.learning_rate = 0
    self.batch_size = 0
    self.epochs = 0
    self.load_saved_training_data = False

    self.processed_data_file_path = processed_data_file_path
    self.processed_label_file_path = processed_label_file_path

    self.model_path = model_path


  def ask(self):
    
    if os.path.exists(self.model_path[0]) and os.path.exists(self.model_path[1]) and os.path.exists(self.model_path[2]) and os.path.exists(self.model_path[3]):
      self.load_saved_model = self._load_saved_model()

    if self.load_saved_model:
      self.should_train = self._should_train()

    if self.should_train:
      # self.learning_rate = self._learning_rate()
      # self.batch_size = self._batch_size()
      self.epochs = self._epochs()

      if os.path.exists(self.processed_data_file_path) and os.path.exists(self.processed_label_file_path):
        self.load_saved_training_data = self._load_saved_training_data()

    self.should_log = self._should_log()

    return self.load_saved_model, self.should_train, self.epochs, self.load_saved_training_data, self.should_log
  
  
  def _learning_rate(self):
    learning_rate_questions = [
      inquirer.List(
        "learning rate",
        message="Learning rate? (Every step is about x3)",
        choices=['Big steps', 'Medium steps', 'Standard steps', 'Small steps', 'Tiny steps'],
      ),
    ]

    def switch(x):
      return {
          'Big steps': 0.0005,
          'Medium steps': 0.00015,
          'Standard steps': 0.00005,
          'Small steps': 0.000015,
          'Tiny steps': 0.000005,
      }[x]
    answer = inquirer.prompt(learning_rate_questions)
    answer = switch(answer['learning rate'])
    return answer
  

  def _batch_size(self):
    batch_size_questions = [
      inquirer.List(
        "batch size",
        message="Batch size?",
        choices=[64, 32, 16, 8, 4, 2, 1],
      ),
    ]

    answer = inquirer.prompt(batch_size_questions)
    return answer['batch size']
  

  def _epochs(self):
    epochs_questions = [
      inquirer.List(
        "epochs",
        message="Epochs?",
        choices=[200, 150, 100, 50, 25, 10, 5, 1],
      ),
    ]

    answer = inquirer.prompt(epochs_questions)
    return answer['epochs']
  
  def _should_log(self):
    should_log_questions = [
      inquirer.List(
        "should_log",
        message="Should log results and inbetween steps?",
        choices=['Yes', 'No'],
      ),
    ]

    def switch(x):
      return {
          'Yes': True,
          'No': False,
      }[x]
    answer = inquirer.prompt(should_log_questions)
    answer = switch(answer['should_log'])
    return answer


  def _should_train(self):
    should_train_questions = [
      inquirer.List(
        "should_train",
        message="Should train?",
        choices=['Yes', 'No'],
      ),
    ]

    def switch(x):
      return {
          'Yes': True,
          'No': False,
      }[x]
    answer = inquirer.prompt(should_train_questions)
    answer = switch(answer['should_train'])
    return answer


  def _load_saved_training_data(self):
    load_saved_training_data_questions = [
      inquirer.List(
        "load_saved_training_data",
        message="Load saved training data?",
        choices=['Yes', 'No'],
      ),
    ]

    def switch(x):
      return {
          'Yes': True,
          'No': False,
      }[x]
    answer = inquirer.prompt(load_saved_training_data_questions)
    answer = switch(answer['load_saved_training_data'])
    return answer


  def _load_saved_model(self):
    load_saved_model_questions = [
      inquirer.List(
        "load_saved_model",
        message="Load saved model?",
        choices=['Yes', 'No'],
      ),
    ]

    def switch(x):
      return {
          'Yes': True,
          'No': False,
      }[x]
    answer = inquirer.prompt(load_saved_model_questions)
    answer = switch(answer['load_saved_model'])
    return answer

