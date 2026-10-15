from ollama import chat
import pyttsx3
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from poslech import collected_text

#setup
engine = pyttsx3.init()
MODEL_PATH = r"C:\Users\pavek\Desktop\UNOB\BMO\vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

#dulezite promenne 
audio_queue = queue.Queue()
collected_text = []
full_odpoved = ""
full_otazka = collected_text
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)


def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

def poslech():

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    collected_text.append(text)
                    print("rozpoznano: ", text)
                    return text

def main():
    print("Zapínáme pásy, zapínáme zapínámeee")
    otazka = poslech()
    print("returnuta otazka: ", otazka)

engine.say(full_odpoved)
engine.runAndWait()