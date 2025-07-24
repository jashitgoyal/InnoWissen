import sounddevice as sd
from scipy.io.wavfile import write
import requests
import time
import argparse
from pydub import AudioSegment
from pydub.playback import play
from app.services.record_utils import record_until_silence

AUDIO_FILENAME = "temp.wav"
RECORD_SECONDS = 5
SAMPLE_RATE = 16000

def record_audio():
    print("\n🎤 Recording (auto-stop on silence)...")
    record_until_silence(AUDIO_FILENAME)
    print("✅ Recording saved.\n")

def transcribe_audio():
    files = {'file': open(AUDIO_FILENAME, 'rb')}
    response = requests.post("http://localhost:8000/transcribe", files=files)
    return response.json().get("transcript", "")

def get_next_question(session_id):
    response = requests.get("http://localhost:8000/interview/next", params={"session_id": session_id})
    data = response.json()
    if "question" in data:
        print(f"🗨️  Q{data['question_number']}: {data['question']}")
        return data["question"]
    else:
        print("✅ Interview complete.")
        return None

def play_tts(question):
    response = requests.get("http://localhost:8000/ask-question", params={"text": question})
    audio_path = response.json().get("audio_file", "output.mp3")
    print("🔊 Playing bot question...\n")
    sound = AudioSegment.from_file(audio_path)
    play(sound)

def submit_answer(session_id, question, answer):
    response = requests.post("http://localhost:8000/interview/answer", json={
        "session_id": session_id,
        "question": question,
        "answer": answer
    })
    if response.status_code == 200:
        data = response.json()
        print("✅ Answer submitted.\n")
        print(f"🧠 Evaluation: {data['evaluation']}\n")
    else:
        print("❌ Failed to submit answer:", response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session_id", required=True, help="Session ID from /interview/start")
    args = parser.parse_args()

    while True:
        question = get_next_question(args.session_id)
        if not question:
            break
        play_tts(question)
        record_audio()
        answer = transcribe_audio()
        print(f"🧑 Your Answer: {answer}\n")
        submit_answer(args.session_id, question, answer)
        input("⏭️  Press Enter for next question...\n")

    # After all questions are done
    print("📄 Generating final report...")
    end_response = requests.post("http://localhost:8000/interview/end", params={"session_id": args.session_id})
    
    if end_response.status_code == 200:
        report_path = end_response.json().get("report_path")
        print(f"✅ Interview complete. PDF report saved at: {report_path}\n")
    else:
        print("❌ Failed to generate final report:", end_response.json())
