# 🎯 Interview AI

> AI-powered mock interview platform that generates role-specific questions from your resume, evaluates your answers in real time, and gives detailed performance feedback with scoring.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://interview-ai-94l7saq9fzil5gs3yon8ja.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)

---

## How it works

```
Your Resume + Target Role
        │
        ▼
LLM extracts: skills, experience, projects, seniority level
        │
        ▼
Question Generator
├── Technical questions (based on your specific stack)
├── Behavioral questions (STAR format, role-appropriate)
└── Project deep-dives (questions about YOUR projects)
        │
        ▼
You type your answer
        │
        ▼
LLM Evaluator scores each answer:
├── Technical accuracy (0–10)
├── Clarity and structure (0–10)
├── Depth and specificity (0–10)
└── Feedback: what was good, what was missing
        │
        ▼
Final performance report
├── Overall score
├── Strongest areas
├── Skill gaps exposed
└── Recommended study topics
```

---

## What makes the questions good

Questions are generated from **your actual resume**, not generic templates. If your resume mentions "LangGraph state graphs", the interviewer asks you about LangGraph — not a generic "tell me about a framework you've used." This makes practice directly relevant to your actual interviews.

---

## Run locally

```bash
git clone https://github.com/pratikshabiradar19/interview-ai.git
cd interview-ai

pip install -r requirements.txt

# Add GROQ_API_KEY to .env
streamlit run app.py
```

---

## Tech stack

`Groq API` `LangChain` `LLaMA 3.3 70B` `Python` `Streamlit`

---

*Built by [Pratiksha Biradar](https://github.com/pratikshabiradar19) — Gen AI Engineer*
