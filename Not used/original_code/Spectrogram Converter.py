import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def audio_to_spectrogram(audio_file, output_file=None):
    # Load audio file
    y, sr = librosa.load(audio_file)
    
    # Compute spectrogram
    D = librosa.stft(y)
    spect = librosa.amplitude_to_db(abs(D), ref=np.max)
    
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
audio_file = "randomnoises.wav"
output_file = "spectrogram.png"
audio_to_spectrogram(audio_file, output_file)
