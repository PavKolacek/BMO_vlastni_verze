import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


MODEL_PATH = r"C:\Users\pavek\Desktop\UNOB\BMO\vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

audio_queue = queue.Queue()
collected_text = []

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


def main():
    print("Načítám model...")
    model = Model(MODEL_PATH)

    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    print("Mluv do mikrofonu. Pro ukončení stiskni CTRL+C.")
    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=16000,
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
                        collected_text.append(text)
                        print("Rozpoznáno:", text)
                        return text
                        print("collected text: ", " ".join(collected_text))
                        print("-" * 40)

    except KeyboardInterrupt:
        print("\n Program gone")
        final_text = " ".join(collected_text)
        print(final_text)


if __name__ == "__main__":
    main()