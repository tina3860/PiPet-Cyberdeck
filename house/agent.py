import json
import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import subprocess
import tempfile
import os

# Load config
with open("config/config.json", "r") as f:
    config = json.load(f)

OLLAMA_URL = "http://localhost:11434/api/chat"
SAMPLE_RATE = 48000
DURATION = 5
messages = []

def record_audio():
    print("🎤 Listening for 5 seconds...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE,
                       channels=1,
                       device=config["mic_device"])
    sd.wait()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav.write(tmp.name, SAMPLE_RATE, recording)
    return tmp.name

def transcribe(audio_file):
    print("💭 Transcribing...")
    subprocess.run(
        ["whisper", audio_file, "--model", "tiny", "--language", "English", "--output_format", "txt", "--output_dir", "/tmp"],
        capture_output=True, text=True
    )
    base = os.path.splitext(os.path.basename(audio_file))[0]
    txt_file = f"/tmp/{base}.txt"
    if os.path.exists(txt_file):
        with open(txt_file) as f:
            return f.read().strip()
    return ""

def chat(user_input):
    messages.append({"role": "user", "content": user_input})
    response = requests.post(OLLAMA_URL, json={
        "model": config["text_model"],
        "messages": [{"role": "system", "content": config["system_prompt"]}] + messages,
        "stream": False
    })
    reply = response.json()["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return reply

def speak(text):
    print("🔊 Speaking...")
    subprocess.run([
        config["piper_path"],
        "--model", config["voice_model"],
        "--output_file", "/tmp/response.wav"
    ], input=text.encode(), capture_output=True)
    subprocess.run(["aplay", "/tmp/response.wav"])

print("Pet House AI is ready!")
print("  - Press Enter to speak")
print("  - Type a message and press Enter to chat by text")
print("  - Type 'quit' to exit")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break
    elif user_input == "":
        audio_file = record_audio()
        text = transcribe(audio_file)
        if text:
            print(f"You said: {text}")
            response = chat(text)
            print(f"Pip: {response}")
            speak(response)
        else:
            print("Couldn't hear anything, try again!")
    else:
        response = chat(user_input)
        print(f"Pip: {response}")
        speak(response)