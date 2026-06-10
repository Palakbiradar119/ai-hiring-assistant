# 🧑‍💼 AI Hiring Assistant Pro

> Enterprise-style AI hiring platform that automates resume screening, JD matching, candidate ranking, and interview generation — replacing hours of manual HR work with a semantic RAG pipeline.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://ai-hiring-assistant-jiklsdrqhpf3cwghnnr9xm.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)

---

## The problem this solves

Manual resume screening for a single role takes 4–8 hours. A recruiter reads 100+ resumes, matches them to the JD, ranks candidates, generates interview questions — all manually. This platform automates the entire pipeline using RAG and LLMs.

```
Job Description (text)
    │
    ▼
Gemini Embeddings ──► ChromaDB vector store
                              │
Resume Pool (PDF/text)        │
    │                         │
    ▼                         ▼
Gemini Embeddings ──► Semantic similarity search
                              │
                              ▼
                    ATS-style keyword filtering
                              │
                              ▼
                    Candidate ranking (score 0–100)
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
            HR Recommendations    Interview Question
            (hire/reject/maybe)   Generator (role-specific)
                    │
                    ▼
            HR Chatbot (Q&A about
            any candidate or role)
```

---

## Features

| Feature | What it does |
|---------|-------------|
| JD–Resume matching | Semantic similarity using Gemini embeddings + ChromaDB |
| ATS filtering | Keyword extraction from JD, hard-filter resumes missing critical skills |
| Candidate ranking | Composite score: semantic match + keyword coverage + experience signals |
| HR recommendations | LLM-generated: hire / reject / interview with reasoning |
| Interview generator | Role + candidate-specific technical and behavioral questions |
| HR chatbot | Ask any question about shortlisted candidates |

---

## Architecture decisions

**Why RAG for resume matching?**
Keyword matching misses synonyms ("developed" vs "built", "NLP" vs "natural language processing"). Semantic embedding captures meaning, not just words — a resume mentioning "built LLM pipelines" correctly matches a JD asking for "LangChain experience".

**ChromaDB as the vector store**
Lightweight, runs in-process (no separate server), persists to disk. Right choice for a single-node application where Pinecone's overhead isn't justified.

---

## Run locally

```bash
git clone https://github.com/pratikshabiradar19/ai-hiring-assistant.git
cd ai-hiring-assistant

pip install -r requirements.txt

# Add GOOGLE_API_KEY to .env
streamlit run app.py
```

---

## Tech stack

`LangChain` `RAG Pipelines` `ChromaDB` `Gemini API` `Google Generative AI Embeddings` `Python` `Streamlit`

---

*Built by [Pratiksha Biradar](https://github.com/pratikshabiradar19) — Gen AI Engineer*
