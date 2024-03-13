from pydub import AudioSegment
from pydub.playback import play
import numpy as np


# Function for autotuning imported audio
def auto_tune(input_file, output_file, target_frequency):
    # Load audio file
    audio = AudioSegment.from_file(input_file)

    # Define tuning factor
    tuning_factor = target_frequency / audio.frame_rate

    # Apply pitch shift to match target frequency
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * tuning_factor)
    })

    # Export autotuned audio
    audio.export(output_file, format="wav")
    print("Autotuning complete!")


if __name__ == '__main__':
  # Load audio file
  y, sr = librosa.load(audio_file)
  
  