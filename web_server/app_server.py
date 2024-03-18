from flask import Flask, request, send_file, send_from_directory
import soundfile as sf
from librosa import load as load_wav
from pathlib import Path
import uuid
from to_sine import audio_to_sine, audio_segment_to_samples

app = Flask(__name__)

# Constantss
BUCKET_DIR_NAME = 'audio_bucket'
# TODO: Fix content types and shit
SUPPORTED_CONTENT_TYPES = ['audio/wav', 'audio/wave', 'application/octet-stream']


def generate_unique_filename():
    # For now strictly hardcoding as wav
    return f'{str(uuid.uuid4())}.wav'


def save_wav_to_bucket(sr, data):
    file_name = generate_unique_filename()
    file_path = Path(BUCKET_DIR_NAME) / file_name
    
    # Save audio to bucket and return link to the file
    with open(file_path, 'wb') as file:
        sf.write(file, data, sr, format='WAV')

    return f'{request.url_root}bucket/{file_name}'


def save_pydub_generator_to_bucket(generator):
    file_name = generate_unique_filename()
    file_path = Path(BUCKET_DIR_NAME) / file_name
    
    # Save audio to bucket and return link to the file
    generator.export(out_f=file_path, format="wav")

    return f'{request.url_root}bucket/{file_name}'


@app.get('/')
def get_index():
    return 'Hello, EchoPond!'


def process_audio(operation):    
    if 'audio' not in request.files:
        return {
            'status': 'fail',
            'data': {
                'audio': 'No audio file uploaded.'
            }
        }, 400
    
    input_file = request.files['audio']
    
    # Return error if file type is not supported
    # TODO: Does this check the actual file or an http header?
    if input_file.content_type not in SUPPORTED_CONTENT_TYPES:
        print(f'Unsupported Media Type "{input_file.content_type}".')
        return {
            'status': 'fail',
            'data': {
                'mediaType': f'Unsupported Media Type "{input_file.content_type}".',
            }
        }, 415
    
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
            'message': f'Failed to save file to bucket.',
        }, 500
    
    return {
        'status': 'success',
        'data': {
            'resultUrl': result_url
        }
    }, 200


@app.post('/api/flip-audio')
def post_flip_audio():
    return process_audio(lambda sr,data : (sr,data[::-1]))


@app.post('/api/to-sine')
def post_to_sine():
    return process_audio(lambda sr,data : audio_segment_to_samples(audio_to_sine(sr, data)))


# Safely host files in audio_bucket directory
@app.route('/bucket/<path:path>')
def send_report(path):
    return send_from_directory(BUCKET_DIR_NAME, path)
