from vertexai.preview.generative_models import GenerativeModel
import vertexai
import os
import random
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



def evaluate_answer(question: str, answer: str, role: str) -> str:
    prompt = f"""
You are evaluating a candidate's response during a {role} interview.

Question: "{question}"
Answer: "{answer}"

Evaluate the answer in 3-4 lines. Focus on what matters most for a {role} interview. Be specific about content, clarity, and how well it aligns with expectations.
"""
    response = model.predict(prompt=prompt, temperature=0.3, max_output_tokens=200)
    return response.text.strip()