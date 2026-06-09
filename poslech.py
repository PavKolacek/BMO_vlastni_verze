import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


MODEL_PATH = r"C:\Users\pavek\Desktop\UNOB\BMO\vosk-model-small-cs-0.4-rhasspy"
SAMPLE_RATE = 16000

audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


def main():
    print("Načítám model...")
    model = Model(MODEL_PATH)

    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    print("Mluv do mikrofonu. Pro ukončení stiskni CTRL+C.")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    print("Rozpoznáno:", text)
            else:
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "")

                if partial_text:
                    print("Průběžně:", partial_text, end="\r")


if __name__ == "__main__":
    main()