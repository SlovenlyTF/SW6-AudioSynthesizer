from flask import Flask, request, send_file
from scipy.io import wavfile
import io
app = Flask(__name__)

@app.get('/')
def index():
    return 'Hello, EchoPond!'

@app.post('/flip_audio')
def post_flip_audio():
    file = request.files['audio']
    #extract audio from filet
    sr, data = wavfile.read(file.stream)
    #flip audio
    flipped_data = flip_audio(data)
    wav_file = io.BytesIO()
    wavfile.write(wav_file, sr, flipped_data)

    print(request.headers)

    #return audio as wav file
    return send_file(wav_file, mimetype='audio/wav', as_attachment=True, download_name='flipped_audio.wav')
    

def flip_audio(audio):
    return audio[::-1]

@app.get('/host_audio')
def host_audio():
    # return send_file('test.txt', mimetype='text/plain', as_attachment=True, download_name='test.txt')
    return send_file('toms_diner1.wav', mimetype='audio/wav', as_attachment=False, download_name='audio.wav')