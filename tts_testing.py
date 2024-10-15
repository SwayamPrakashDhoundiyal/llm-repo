import torch
import asyncio
from TTS.api import TTS
import os
import time
import mutagen 
from mutagen.wave import WAVE 

# for playing wav file
# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# Initialize the VITS TTS model (supports emotions)
tts = TTS(model_name="tts_models/en/vctk/vits").to(device)
#print(tts.speakers)
sentence = ""
queue =[]
curr = 0
playing = False

def played(length):
    print("called")
    global playing
    time.sleep(length)
    playing = False
    print("played")

async def play_wav(count,callback):
    global playing
    global queue
    if playing == False:
        print("playing")
        playing = True
        if len(queue):
            del(queue[0])
        audio = WAVE(f"output{count}.wav")
        audio_info = audio.info
        length = audio_info.length
        os.system(f"output{count}.wav")
        callback(length)
    else:
        queue.append(count)

async def tts_func_file(tts =tts,word=None,File_path=None,count=0):
    global sentence
    for char in word:
        count +=1
        if char in [".", "?", "!",":",";"]:
            sentence = sentence+char
            tts.tts_to_file(text=sentence,emotion="Happy",speaker="p335",file_path=f"output{count}.wav")
            print(sentence)
            sentence =""
            await play_wav(count,played)

        else:
            sentence +=char
            await asyncio.sleep(1)

#s = "Emotion synthesis complete. Output saved to emotion_output.wav used in."
#count = 0
    #for word in text:
    #    count +=1
    #    asyncio.run(tts_func_file(word=word,File_path=f"output{count}.wav"))
#
#while len(queue):
#    play_wav(queue[0],played)

#os.system('start /min "emotion_output2.wav"')
def tts_func_file_all(sentence,count):
    tts.tts_to_file(text=sentence,emotion="neutral",speaker="p335",file_path=f"output{count}.wav")
    os.system(f"output{count}.wav")

print(f"Emotion synthesis complete. Output saved to emotion_output.wav used in {device}")
