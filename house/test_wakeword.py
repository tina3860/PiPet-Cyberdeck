import numpy as np
import pyaudio
from openwakeword.model import Model

# Load wake word model
m = Model()
print("Available wake words:", list(m.models.keys()))

# Audio settings - record directly at 16000Hz
MIC_RATE = 16000  # OpenWakeWord's native rate
CHUNK = 1280  # OpenWakeWord's chunk size

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=MIC_RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print('🎤 Listening for default wake words... (say "Alexa" or "Hey Jarvis")')
print('Press Ctrl+C to stop')

try:
    while True:
        # Read audio at 16000 Hz (no resampling needed!)
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_16k = np.frombuffer(data, dtype=np.int16)

        # Predict
        m.predict(audio_16k)

        # Check for detection
        for name, scores in m.prediction_buffer.items():
            if scores[-1] > 0.5:
                print(f'✨ Wake word detected: {name} - Score: {scores[-1]:.2f}')

except KeyboardInterrupt:
    print('\n👋 Stopped')
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()