"""
Taget fra Aladdin Pearsons GitHub repository:

Training for CycleGAN

Programmed by Aladdin Persson <aladdin.persson at hotmail dot com>
* 2020-11-05: Initial coding
* 2022-12-21: Small revision of code, checked that it works with latest PyTorch version
"""

import torch
from Cyclegan import dataset
# from dataset import HumMusicDataset
import sys
from Cyclegan import utils
# from utils import save_checkpoint, load_checkpoint
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from Cyclegan import config
from tqdm import tqdm
from torchvision.utils import save_image
from Cyclegan import discriminator_model
# from discriminator_model import Discriminator
from Cyclegan import gen_model
# from gen_model import Generator
import numpy as np

class trainer:
    def __init__(self, train_hum_numpy_array = [0], train_music_numpy_array = [0], val_hum_numpy_array = [0], val_music_numpy_array = [0]):
        self.train_hum_numpy_array = train_hum_numpy_array
        self.train_music_numpy_array = train_music_numpy_array

        self.val_hum_numpy_array = val_hum_numpy_array
        self.val_music_numpy_array = val_music_numpy_array

    def train_fn(
        self, disc_H, disc_Z, gen_Z, gen_H, loader, opt_disc, opt_gen, l1, mse, d_scaler, g_scaler, epoch_num
    ):
        H_reals = 0
        H_fakes = 0
        loop = tqdm(loader, leave=True)

        for idx, (music, hum) in enumerate(loop):
            music = music.to(config.DEVICE)
            hum = hum.to(config.DEVICE)

            # Train Discriminators H and Z
            with torch.cuda.amp.autocast():
                fake_hum = gen_H(music)
                D_H_real = disc_H(hum)
                D_H_fake = disc_H(fake_hum.detach())
                H_reals += D_H_real.mean().item()
                H_fakes += D_H_fake.mean().item()
                D_H_real_loss = mse(D_H_real, torch.ones_like(D_H_real))
                D_H_fake_loss = mse(D_H_fake, torch.zeros_like(D_H_fake))
                D_H_loss = D_H_real_loss + D_H_fake_loss

                fake_music = gen_Z(hum)
                D_Z_real = disc_Z(music)
                D_Z_fake = disc_Z(fake_music.detach())
                D_Z_real_loss = mse(D_Z_real, torch.ones_like(D_Z_real))
                D_Z_fake_loss = mse(D_Z_fake, torch.zeros_like(D_Z_fake))
                D_Z_loss = D_Z_real_loss + D_Z_fake_loss

                # put it togethor
                D_loss = (D_H_loss + D_Z_loss) / 2

            opt_disc.zero_grad()
            d_scaler.scale(D_loss).backward()
            d_scaler.step(opt_disc)
            d_scaler.update()

            # Train Generators H and Z
            with torch.cuda.amp.autocast():
                # adversarial loss for both generators
                D_H_fake = disc_H(fake_hum)
                D_Z_fake = disc_Z(fake_music)
                loss_G_H = mse(D_H_fake, torch.ones_like(D_H_fake))
                loss_G_Z = mse(D_Z_fake, torch.ones_like(D_Z_fake))

                # cycle loss
                cycle_music = gen_Z(fake_hum)
                cycle_hum = gen_H(fake_music)
                cycle_music_loss = l1(music, cycle_music)
                cycle_hum_loss = l1(hum, cycle_hum)

                # identity loss (remove these for efficiency if you set lambda_identity=0)
                identity_music = gen_Z(music)
                identity_hum = gen_H(hum)
                identity_music_loss = l1(music, identity_music)
                identity_hum_loss = l1(hum, identity_hum)

                # add all togethor
                G_loss = (
                    loss_G_Z
                    + loss_G_H
                    + cycle_music_loss * config.LAMBDA_CYCLE
                    + cycle_hum_loss * config.LAMBDA_CYCLE
                    + identity_hum_loss * config.LAMBDA_IDENTITY
                    + identity_music_loss * config.LAMBDA_IDENTITY
                )

            opt_gen.zero_grad()
            g_scaler.scale(G_loss).backward()
            g_scaler.step(opt_gen)
            g_scaler.update()

            if idx % 50 == 0:
                save_image(fake_hum * 0.5 + 0.5, f"training_images_hum/epoch_{epoch_num}_index_{idx}.png")
                save_image(fake_music * 0.5 + 0.5, f"training_images_music/epoch_{epoch_num}_index_{idx}.png")

            loop.set_postfix(H_real=H_reals / (idx + 1), H_fake=H_fakes / (idx + 1))


    def run(self, load_saved_model, should_train, epochs):
        disc_H = discriminator_model.Discriminator(in_channels=config.IMAGECHANNELS).to(config.DEVICE)
        disc_Z = discriminator_model.Discriminator(in_channels=config.IMAGECHANNELS).to(config.DEVICE)
        gen_Z = gen_model.Generator(img_channels=config.IMAGECHANNELS).to(config.DEVICE)
        gen_H = gen_model.Generator(img_channels=config.IMAGECHANNELS).to(config.DEVICE)
        opt_disc = optim.Adam(
            list(disc_H.parameters()) + list(disc_Z.parameters()),
            lr=config.LEARNING_RATE,
            betas=(0.5, 0.999),
        )

        opt_gen = optim.Adam(
            list(gen_Z.parameters()) + list(gen_H.parameters()),
            lr=config.LEARNING_RATE,
            betas=(0.5, 0.999),
        )

        L1 = nn.L1Loss()
        mse = nn.MSELoss()

        if load_saved_model:
            utils.load_checkpoint(
                config.CHECKPOINT_GEN_H,
                gen_H,
                opt_gen,
                config.LEARNING_RATE,
            )
            utils.load_checkpoint(
                config.CHECKPOINT_GEN_Z,
                gen_Z,
                opt_gen,
                config.LEARNING_RATE,
            )
            utils.load_checkpoint(
                config.CHECKPOINT_CRITIC_H,
                disc_H,
                opt_disc,
                config.LEARNING_RATE,
            )
            utils.load_checkpoint(
                config.CHECKPOINT_CRITIC_Z,
                disc_Z,
                opt_disc,
                config.LEARNING_RATE,
            )

        data_dataset = dataset.HumMusicDataset(
            hum_numpy_array=self.train_hum_numpy_array,
            music_numpy_array=self.train_music_numpy_array,
            transform=config.transforms,
        )
        data_val_dataset = dataset.HumMusicDataset(
            hum_numpy_array=self.val_hum_numpy_array,
            music_numpy_array=self.val_music_numpy_array,
            transform=config.transforms,
        )
        val_loader = DataLoader(
            data_val_dataset,
            batch_size=1,
            shuffle=False,
            pin_memory=True,
        )
        loader = DataLoader(
            data_dataset,
            batch_size=config.BATCH_SIZE,
            shuffle=True,
            num_workers=config.NUM_WORKERS,
            pin_memory=True,
        )
        
        g_scaler = torch.cuda.amp.GradScaler()
        d_scaler = torch.cuda.amp.GradScaler()
        if should_train:
            for epoch in range(epochs):
                self.train_fn(
                    disc_H,
                    disc_Z,
                    gen_Z,
                    gen_H,
                    loader,
                    opt_disc,
                    opt_gen,
                    L1,
                    mse,
                    d_scaler,
                    g_scaler,
                    epoch_num=epoch,
                )

                if config.SAVE_MODEL:
                    utils.save_checkpoint(gen_H, opt_gen, filename=config.CHECKPOINT_GEN_H)
                    utils.save_checkpoint(gen_Z, opt_gen, filename=config.CHECKPOINT_GEN_Z)
                    utils.save_checkpoint(disc_H, opt_disc, filename=config.CHECKPOINT_CRITIC_H)
                    utils.save_checkpoint(disc_Z, opt_disc, filename=config.CHECKPOINT_CRITIC_Z)

        return gen_H, gen_Z