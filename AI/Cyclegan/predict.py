import torch
from Cyclegan import dataset
from torch.utils.data import DataLoader
from Cyclegan import config
from tqdm import tqdm
import numpy as np


class predictionClass:
  def __init__(self, model, data):
    self.model = model
    self.data = np.array(data)
    self.label = np.array(data)

  def predict(
    self,
  ):
    data_dataset = dataset.HumMusicDataset(
      hum_numpy_array=self.data,
      music_numpy_array=self.label,
      transform=config.transforms,
    )
    loader = DataLoader(
      data_dataset,
      batch_size=1,
      shuffle=False,
      num_workers=config.NUM_WORKERS,
      pin_memory=True,
    )

    loop = tqdm(loader, leave=True)

    predictions = []

    for idx, (music, hum) in enumerate(loop):
      music = music.to(config.DEVICE)

      # Train Discriminators H and Z
      with torch.cuda.amp.autocast():
        fake_hum = self.model(music)
        fake_hum = fake_hum.squeeze(0).detach().cpu().numpy()
        predictions.append(fake_hum)

    # Reshape the predictions
    predictions = np.array(predictions)
    predictions = np.concatenate(predictions, axis=0)
    predictions = predictions[..., np.newaxis]

    return predictions