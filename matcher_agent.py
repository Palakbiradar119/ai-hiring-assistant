from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def run(parsed_resume, job_description):
    """
    Matches parsed resume against job description and returns a match score.
    """

    # Combine resume fields into one text block
    resume_skills = ", ".join(parsed_resume.get("skills", []))
    resume_education = ", ".join(parsed_resume.get("education", []))
    resume_raw = parsed_resume.get("raw_text", "")

    combined_resume_text = f"{resume_raw} {resume_skills} {resume_education}"

    # Handle empty inputs
    if not combined_resume_text.strip() or not job_description.strip():
        return {
            "match_score": 0,
            "match_percentage": "0%",
            "matched_skills": [],
            "missing_skills": [],
            "verdict": "Insufficient data to match"
        }

    # TF-IDF Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([combined_resume_text, job_description])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    match_percentage = round(score * 100, 2)

    # Skill matching
    jd_words = set(job_description.lower().split())
    resume_skills_list = [s.lower() for s in parsed_resume.get("skills", [])]
    matched_skills = [s for s in resume_skills_list if s in jd_words]
    missing_skills = [s for s in resume_skills_list if s not in jd_words]

    # Verdict
    if match_percentage >= 70:
        verdict = "Strong Match ✅"
    elif match_percentage >= 40:
        verdict = "Moderate Match ⚠️"
    else:
        verdict = "Weak Match ❌"

    return {
        "match_score": round(score, 4),
        "match_percentage": f"{match_percentage}%",
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "verdict": verdict
    }