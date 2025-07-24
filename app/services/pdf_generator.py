import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

LOG_DIR = "logs"
PDF_DIR = "reports"

os.makedirs(PDF_DIR, exist_ok=True)

def generate_pdf_report(session_id: str):
    log_path = os.path.join(LOG_DIR, f"{session_id}.json")
    pdf_path = os.path.join(PDF_DIR, f"{session_id}.pdf")

    if not os.path.exists(log_path):
        raise FileNotFoundError("Log file not found for this session")

    with open(log_path, "r") as f:
        data = json.load(f)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, f"Interview Report: {session_id}")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    total_score = 0
    for i, entry in enumerate(data, 1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"Q{i}: {entry['question']}")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"🗣️ Answer: {entry['answer']}")
        y -= 20

        c.drawString(50, y, f"🧠 Evaluation: {entry['evaluation']}")
        y -= 20

        score = entry.get("score", "N/A")
        if isinstance(score, (int, float)):
            total_score += score
        c.drawString(50, y, f"🎯 Score: {score}")
        y -= 30

        if y < 100:
            c.showPage()
            y = height - 50

    avg_score = round(total_score / len(data), 2) if data else "N/A"

    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, f"✅ Final Score: {avg_score}")
    y -= 20

    c.save()
    return pdf_path
