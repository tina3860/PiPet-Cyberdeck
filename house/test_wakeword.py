import numpy as np
import pyaudio
from scipy import signal
from openwakeword.model import Model

# Load wake word model
m = Model(wakeword_model_paths=['/home/tina386/PiPet-Cyberdeck-Ecosystem/house/models/Hey_Pip.onnx'])

# Audio settings
MIC_RATE = 44100  # Your mic's native sample rate
TARGET_RATE = 16000  # OpenWakeWord needs this
CHUNK_44K = int(1280 * MIC_RATE / TARGET_RATE)  # ~3520 samples at 44100Hz

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=MIC_RATE,
    input=True,
    input_device_index=2,  # Device 2 (USB PnP Sound Device)
    frames_per_buffer=CHUNK_44K
)

print('🎤 Listening for wake word... (say "hey Pip" or your custom phrase)')
print('Press Ctrl+C to stop')

try:
    while True:
        # Read audio at 44100 Hz
        data = stream.read(CHUNK_44K, exception_on_overflow=False)
        audio_44k = np.frombuffer(data, dtype=np.int16)

        # Resample to 16000 Hz for OpenWakeWord
        audio_16k = signal.resample(audio_44k, 1280).astype(np.int16)

        # Predict
        m.predict(audio_16k)

        # Check for detection
        for name, score in m.prediction_buffer.items():
            if score[-1] > 0.5:
                print(f'✨ Wake word detected! Score: {score[-1]:.2f}')

except KeyboardInterrupt:
    print('\n👋 Stopped')
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
