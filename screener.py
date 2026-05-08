import pdfplumber
import os
from groq import Groq
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def screen_resume(resume_text, job_description):
    prompt = f"""
You are an expert HR recruiter and talent acquisition specialist.
Analyze this resume against the job description and provide evaluation.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide your evaluation in this EXACT JSON format only, no other text:
{{
    "candidate_name": "extract name from resume",
    "overall_score": <number 0-100>,
    "skills_match": ["skill1", "skill2", "skill3"],
    "skills_gap": ["missing_skill1", "missing_skill2"],
    "experience_match": "<Strong/Moderate/Weak>",
    "education_match": "<Strong/Moderate/Weak>",
    "recommendation": "<Strongly Recommended/Recommended/Maybe/Not Recommended>",
    "summary": "<2 sentence summary of candidate fit>",
    "interview_questions": [
        "Question 1 specific to this candidate",
        "Question 2 specific to this candidate",
        "Question 3 specific to this candidate",
        "Question 4 specific to this candidate",
        "Question 5 specific to this candidate"
    ]
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        result_text = response.choices[0].message.content.strip()
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(result_text)
        return result, None
    except json.JSONDecodeError:
        try:
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result, None
        except:
            pass
        return None, "Could not parse AI response"
    except Exception as e:
        return None, str(e)

def screen_multiple_resumes(pdf_files, job_description):
    results = []
    for pdf_file in pdf_files:
        resume_text = extract_text_from_pdf(pdf_file)
        if resume_text.startswith("Error"):
            results.append({
                "filename": pdf_file.name,
                "error": resume_text
            })
            continue
        result, error = screen_resume(resume_text, job_description)
        if error:
            results.append({
                "filename": pdf_file.name,
                "error": error
            })
        else:
            result["filename"] = pdf_file.name
            result["resume_text"] = resume_text
            results.append(result)

    valid_results = [r for r in results if "overall_score" in r]
    error_results = [r for r in results if "error" in r]
    valid_results.sort(key=lambda x: x["overall_score"], reverse=True)

    for i, r in enumerate(valid_results, 1):
        r["rank"] = i

    return valid_results + error_results

def generate_interview_questions(resume_text, job_description, candidate_name):
    prompt = f"""
You are an expert interviewer.
Generate 8 highly specific interview questions for this candidate.

CANDIDATE: {candidate_name}
JOB DESCRIPTION: {job_description}
RESUME: {resume_text}

Return ONLY a JSON array like this:
[
    {{"type": "Technical", "question": "..."}},
    {{"type": "Behavioral", "question": "..."}},
    {{"type": "Situational", "question": "..."}},
    {{"type": "Technical", "question": "..."}},
    {{"type": "Behavioral", "question": "..."}},
    {{"type": "Gap Analysis", "question": "..."}},
    {{"type": "Motivation", "question": "..."}},
    {{"type": "Technical", "question": "..."}}
]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000
        )
        result_text = response.choices[0].message.content.strip()
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        questions = json.loads(result_text)
        return questions, None
    except Exception as e:
        return None, str(e)
