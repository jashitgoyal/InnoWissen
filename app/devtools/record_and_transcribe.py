import sounddevice as sd
from scipy.io.wavfile import write
import requests
import time

FILENAME = "temp.wav"
DURATION = 5  # seconds
SAMPLERATE = 16000  # Hz

def record():
    print(f"Recording for {DURATION} seconds...")
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    write(FILENAME, SAMPLERATE, audio)
    print("Recording saved.")

def transcribe():
    files = {'file': open(FILENAME, 'rb')}
    response = requests.post("http://localhost:8000/transcribe", files=files)
    print("Transcription:", response.json())

if __name__ == "__main__":
    record()
    time.sleep(1)
    transcribe()
