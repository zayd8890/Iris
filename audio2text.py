# audio2text.py
import whisper

# Load Whisper model once (you can cache or load outside for efficiency)
model = whisper.load_model("small")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes speech from an audio file to text using Whisper.
    """
    try:
        result = model.transcribe(file_path)
        return result.get("text", "")
    except Exception as e:
        print(f"[ERROR] Failed to transcribe: {e}")
        return ""
