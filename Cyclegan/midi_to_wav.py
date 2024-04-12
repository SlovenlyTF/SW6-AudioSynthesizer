from midi2audio import FluidSynth
import os

def midi_to_wav(midi_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize FluidSynth
    fluidsynth = FluidSynth()

    # Convert MIDI to WAV
    wav_file = "output.wav" # os.path.join(output_dir, os.path.splitext(os.path.basename(midi_file))[0] + '.wav')
    print("Converting MIDI to WAV:", midi_file, "=>", wav_file)
    fluidsynth.midi_to_audio(midi_file, wav_file)

    return wav_file

# Example usage
midi_file = "bach_846.mid"
output_dir = "output_directory"
wav_file = midi_to_wav(midi_file, output_dir)
print("WAV file generated:", wav_file)
