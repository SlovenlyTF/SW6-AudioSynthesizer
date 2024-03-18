# Delvist stjålet fra
# https://thewolfsound.com/how-to-auto-tune-your-voice-with-python/

#!/usr/bin/python3
from functools import partial
import librosa
import librosa.display
import numpy as np
import scipy.signal as sig

from pydub.generators import Sine
from pydub.utils import mediainfo

# Constants
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


def generate_piano_sounds(hz_list,durations):
    waves = []
    # Play notes
    for (hz,duration) in zip(hz_list,durations):
        wave = Sine(hz).to_audio_segment(duration=duration*1000)
        waves.append(wave)
        
    return sum(waves)


def frequencies_to_hz_and_durations(frequencies, delta_time_seconds):
    hz_list = []
    durations = []
    prev_hz = None
    
    i = -1
    
    for hz in frequencies:
        if hz != prev_hz:
            prev_hz = hz
            hz_list.append(hz)
            durations.append(delta_time_seconds)
            i += 1
        else:
            durations[i] += delta_time_seconds
    
    return (hz_list,durations)


def consolidate_durations(hz_list,durations,duration_threshold=0.05):
    new_hz_list = []
    new_durations = []
    for i,duration in enumerate(durations):
        if duration < duration_threshold and i > 0:
            new_durations[-1] += duration
        else:
            new_hz_list.append(hz_list[i])
            new_durations.append(duration)
    
    return (new_hz_list,new_durations)


def fix_durations(hz_list,durations):
    new_durations = []
    for i,duration in enumerate(durations):
        if hz_list[i] == 0:
            new_durations.append(duration)
            continue
        
        delta = 0.5 / hz_list[i]
        adjustment = duration % delta
        if adjustment > delta / 2:
            new_durations.append(duration + delta - adjustment)
        else:
            new_durations.append(duration - adjustment)
    
    return new_durations


def audio_to_sine(sr, data, scale='C:min', correction_method='closest'):
  # Only mono-files are handled. If stereo files are supplied, only the first channel is used.
    if data.ndim > 1:
        data = data[0, :]

    # Pick the pitch adjustment strategy according to the arguments.
    correction_function = closest_pitch if correction_method == 'closest' else \
        partial(aclosest_pitch_from_scale, scale=scale)

    # Get the corrected pitches.
    corrected_pitches = get_corrected_pitches(data, sr, correction_function)
    corrected_pitches = np.nan_to_num(corrected_pitches, 1)
    # Moving up 2 octaves for now - straight from ass
    corrected_pitches = [p*4 for p in corrected_pitches]
    
    (hz,durations) = frequencies_to_hz_and_durations(corrected_pitches, (len(data)/sr)/len(corrected_pitches))
    (hz,durations) = consolidate_durations(hz,durations)
    durations = fix_durations(hz,durations)

    return generate_piano_sounds(hz,durations)
    
    """
    print('Saving piano to file...')
    piano_filepath = output_dir / (filepath.stem + '_piano' + filepath.suffix)
    piano_waveasdasd.export(out_f=piano_filepath.resolve(), format="wav")
    """

def audio_segment_to_samples(audio_segment):
    data = audio_segment.get_array_of_samples()
    sr = audio_segment.frame_rate
    return sr, data
