def evaluate_answer(question: str, answer: str, role: str) -> dict:
    prompt = f"""
You are an experienced interviewer conducting a {role.upper()} interview.

Evaluate the following answer given by a candidate.

Question:
"{question}"

Candidate's Answer:
"{answer}"

Now evaluate the answer in 3-4 sentences. Be specific. If it's a technical role, focus on correctness and clarity. If it's HR, focus on communication and intent.
Also give a score out of 10 (as a float) in this format:

EVALUATION: <Your evaluation here>
SCORE: <score here>
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 400,
            }
        )

        # Check for valid response
        candidate = response.candidates[0] if response.candidates else None
        if not candidate or candidate.finish_reason != 0 or not candidate.content.parts:
            return {
                "evaluation": f"Evaluation skipped: Gemini filtered or rejected the input.",
                "score": 0.0
            }

        # Parse response text
        text = candidate.content.parts[0].text.strip()
        print("🔍 Gemini Response:", text)

        # Extract EVALUATION and SCORE
        lines = text.splitlines()
        evaluation = ""
        score = None
        for line in lines:
            if line.startswith("EVALUATION:"):
                evaluation = line.replace("EVALUATION:", "").strip()
            elif line.startswith("SCORE:"):
                try:
                    score = float(line.replace("SCORE:", "").strip())
                except ValueError:
                    score = None

        return {
            "evaluation": evaluation or "No evaluation extracted.",
            "score": score if score is not None else 0.0
        }

    except Exception as e:
        return {
            "evaluation": f"Evaluation error: {str(e)}",
            "score": 0.0
        }
