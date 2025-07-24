import os
import json
from datetime import datetime

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

def log_answer(session_id: str, question: str, answer: str, evaluation: str, score: float = None):
    log_path = os.path.join(LOG_DIR, f"{session_id}.json")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "evaluation": evaluation,
        "score": score
    }

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)
