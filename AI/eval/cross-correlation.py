#Fully made by chatGPT 3.5

import numpy as np
import scipy.signal
import soundfile as sf
import matplotlib.pyplot as plt
from tqdm import tqdm  # Import tqdm for progress bar

def cross_correlation(audio1, audio2):
    # Load audio files
    data1, sr1 = sf.read(audio1)
    data2, sr2 = sf.read(audio2)
    
    # Ensure both audio files have the same sample rate
    assert sr1 == sr2, "Sample rates of the audio files must be the same"
    print(f"Sample rate: {sr1} Hz")
    print(f"Sample rate: {sr2} Hz")
    
    # Ensure data is 1-dimensional (mono audio)
    if len(data1.shape) > 1:
        data1 = data1[:, 0]  # Take only the first channel
    if len(data2.shape) > 1:
        data2 = data2[:, 0]  # Take only the first channel
    
    # Perform cross-correlation
    corr = scipy.signal.correlate(data1, data2, mode='full')
    time_shifts = np.linspace(-len(data1)/sr1, len(data1)/sr1, num=len(corr))
    
    return time_shifts, corr

def plot_cross_correlation(time_shifts, corr):
    # Plot cross-correlation
    plt.figure(figsize=(10, 5))
    plt.plot(time_shifts, corr)
    plt.title('Cross-correlation of Audio Files')
    plt.xlabel('Time Shift (s)')
    plt.ylabel('Correlation')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Example usage
    audio_file1 = 'audio/piano_fra_youtube_til_ssim.wav'  # Replace with your audio file path
    audio_file2 = 'audio/generated_piano_til_ssim.wav'  # Replace with your audio file path
    
    # Compute cross-correlation
    print("Computing cross-correlation...")
    with tqdm(total=100) as pbar:  # Initialize tqdm progress bar
        time_shifts, corr = cross_correlation(audio_file1, audio_file2)
        pbar.update(100)  # Update progress bar to 100% when done
    
    # Plot results
    plot_cross_correlation(time_shifts, corr)