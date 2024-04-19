from midi2audio import FluidSynth
import os

def midi_to_wav(midi_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize FluidSynth
    fluidsynth = FluidSynth('piano.sf2', 22050)

    # Convert MIDI to WAV
    wav_file = os.path.join(output_dir, os.path.splitext(os.path.basename(midi_file))[0] + '.wav')
    print("Converting MIDI to WAV:", midi_file, "=>", wav_file)
    fluidsynth.midi_to_audio(midi_file, wav_file)

    return wav_file

# Example usage
'''
midi_file = "bach_846.mid"
output_dir = "output_directory"
wav_file = midi_to_wav(midi_file, output_dir)
print("WAV file generated:", wav_file)
'''

# Convert all MIDI files in a directory to WAV
midi_dir = "C:\\University\\dataset_sw6\\piano_midi"
output_dir = "C:\\University\\dataset_sw6\\constructed_wav"
for midi_file in os.listdir(midi_dir):
    if midi_file.endswith(".mid"):
        midi_file = os.path.join(midi_dir, midi_file)
        wav_file = midi_to_wav(midi_file, output_dir)
        print("WAV file generated:", wav_file)