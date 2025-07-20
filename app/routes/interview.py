from fastapi import APIRouter,UploadFile, File
from app.services import tts
from app.services import stt

router = APIRouter()

@router.get("/ask-question")
def ask_question(text: str = "Tell me about yourself"):
    audio_path = tts.text_to_speech(text)
    return {"message": "Success", "audio_file": audio_path}



@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.wav", "wb") as f:
        f.write(contents)

    transcript = stt.transcribe_audio("temp.wav")
    return {"transcript": transcript}
