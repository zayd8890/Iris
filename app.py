from flask import Flask, send_from_directory, request, jsonify
import os
import toml
import numpy as np
import noisereduce as nr
from audio2text import transcribe_audio
from text2audio import speak_text
from agent import AgentManager
from tools.fan_control import FanControlTool
from tools.light_control import LightControlTool
from tools.thermostat_control import ThermostatControlTool
import soundfile as sf
import time
import logging
from pydub import AudioSegment

def convert_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(44100)
    audio.export(output_path, format="wav")


# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
AUDIO_FILE = os.path.join(UPLOAD_FOLDER, 'user_input.wav')
RESPONSE_AUDIO = os.path.join(UPLOAD_FOLDER, 'assistant_response.wav')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load config
try:
    config = toml.load('config.toml')
    DEEPSEEK_API = config['secret']['deepseek_api']
except Exception as e:
    logger.error(f"Error loading config: {e}")
    DEEPSEEK_API = os.environ.get('DEEPSEEK_API', '')

# Initialize agent once
try:
    agent = AgentManager(
        verbose=True,  # Set to True for more debugging info
        model_id="deepseek/deepseek-chat",
        temperature=0.7,
        api_key=DEEPSEEK_API,
        tools=[FanControlTool(), ThermostatControlTool(), LightControlTool()]
    )
except Exception as e:
    logger.error(f"Error initializing agent: {e}")
    agent = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        logger.error("No audio file provided in request")
        return "❌ No audio file provided.", 400

    audio = request.files['file']
    raw_audio_path = os.path.join(UPLOAD_FOLDER, 'raw_audio')
    audio.save(raw_audio_path)
    logger.info(f"Saved raw audio file to {raw_audio_path}")

    try:
        # Convert to WAV mono 44.1kHz for consistent format
        audio_segment = AudioSegment.from_file(raw_audio_path)
        audio_segment = audio_segment.set_channels(1).set_frame_rate(44100)
        audio_segment.export(AUDIO_FILE, format="wav")
        logger.info(f"Converted audio to WAV mono 44.1kHz at {AUDIO_FILE}")

        data, samplerate = sf.read(AUDIO_FILE)
        logger.info(f"Audio length: {len(data)}, Sample rate: {samplerate}")
        logger.info(f"Max amplitude: {np.max(np.abs(data))}")

        if len(data) < samplerate * 0.5:
            return "🤖 Recording too short. Please speak longer.", 200
        if np.max(np.abs(data)) < 0.01:
            return "🤖 Audio volume too low. Please speak louder.", 200

        # Apply noise reduction (optional)
        try:
            reduced_noise = nr.reduce_noise(y=data, sr=samplerate)
            sf.write(AUDIO_FILE, reduced_noise, samplerate)
            logger.info("Noise reduction completed")
        except Exception as nr_error:
            logger.error(f"Noise reduction failed: {nr_error}")
            logger.info("Continuing with original audio")

        user_text = transcribe_audio(AUDIO_FILE)
        logger.info(f"Transcription result: '{user_text}'")

        if not user_text.strip():
            return "🤖 No speech detected. Please try again and speak clearly.", 200

        # Check for test command
        if user_text.lower().strip() in ["test", "hello", "hi", "hey"]:
            logger.info("Test command detected")
            return f"✅ Assistant: Hello! I can hear you. Try asking me to control something like 'turn on the lights' or 'set the thermostat to 72 degrees'.", 200

        logger.info(f"Processing query: '{user_text}'")
        start_time = time.time()
        
        if agent is None:
            logger.error("Agent not initialized")
            return "❌ Error: Voice assistant not properly initialized", 500
            
        response = agent.run_query(user_text)
        query_time = time.time() - start_time
        logger.info(f"Query processed in {query_time:.2f} seconds")
        logger.info(f"Assistant response: '{response}'")

        # Generate audio response
        logger.info("Generating speech response...")
        speak_text(response)
        logger.info("Speech generation completed")

        return f"✅ Assistant: {response}", 200
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
        return f"❌ Error: {str(e)}", 500

@app.route('/get_audio_response', methods=['GET'])
def get_audio_response():
    if os.path.exists(RESPONSE_AUDIO):
        return send_from_directory(UPLOAD_FOLDER, 'assistant_response.wav')
    else:
        return "No audio response available", 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "tools": ["fan", "lights", "thermostat"]
    })

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))