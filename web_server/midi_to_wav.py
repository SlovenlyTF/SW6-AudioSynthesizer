from midi2audio import FluidSynth
from pydub import AudioSegment
from os import path, listdir, makedirs

SOUNDFONT_DIR = path.join(path.dirname(__file__), 'soundfonts')

# Get all filenames in SOUNDFONT_DIR
SOUNDFONTS = [f for f in listdir(SOUNDFONT_DIR) if path.isfile(SOUNDFONT_DIR / f)]


def midi_to_wav(midi_file, output_dir, soundfont, volume_change=20):
    # Create output directory if it doesn't exist
    if not path.exists(output_dir):
        makedirs(output_dir)

    # Initialize FluidSynth
    fluidsynth = FluidSynth(soundfont, 22050)

    # Convert MIDI to WAV
    wav_file = path.join(output_dir, path.splitext(path.basename(midi_file))[0] + '.wav')
    fluidsynth.midi_to_audio(midi_file, wav_file)
    
    # Change volume
    audio = AudioSegment.from_wav(wav_file)
    audio = audio + volume_change
    audio.export(wav_file, "wav")

    return wav_file


def get_soundfont_path(request):
  if 'soundfont' not in request.files:
    return {
      'status': 'fail',
      'data': {
        'message': 'No soundfont provided'
      }
    }, 400
  
  soundfont = request.files['soundfont']
  
  if soundfont not in SOUNDFONTS:
    return {
      'status': 'fail',
      'data': {
        'message': f'Invalid soundfont provided: {soundfont}'
      }
    }, 400
  
  return SOUNDFONT_DIR / soundfont
