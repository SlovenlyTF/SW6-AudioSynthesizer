from flask import Flask, request, send_file, send_from_directory
import soundfile as sf
from librosa import load as load_wav
from pathlib import Path
import uuid
from to_sine import audio_to_sine, audio_segment_to_samples
from to_midi import audio_to_midi
from midi_to_wav import midi_to_wav, get_soundfont_path
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)

# Constants
BUCKET_DIR = Path('audio_bucket')
# TODO: Fix content types and shit
SUPPORTED_CONTENT_TYPES = ['audio/wav', 'audio/wave', 'application/octet-stream']


def generate_unique_filename():
    # For now strictly hardcoding as wav
    return f'{str(uuid.uuid4())}.wav'


def save_wav_to_bucket(sr, data):
    file_name = generate_unique_filename()
    file_path = BUCKET_DIR / file_name
    
    # Save audio to bucket and return link to the file
    with open(file_path, 'wb') as file:
        sf.write(file, data, sr, format='WAV')

    return f'{request.url_root}bucket/{file_name}'


def save_pydub_generator_to_bucket(generator):
    file_name = generate_unique_filename()
    file_path = BUCKET_DIR / file_name
    
    # Save audio to bucket and return link to the file
    generator.export(out_f=file_path, format="wav")

    return f'{request.url_root}bucket/{file_name}'


@app.get('/')
def get_index():
    return 'Hello, EchoPond!'


def get_input_file(request):
    if 'audio' not in request.files:
        return None, {
            'status': 'fail',
            'data': {
                'audio': 'No audio file uploaded.'
            }
        }, 400
    
    input_file = request.files['audio']
    
    # Return error if file type is not supported
    # TODO: Does this check the actual file or an http header?
    if input_file.content_type not in SUPPORTED_CONTENT_TYPES:
        return None, {
            'status': 'fail',
            'data': {
                'mediaType': f'Unsupported Media Type "{input_file.content_type}".',
            }
        }, 415
    
    return input_file, None, None


def process_audio(request, operation):
    input_file, error_response, error_code = get_input_file(request)
    if error_response:
        return error_response, error_code
    
    # Extract audio from filet
    input_data, input_sr = load_wav(input_file.stream)
    
    # Flip audio
    new_sr, new_data = operation(input_sr, input_data)
    
    # Return bucket URL for resulting file
    try:
        result_url = save_wav_to_bucket(new_sr, new_data)
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Failed to save file to bucket.',
        }, 500
    
    return {
        'status': 'success',
        'data': {
            'resultUrl': result_url
        }
    }, 200


@app.post('/api/flip-audio')
def post_flip_audio():
    return process_audio(request, lambda sr,data : (sr,data[::-1]))


@app.post('/api/to-sine')
def post_to_sine():
    return process_audio(request, lambda sr,data : audio_segment_to_samples(audio_to_sine(sr, data)))


# Perhaps a bit too mouthy about where errors occur
@app.post('/api/to-midi')
def post_to_midi():
    # Get input file
    input_file, error_message, error_code = get_input_file(request)
    if error_message:
        return error_message, error_code
    
    # Get soundfont
    soundfont_path, error_message, error_code = get_soundfont_path(request)
    if error_message:
        return error_message, error_code
    
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav')
        input_file.save(temp_file.name)
        
        # Convert audio to midi
        file_name_base = str(uuid.uuid4())
        midi_path = str(BUCKET_DIR / f'{file_name_base}.mid')
        # Right now audio_to_midi saves midi in bucket, we can serve it or remove it
        audio_to_midi(temp_file.name, midi_path)
        temp_file.close()
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to convert audio to midi.',
        }, 500
    
    try:
        # Convert midi to wav
        midi_to_wav(midi_path, BUCKET_DIR, soundfont_path)
        result_url = f'{request.url_root}bucket/{file_name_base}.wav' # Bad but I can't be arsed rn
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Failed to convert midi to wav.',
        }, 500
    
    return {
        'status': 'success',
        'data': {
            'resultUrl': result_url
        }
    }, 200


# Safely host files in audio_bucket directory
@app.route('/bucket/<path:path>')
def send_report(path):
    return send_from_directory(BUCKET_DIR, path)


# Create the app for use with waitress
def create_app():
    # Create bucket directory if it doesn't exist
    BUCKET_DIR.mkdir(exist_ok=True)
    return app
