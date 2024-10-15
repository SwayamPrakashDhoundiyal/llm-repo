import numpy as np
import sounddevice as sd
from TTS.api import TTS
import torch

# Initialize TTS
device = "cuda" if torch.cuda.is_available() else "cpu"
# Initialize the VITS TTS model (supports emotions)
tts = TTS(model_name="tts_models/en/vctk/vits").to(device)

# Function to synthesize and play speech in chunks
def stream_tts(text, chunk_size=50,done=False):
    # Synthesize the current chunk
    wav = tts.tts(text,speaker="p335")
    # Play the synthesized chunk
    sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
    sd.wait()  # Wait for playback to finish before processing the next chunk