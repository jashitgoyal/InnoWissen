from vertexai.preview.generative_models import GenerativeModel
import vertexai
import os
from dotenv import load_dotenv

load_dotenv()

vertexai.init(
    project=os.getenv("GCP_PROJECT_ID"),
    location=os.getenv("GCP_REGION")
)

def generate_questions(interview_type: str, role: str = "Software Engineer", count: int = 5):
    prompt = f"""
    You are an expert interviewer. Generate {count} concise, verbal interview questions for a {interview_type} interview for the role of {role}.
    Return the questions as a numbered list.
    """

    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    lines = response.text.strip().split("\n")
    questions = [line.split('.', 1)[-1].strip() for line in lines if '.' in line]
    return questions
