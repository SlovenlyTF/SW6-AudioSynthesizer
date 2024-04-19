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
    fluidsynth.midi_to_audio(midi_file, wav_file)

    return wav_file

# Set output_dir as audio_bucket in the current directory
output_dir = os.path.join(os.getcwd(), 'audio_bucket')

# Set toms_diner1.mid as the input MIDI file
midi_file = os.path.join(os.getcwd(), 'toms_diner1.mid')
wav_file = midi_to_wav(midi_file, output_dir)
