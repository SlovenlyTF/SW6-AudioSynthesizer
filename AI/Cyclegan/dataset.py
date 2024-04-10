from PIL import Image
import os
from torch.utils.data import Dataset
import numpy as np

class HumMusicDataset(Dataset):
    def __init__(self, music_numpy_array, hum_numpy_array, transform=None):
        self.music_numpy_array = music_numpy_array
        self.hum_numpy_array = hum_numpy_array
        self.transform = transform

        self.length_dataset = max(len(self.music_numpy_array), len(self.hum_numpy_array)) # 1000, 1500
        self.music_len = len(self.music_numpy_array)
        self.hum_len = len(self.hum_numpy_array)

    def __len__(self):
        return self.length_dataset

    def __getitem__(self, index):
        music_img = self.music_numpy_array[index % self.music_len]
        hum_img = self.hum_numpy_array[index % self.hum_len]

        print(f"music_img.shape: {music_img.shape}, hum_img.shape: {hum_img.shape}")

        if self.transform:
            augmentations = self.transform(image=music_img, image0=hum_img)
            music_img = augmentations["image"]
            hum_img = augmentations["image0"]

        return music_img, hum_img