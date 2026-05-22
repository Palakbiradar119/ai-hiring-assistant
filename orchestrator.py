from parser_agent import run as parser_run
from matcher_agent import run as matcher_run
from interview_agent import run as interview_run
from hr_agent import run as hr_run

from pdf_utils import extract_text_from_pdf


def run_pipeline(pdf_bytes, filename, job_description):

    # STEP 1
    resume_text = extract_text_from_pdf(pdf_bytes)

    # STEP 2
    parsed_resume = parser_run(resume_text)

    # STEP 3
    match_result = matcher_run(
        parsed_resume,
        job_description
    )

    # STEP 4
    interview_questions = interview_run(
        parsed_resume,
        match_result,
        job_description
    )

    # STEP 5
    hr_result = hr_run(
        parsed_resume,
        match_result,
        interview_questions
    )

    return {

        "candidate_name":
        parsed_resume.get("name", filename),

        "overall_score":
        match_result.get("score", 0),

        "hire_decision":
        hr_result.get("hire_decision", "NO"),

        "recommendation":
        hr_result.get("reasoning", ""),

        "parsed_resume":
        parsed_resume,

        "match_result":
        match_result,

        "interview_questions":
        interview_questions,

        "hr_result":
        hr_result
    }