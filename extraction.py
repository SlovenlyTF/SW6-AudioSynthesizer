import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def audio_to_spectrogram(audio_file, output_file=None):

    # Load audio file
    y, sr = librosa.load(audio_file)

    # Compute the Short-Time Fourier Transform (STFT)
    stft = np.abs(librosa.stft(y))

    timestep = 1  # seconds
    # Extract frequencies
    audio_duration = len(y) / sr  # Assuming y and sr are already defined
    time_range = range(0, int(audio_duration), timestep)
    for t in time_range:
        # Compute frequencies at each time step
        frequencies = librosa.core.fft_frequencies(sr=sr)
        print(f"Time: {t} s")
        print(frequencies)
          # Convert frequencies to notes
        notes=[]
        for i in range(1, len(frequencies)):
            notes.append(librosa.hz_to_note(frequencies[i]))
        print(notes)

    # Extract times
    times = librosa.core.frames_to_time(np.arange(stft.shape[1]), sr=sr)
  
    # Extract pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
   
    # Extract harmonic pitches
    harmonics = librosa.effects.harmonic(y)
    h_pitches, h_magnitudes = librosa.piptrack(y=harmonics, sr=sr)

    # Compute spectrogram
    stft = librosa.stft(y)
    spect = librosa.amplitude_to_db(abs(stft), ref=np.max)
    
    # Plot and save spectrogram
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(spect, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

# Example usage
audio_file = "goat.wav"
output_file = "spectrogram.png"
audio_to_spectrogram(audio_file, output_file)
