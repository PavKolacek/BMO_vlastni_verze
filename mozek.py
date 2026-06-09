from ollama import chat
import pyttsx3
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import time

#setup
engine = pyttsx3.init()
MODEL_PATH = r"C:\Users\pavek\Desktop\UNOB\BMO\vosk-model-small-cs-0.4-rhasspy"
SAMPLE_RATE = 32000

#dulezite promenne 
audio_queue = queue.Queue()
full_odpoved = ""
full_otazka = ""
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)


def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):
    data = audio_queue.get()

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")

        if text:
            full_otazka += text
            print("Rozpoznáno:", text)
    else:
        partial = json.loads(recognizer.PartialResult())
        partial_text = partial.get("partial", "")

        if partial_text:
            full_otazka += partial_text
            print("Průběžně:", partial_text, end="\r")

stream = chat(
    model='gemma4',
    messages=[{'role': 'user', 'content': 'who or what are you'}],
    stream=True,
)

for chunk in stream:
    part = chunk['message']["content"]
    full_odpoved += part
    
    
engine.say(full_odpoved)
engine.runAndWait()