import librosa
import numpy as np

def detect_sustained_note(wav_file, threshold=0.01):
    # Load the audio file
    y, sr = librosa.load(wav_file)

    # Compute the short-time Fourier transform (STFT)
    D = librosa.stft(y)

    # Compute the energy (magnitude) of each frame
    energy = np.abs(D)

    # Compute the frame-wise energy change
    energy_change = np.diff(energy, axis=1)

    # Find the frame where energy change exceeds the threshold
    onset_frame_idx = np.where(energy_change > threshold)

    # If no frame exceeds the threshold, return None
    if len(onset_frame_idx[1]) == 0:
        return None

    # Get the first occurrence of onset
    onset_frame = onset_frame_idx[1][0]

    # Convert the frame index to time
    onset_time = librosa.frames_to_time([onset_frame], sr=sr)[0]  # Convert to list before passing to frames_to_time

    return onset_time

def cut_attack_and_release(wav_file, output_file, attack_duration=0.1, release_duration=0.1):
    # Load the audio file
    y, sr = librosa.load(wav_file)

    # Detect the onset of the sustained note
    onset_time = detect_sustained_note(wav_file)

    # If no onset detected, return
    if onset_time is None:
        print("No sustained note detected.")
        return

    # Convert time to samples
    attack_samples = int(attack_duration * sr)
    release_samples = int(release_duration * sr)

    # Calculate the indices to cut
    attack_end_index = int(onset_time * sr) - attack_samples
    release_start_index = int(onset_time * sr)

    # Ensure valid indices
    attack_end_index = max(attack_end_index, 0)
    release_start_index = min(release_start_index, len(y))

    # Cut the attack and release
    cut_audio = np.concatenate((y[:attack_end_index], y[release_start_index:]))

    # Save the output file
    librosa.output.write_wav(output_file, cut_audio, sr)

# Example usage
input_file = 'aah.wav'
output_file = 'haa.wav'
cut_attack_and_release(input_file, output_file)