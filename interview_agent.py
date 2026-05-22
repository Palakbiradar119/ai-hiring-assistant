from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def run(parsed_resume, match_result, job_description):
    """
    Generates personalized interview questions based on resume and job description.
    """

    name = parsed_resume.get("name", "Candidate")
    skills = ", ".join(parsed_resume.get("skills", []))
    education = ", ".join(parsed_resume.get("education", []))
    match_percentage = match_result.get("match_percentage", "N/A")
    matched_skills = ", ".join(match_result.get("matched_skills", []))
    missing_skills = ", ".join(match_result.get("missing_skills", []))

    prompt = (
        "You are an expert technical interviewer. "
        "Based on the following candidate profile and job description, "
        "generate 10 relevant interview questions.\n\n"
        f"Candidate Name: {name}\n"
        f"Skills: {skills}\n"
        f"Education: {education}\n"
        f"Match Score: {match_percentage}\n"
        f"Matched Skills: {matched_skills}\n"
        f"Skills Gap: {missing_skills}\n\n"
        f"Job Description:\n{job_description}\n\n"
        "Generate:\n"
        "- 4 Technical questions based on their skills\n"
        "- 3 Behavioral questions\n"
        "- 2 Questions targeting their skill gaps\n"
        "- 1 Culture fit question\n\n"
        "Format each question with a number and category label like:\n"
        "1. [Technical] ...\n"
        "2. [Behavioral] ...\n"
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

    lines = response_text.strip().split("\n")
    questions = [line.strip() for line in lines if line.strip() and line[0].isdigit()]

    return {
        "candidate_name": name,
        "total_questions": len(questions),
        "questions": questions,
        "raw_response": response_text
    }