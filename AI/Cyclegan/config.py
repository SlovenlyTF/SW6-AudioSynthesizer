import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from AudioProcessor import AudioProcessor

AudioProcessor = AudioProcessor()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TRAIN_DIR = "../data/train"
VAL_DIR = "../data/test"
BATCH_SIZE = 1
LEARNING_RATE = 1e-5 # 0.00001
LAMBDA_IDENTITY = 0.0
LAMBDA_CYCLE = 10
NUM_WORKERS = 4
NUM_EPOCHS = 10
NUM_RESIDUALS = 9
NUM_FEATURES = 128
LOAD_MODEL = False
SAVE_MODEL = True
CHECKPOINT_GEN_H = "model/genh.pth.tar"
CHECKPOINT_GEN_Z = "model/genz.pth.tar"
CHECKPOINT_CRITIC_H = "model/critich.pth.tar"
CHECKPOINT_CRITIC_Z = "model/criticz.pth.tar"
IMAGE_SIZE_X = 128
IMAGE_SIZE_Y = 1024
IMAGECHANNELS = 1

transforms = A.Compose(
    [
        A.Resize(width=128, height=1024),
        # A.HorizontalFlip(p=0.5),
        # A.Normalize(mean=[0.5], std=[0.5], max_pixel_value=255),
        ToTensorV2(),
    ],
    additional_targets={"image0": "image"},
)