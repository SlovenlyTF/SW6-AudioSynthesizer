import numpy as np
import librosa
import librosa.display
import math
import matplotlib.pyplot as plt

def audio_to_spectrograms(audio_file, timestep):

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

    # Compute spectrogram
    spect = []
    for i in range(len(samples)):
        stft = librosa.stft(samples[i])
        spect.append(librosa.amplitude_to_db(abs(stft), ref=np.max))
    
        # Plot and save spectrogram
        plt.figure(figsize=(4, 2))
        librosa.display.specshow(spect[i], sr=sr, x_axis='time', y_axis='log')
        # plt.colorbar(format='%+2.0f dB')
        # plt.title('Spectrogram')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        plt.tight_layout()
    return spect