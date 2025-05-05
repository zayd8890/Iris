# text2audio.py
import pyttsx3

# Initialize TTS engine once
engine = pyttsx3.init()

def speak_text(text: str):
    """
    Speaks the given text aloud using the system's TTS engine.
    """
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Failed to speak text: {e}")
