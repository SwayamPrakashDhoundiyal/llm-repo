import speech_recognition as sr

def process_audio_chunk(chunk, recognizer):
    try:
        # Recognize the chunk using Google's speech recognition
        text = recognizer.recognize_google(chunk)
        print(f"Recognized: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Request failed: {e}")

def stream_and_recognize():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        # Adjust the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")

        while True:
            try:
                # Listen to audio in chunks (stream mode)
                audio_chunk = recognizer.listen(source, phrase_time_limit=2)
                process_audio_chunk(audio_chunk, recognizer)
            except KeyboardInterrupt:
                print("Stopping the recognition")
                break

if __name__ == "__main__":
    stream_and_recognize()
