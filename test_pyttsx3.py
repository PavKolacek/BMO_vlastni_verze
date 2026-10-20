import pyttsx3

engine = pyttsx3.init()

print("První odpověď")
engine.say("This is the first answer.")
engine.runAndWait()

print("Druhá odpověď")
engine.say("This is the second answer.")
engine.runAndWait()

print("Test dokončen")
