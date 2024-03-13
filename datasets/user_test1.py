# Delvist stjålet fra
# https://thewolfsound.com/how-to-auto-tune-your-voice-with-python/

#!/usr/bin/python3
from functools import partial
from pathlib import Path
import argparse
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import scipy.signal as sig
import musicalbeeps


SEMITONES_IN_OCTAVE = 12


def degrees_from(scale: str):
    """Return the pitch classes (degrees) that correspond to the given scale"""
    degrees = librosa.key_to_degrees(scale)
    # To properly perform pitch rounding to the nearest degree from the scale, we need to repeat
    # the first degree raised by an octave. Otherwise, pitches slightly lower than the base degree
    # would be incorrectly assigned.
    degrees = np.concatenate((degrees, [degrees[0] + SEMITONES_IN_OCTAVE]))
    return degrees


def closest_pitch(f0):
    """Round the given pitch values to the nearest MIDI note numbers"""
    midi_note = np.around(librosa.hz_to_midi(f0))
    # To preserve the nan values.
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    # Convert back to Hz.
    return librosa.midi_to_hz(midi_note)


def closest_pitch_from_scale(f0, scale):
    """Return the pitch closest to f0 that belongs to the given scale"""
    # Preserve nan.
    if np.isnan(f0):
        return np.nan
    degrees = degrees_from(scale)
    midi_note = librosa.hz_to_midi(f0)
    # Subtract the multiplicities of 12 so that we have the real-valued pitch class of the
    # input pitch.
    degree = midi_note % SEMITONES_IN_OCTAVE
    # Find the closest pitch class from the scale.
    degree_id = np.argmin(np.abs(degrees - degree))
    # Calculate the difference between the input pitch class and the desired pitch class.
    degree_difference = degree - degrees[degree_id]
    # Shift the input MIDI note number by the calculated difference.
    midi_note -= degree_difference
    # Convert to Hz.
    return librosa.midi_to_hz(midi_note)


def aclosest_pitch_from_scale(f0, scale):
    """Map each pitch in the f0 array to the closest pitch belonging to the given scale."""
    sanitized_pitch = np.zeros_like(f0)
    for i in np.arange(f0.shape[0]):
        sanitized_pitch[i] = closest_pitch_from_scale(f0[i], scale)
    # Perform median filtering to additionally smooth the corrected pitch.
    smoothed_sanitized_pitch = sig.medfilt(sanitized_pitch, kernel_size=11)
    # Remove the additional NaN values after median filtering.
    smoothed_sanitized_pitch[np.isnan(smoothed_sanitized_pitch)] = \
        sanitized_pitch[np.isnan(smoothed_sanitized_pitch)]
    return smoothed_sanitized_pitch


def get_corrected_pitches(audio, sr, correction_function):
    # Set some basis parameters.
    frame_length = 2048
    hop_length = frame_length // 4
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')

    # Pitch tracking using the PYIN algorithm.
    f0, voiced_flag, voiced_probabilities = librosa.pyin(audio,
                                                         frame_length=frame_length,
                                                         hop_length=hop_length,
                                                         sr=sr,
                                                         fmin=fmin,
                                                         fmax=fmax)

    # Apply the chosen adjustment strategy to the pitch.
    return correction_function(f0)


def generate_piano_sounds(notes, duration):
    # Initialize the player
    player = musicalbeeps.Player(volume=0.5, mute_output=False)

    # Play notes
    for note in notes:
        player.play_note(note, duration)


def main():
    # Parse the command line arguments.
    ap = argparse.ArgumentParser()
    ap.add_argument('vocals_file')
    ap.add_argument('--correction-method', '-c', choices=['closest', 'scale'], default='closest')
    ap.add_argument('--scale', '-s', type=str, help='see librosa.key_to_degrees;'
                                                    ' used only for the \"scale\" correction'
                                                    ' method')
    args = ap.parse_args()
    
    filepath = Path(args.vocals_file)

    # Load the audio file.
    print('Loading audio file...')
    y, sr = librosa.load(str(filepath), sr=None, mono=False)

    # Only mono-files are handled. If stereo files are supplied, only the first channel is used.
    if y.ndim > 1:
        y = y[0, :]

    # Pick the pitch adjustment strategy according to the arguments.
    correction_function = closest_pitch if args.correction_method == 'closest' else \
        partial(aclosest_pitch_from_scale, scale=args.scale)

    # Get the corrected pitches.
    print('Calculating corrected pitches...')
    corrected_pitches = get_corrected_pitches(y, sr, correction_function)
    notes = [librosa.hz_to_note(hz) for hz in corrected_pitches]

    print('Generating piano sounds...')
    piano_sound = generate_piano_sounds(notes, len(y)/sr)
    """
    print('Saving piano to file...')
    piano_filepath = filepath.parent / (filepath.stem + '_piano' + filepath.suffix)
    sf.write(str(piano_filepath), piano_sound, sr)
    """


if __name__=='__main__':
    main()
