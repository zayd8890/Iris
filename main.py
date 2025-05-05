import numpy as np
import sounddevice as sd
import soundfile as sf
from audio2text import transcribe_audio
from agent import AgentManager  
from text2audio import speak_text
from tools.light_control import LightControlTool
from tools.fan_control import FanControlTool
from tools.thermostat_control import ThermostatControlTool
import toml

config = toml.load('config.toml')

DEEPSEEK_API = config['secret']['deepseek_api']
AUDIO_FILE = "user_input.wav"
SAMPLERATE = 44100
SILENCE_THRESHOLD = 0.35  # Adjust this value as needed
SILENCE_DURATION = 2.0    # Duration of silence in seconds to stop recording


def record_audio(samplerate=SAMPLERATE):
    print("🎙️ Recording... Speak now.")
    recording = []
    silence_counter = 0
    chunk_duration = 0.5  # Duration of each audio chunk in seconds
    chunk_size = int(samplerate * chunk_duration)

    try:
        with sd.InputStream(samplerate=samplerate, channels=1) as stream:
            while True:
                audio_chunk, _ = stream.read(chunk_size)
                volume = np.linalg.norm(audio_chunk)
                recording.append(audio_chunk)
                print(f"[DEBUG] Volume: {volume:.4f}")
                if volume < SILENCE_THRESHOLD:
                    silence_counter += chunk_duration
                else:
                    silence_counter = 0

                if silence_counter > SILENCE_DURATION:
                    print("🛑 Silence detected. Stopping recording.")
                    break

        audio_data = np.concatenate(recording, axis=0)
        sf.write(AUDIO_FILE, audio_data, samplerate)
        print("✅ Recording complete.")

    except Exception as e:
        print(f"[ERROR] Failed to record audio: {e}")

def main():
    # Initialize the agent with desired configuration
    agent = AgentManager(
        verbose=False,  # Set to True if you want detailed processing logs
        model_id="deepseek/deepseek-chat",  # Can change model here
        temperature=0.7,  # Adjust creativity parameter
        api_key=DEEPSEEK_API,
        tools=[FanControlTool(),ThermostatControlTool(),LightControlTool()]
    )
    
    record_audio()
    user_text = transcribe_audio(AUDIO_FILE)
    print(f"📝 You said: {user_text}")
    
    if user_text:
        # Get only the final answer from the agent
        response = agent.run_query(user_text)
        # Print and speak the clean response
        print(f"🤖 Assistant: {response}")
        speak_text(response)

if __name__ == "__main__":
    main()