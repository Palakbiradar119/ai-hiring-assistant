from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def run(parsed_resume, match_result, interview_questions):
    """
    Generates a final HR report and hiring recommendation.
    """

    name = parsed_resume.get("name", "Candidate")
    email = parsed_resume.get("email", "N/A")
    phone = parsed_resume.get("phone", "N/A")
    skills = ", ".join(parsed_resume.get("skills", []))
    education = ", ".join(parsed_resume.get("education", []))

    match_percentage = match_result.get("match_percentage", "N/A")
    verdict = match_result.get("verdict", "N/A")
    matched_skills = ", ".join(match_result.get("matched_skills", []))
    missing_skills = ", ".join(match_result.get("missing_skills", []))

    questions = interview_questions.get("questions", [])
    questions_text = "\n".join(questions) if questions else "No questions generated"

    prompt = (
        "You are a senior HR manager. Based on the complete candidate evaluation below, "
        "write a professional HR report and give a final hiring recommendation.\n\n"
        "=== CANDIDATE PROFILE ===\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Skills: {skills}\n"
        f"Education: {education}\n\n"
        "=== MATCH ANALYSIS ===\n"
        f"Match Score: {match_percentage}\n"
        f"Verdict: {verdict}\n"
        f"Matched Skills: {matched_skills}\n"
        f"Skills Gap: {missing_skills}\n\n"
        "=== INTERVIEW QUESTIONS PREPARED ===\n"
        f"{questions_text}\n\n"
        "Please provide:\n"
        "1. A brief candidate summary (2-3 lines)\n"
        "2. Key strengths\n"
        "3. Areas of concern\n"
        "4. Final hiring recommendation (Hire / Hold / Reject)\n"
        "5. Suggested next steps\n\n"
        "Be professional, concise and unbiased."
    )

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.choices[0].message.content

    recommendation = "Hold"
    if "hire" in response_text.lower():
        recommendation = "Hire"
    elif "reject" in response_text.lower():
        recommendation = "Reject"
    else:
        recommendation = "Hold"

    return {
        "candidate_name": name,
        "candidate_email": email,
        "candidate_phone": phone,
        "match_percentage": match_percentage,
        "verdict": verdict,
        "recommendation": recommendation,
        "full_report": response_text
    }