import re

def run(resume_text):
    """
    Parses raw resume text and extracts key information.
    """

    # Extract Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    email = email_match.group(0) if email_match else "Not found"

    # Extract Phone
    phone_match = re.search(r'(\+91[\-\s]?)?[6-9]\d{9}', resume_text)
    phone = phone_match.group(0) if phone_match else "Not found"

    # Extract Name (first non-empty line assumed to be name)
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    name = lines[0] if lines else "Not found"

    # Extract Skills (basic keyword matching)
    skills_keywords = [
        "Python", "Java", "SQL", "Machine Learning", "Deep Learning",
        "NLP", "React", "Node.js", "JavaScript", "C++", "Data Analysis",
        "Excel", "Power BI", "Tableau", "AWS", "Docker", "Git"
    ]
    found_skills = [skill for skill in skills_keywords if skill.lower() in resume_text.lower()]

    # Extract Education keywords
    education_keywords = ["B.Tech", "M.Tech", "MBA", "B.Sc", "M.Sc", "PhD", "Bachelor", "Master", "Diploma"]
    found_education = [edu for edu in education_keywords if edu.lower() in resume_text.lower()]

    # Extract Experience (look for year patterns)
    experience_matches = re.findall(r'\b(19|20)\d{2}\b', resume_text)
    years_mentioned = list(set(experience_matches))

    parsed_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills,
        "education": found_education,
        "years_mentioned": sorted(years_mentioned),
        "raw_text": resume_text
    }

    return parsed_data