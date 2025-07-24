import pyaudio
import wave
import webrtcvad
import collections
import time
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
SILENCE_THRESHOLD = 1.5  # seconds

def record_until_silence(filename="temp.wav"):
    vad = webrtcvad.Vad(2)  # 0–3 (aggressiveness)
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=FRAME_SIZE)

    print("\n🎤 Recording... (auto-stop on silence)")
    frames = []
    ring_buffer = collections.deque(maxlen=int(SILENCE_THRESHOLD * 1000 / FRAME_DURATION))
    start_time = time.time()
    silence_start = None

    try:
        while True:
            frame = stream.read(FRAME_SIZE)
            is_speech = vad.is_speech(frame, RATE)
            frames.append(frame)

            if is_speech:
                silence_start = None
            else:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_THRESHOLD:
                    break

    except KeyboardInterrupt:
        print("⛔ Manually stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("✅ Recording saved.\n")
