from ollama import chat
import pyttsx3
from poslech import main as listen

# Inicializace TTS
engine = pyttsx3.init()

# Získání otázky z poslech.py
full_otazka = listen()
full_odpoved = ""

# Komunikace s Ollama
stream = chat(
    model='gemma4',
    messages=[{'role': 'user', 'content': full_otazka}],
    stream=True,
)

for chunk in stream:
    part = chunk['message']['content']
    full_odpoved += part

# Hlasová odpověď
engine.say(full_odpoved)
engine.runAndWait()
