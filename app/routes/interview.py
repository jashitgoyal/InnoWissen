from fastapi import APIRouter,UploadFile, File
from app.services import tts
from app.services import stt
from fastapi import Request
from app.services import question_gen

from pydantic import BaseModel
import uuid

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



# In-memory session store (replace later with DB)
session_store = {}
class InterviewStartRequest(BaseModel):
    type: str = "HR"
    role: str = "Software Engineer"

@router.post("/interview/start")
async def start_interview(req: InterviewStartRequest):
    interview_type = req.type
    role = req.role

    session_id = f"{interview_type.lower()}-{role.lower()}-{str(len(session_store) + 1)}"
    questions = question_gen.generate_questions(interview_type, role)

    session_store[session_id] = {
        "questions": questions,
        "current": 0,
        "answers": []
    }

    return {
        "session_id": session_id,
        "total_questions": len(questions),
        "interview_type": interview_type,
        "role": role,
        "message": "Interview started successfully"
    }


@router.get("/interview/next")
def next_question(session_id: str):
    session = session_store.get(session_id)
    if not session:
        return {"error": "Invalid session ID"}
    
    idx = session["current"]
    if idx >= len(session["questions"]):
        return {"message": "Interview complete"}

    question = session["questions"][idx]
    session["current"] += 1
    return {"question": question, "question_number": idx + 1}


class AnswerSubmission(BaseModel):
    session_id: str
    question: str
    answer: str

@router.post("/interview/answer")
async def submit_answer(payload: AnswerSubmission):
    session = session_store.get(payload.session_id)
    if not session:
        return {"error": "Invalid session ID"}

    session["answers"].append({
        "question": payload.question,
        "answer": payload.answer
    })

    return {
        "message": "Answer submitted successfully",
        "question": payload.question,
        "transcript": payload.answer
    }
