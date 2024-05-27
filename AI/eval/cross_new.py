import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

def load_wav_file(file_path):
    try:
        sampling_rate, signal = wav.read(file_path)
        print(f'Successfully loaded {file_path} with sampling rate {sampling_rate}')
        return sampling_rate, signal
    except Exception as e:
        print(f'Error loading {file_path}: {e}')
        return None, None

def preprocess_signal(signal, downsample_factor=10):
    if signal is None:
        return None
    # If stereo, convert to mono by averaging the two channels
    if signal.ndim > 1:
        signal = signal.mean(axis=1)
    # Downsample the signal to make processing faster
    signal = signal[::downsample_factor]
    # Normalize the signal
    signal = (signal - np.mean(signal)) / np.std(signal)
    return signal

# Load .wav files
file1 = 'audio/postprocess/original_mario.wav'
file2 = 'audio/postprocess/original_mario.wav'
sampling_rate1, signal1 = load_wav_file(file1)
sampling_rate2, signal2 = load_wav_file(file2)

# Check if loading was successful
if sampling_rate1 is None or sampling_rate2 is None:
    print("Error: One or both of the signals could not be loaded.")
else:
    # Print sampling rates for verification
    print(f'Sampling rate 1: {sampling_rate1}')
    print(f'Sampling rate 2: {sampling_rate2}')

    # Preprocess signals with downsampling
    downsample_factor = 10
    signal1 = preprocess_signal(signal1, downsample_factor)
    signal2 = preprocess_signal(signal2, downsample_factor)

    # Ensure signals are loaded correctly
    if signal1 is None or signal2 is None:
        print("Error: One or both of the signals could not be loaded.")
    else:
        # Ensure signals are the same length (truncate the longer one)
        min_length = min(len(signal1), len(signal2))
        signal1 = signal1[:min_length]
        signal2 = signal2[:min_length]

        # Compute cross-correlation
        cross_corr = np.correlate(signal1, signal2, mode='full')
        lags = np.arange(-len(signal1) + 1, len(signal1))

        # Find the lag with the highest absolute cross-correlation value
        max_corr_index = np.argmax(np.abs(cross_corr))
        best_lag = lags[max_corr_index]
        best_corr = cross_corr[max_corr_index]

        # Calculate time in seconds for the best lag
        time_seconds = best_lag / sampling_rate1  # Assuming both signals have the same sampling rate

        # Print the lag with the highest similarity and corresponding time in seconds
        print(f'Best similarity at lag: {best_lag} samples with cross-correlation value: {best_corr}')
        print(f'Time in seconds for lag {best_lag} samples: {time_seconds:.6f} seconds')

        # Plot the cross-correlation values
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(lags, cross_corr, label='Cross-correlation')
        ax.axvline(x=0, color='r', linestyle='--', label='Zero lag')
        ax.axvline(x=best_lag, color='black', linestyle='--', label=f'Best lag: {best_lag}')
        ax.set_xlabel('Lag (samples)')
        ax.set_ylabel('Cross-correlation Amplitude')
        ax.set_title('Cross-correlation')
        ax.legend()

        plt.show()
