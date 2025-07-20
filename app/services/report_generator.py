from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_interview_report(session_id: str, interview_type: str, evaluations: list, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{session_id}_report.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 40
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Interview Report: {session_id}")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Interview Type: {interview_type.upper()}")
    y -= 20
    c.drawString(50, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 40

    total_score = 0
    for i, item in enumerate(evaluations, 1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Q{i}: {item['question']}")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"A: {item['answer']}")
        y -= 20

        c.drawString(50, y, f"Evaluation: {item['evaluation']}")
        y -= 20

        score = item.get("score", -1)
        if score >= 0:
            total_score += score
        c.drawString(50, y, f"Score: {score}/10")
        y -= 30

        if y < 100:  # Start new page if running low
            c.showPage()
            y = height - 40

    avg_score = total_score / len(evaluations) if evaluations else 0
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"\nAverage Score: {avg_score:.2f}/10")

    c.save()
    return filename
