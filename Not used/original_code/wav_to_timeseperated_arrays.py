import numpy as np
import librosa
import math

def audio_to_arrays(audio_file, timestep):

    # Load audio file
    y, sr = librosa.load(audio_file)
    # Compute the Short-Time Fourier Transform (STFT)
    stft = np.abs(librosa.stft(y))

    # Extract frequencies
    audio_duration = len(y) / sr  # Assuming y and sr are already defined
    samples = []

    for i in range(math.ceil(audio_duration / timestep)):
        if i == math.ceil(audio_duration / timestep) - 1:
            samples.append(y[int(i * (sr * timestep)):])
            for j in range(int((i + 1) * (sr * timestep)) - len(y)):
                samples[i] = np.append(samples[i], 0)
        else:
            samples.append(y[int(i * (sr * timestep)):int((i + 1) * (sr * timestep))])
        print(samples[i].shape, end='')
    return samples