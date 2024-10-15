import os
import sys
import queue
import sounddevice as sd
import vosk
import json

paragraph=""
count=0

# Load Vosk model
model = vosk.Model("vosk-model-en-in-0.5")

# Initialize a queue to buffer the audio data
audio_queue = queue.Queue()

# Define a callback to feed the audio data to the queue
def callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))

# Open a stream for real-time audio input
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    recognizer = vosk.KaldiRecognizer(model, 16000)

    print("Listening...")

    try:
        while True:
            # Get the audio data from the queue
            data = audio_queue.get()

            # If audio data is available, process it
            if recognizer.AcceptWaveform(data):
                # Output recognized text for complete utterances
                result = recognizer.Result()
                result_dict = json.loads(result)
                if not paragraph:
                    paragraph += result_dict.get("text", "").replace("question mark","?").replace("questionmark","?")
                else:
                    paragraph += str(" " + result_dict.get("text", "")).replace("question mark","?").replace("questionmark","?")
            else:
                # Output partial results (for faster feedback)
                partial_result = recognizer.PartialResult()
                result_dict = json.loads(partial_result)
                if not result_dict.get("text", "") and count < 10:
                    count += 1

                elif result_dict.get("text", ""):
                    count = 0
                elif count > 9:
                    txt = result_dict.get("text", "")
                    paragraph += f"(Queue ended.{txt})"
                    paragraph += "\n"
                    count = 0


            sys.stdout.write("\033c")
            print(paragraph)
    
    except KeyboardInterrupt:
        print("Last paragraph is:\n")
        print(paragraph)