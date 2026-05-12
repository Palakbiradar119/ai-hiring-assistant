# 🚀 AI Hiring Assistant Pro

An enterprise-style AI-powered hiring platform that automates resume screening, candidate ranking, job description matching, and interview preparation using Generative AI, RAG pipelines, and LLM-powered workflows.

---

# 📌 Problem Statement

Recruiters often spend hours manually reviewing resumes and shortlisting candidates. Traditional ATS systems fail to understand contextual skills and candidate-job fit effectively.

AI Hiring Assistant Pro solves this problem using Retrieval-Augmented Generation (RAG), semantic resume analysis, and LLM-powered candidate evaluation.

---

# ✨ Features

✅ Bulk Resume Upload
✅ AI Resume Screening
✅ Candidate Ranking System
✅ Job Description Matching
✅ Resume Parsing & Skill Extraction
✅ ATS-style Filtering
✅ AI Hiring Recommendations
✅ HR Chatbot Assistant
✅ AI Interview Question Generator
✅ CSV Export Support
✅ Recruiter-Friendly Dashboard

---

# 🧠 System Workflow

1️⃣ Upload candidate resumes in PDF format
2️⃣ Extract and process resume text
3️⃣ Generate embeddings using HuggingFace models
4️⃣ Store embeddings inside ChromaDB vector database
5️⃣ Compare resumes against Job Description
6️⃣ Rank candidates based on semantic matching
7️⃣ Generate hiring recommendations and interview questions

---

# 🏗️ Architecture

Recruiter → Upload Resumes → Resume Parser → Embedding Generation → ChromaDB Vector Store → Gemini/Groq LLM → Candidate Ranking & AI Insights

---

# 🛠️ Tech Stack

| Category        | Technology            |
| --------------- | --------------------- |
| Language        | Python                |
| Frontend        | Streamlit             |
| AI Framework    | LangChain             |
| LLM             | Gemini API / Groq API |
| Vector Database | ChromaDB              |
| Embeddings      | HuggingFace           |
| Data Processing | Pandas                |
| PDF Parsing     | PyPDFLoader           |
| Deployment      | Streamlit Cloud       |

---

# 📂 Project Structure

```bash
ai-hiring-assistant/
│
├── app.py
├── rag_engine.py
├── screener.py
├── requirements.txt
├── README.md
├── images/
```

---

# 📸 Screenshots

## Dashboard

(Add screenshot here)

## Resume Ranking

(Add screenshot here)

## HR Chatbot

(Add screenshot here)

## Interview Generator

(Add screenshot here)

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Palakbiradar119/ai-hiring-assistant.git

cd ai-hiring-assistant
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv

venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

OR

```env
GROQ_API_KEY=your_api_key
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 🌐 Live Demo

https://ai-hiring-assistant-jiklsdrqhpf3cwghnnr9xm.streamlit.app/

---

# 🔥 Key Highlights

* Enterprise-style AI hiring workflow
* Real-world ATS-inspired candidate ranking
* RAG-powered semantic resume understanding
* AI-generated hiring recommendations
* Streamlit deployment with live demo
* Modular and scalable architecture

---

# 🚀 Future Improvements

* Multi-Agent Hiring Workflow
* AI Voice Interview System
* Recruiter Authentication
* Email Automation
* SQL Candidate Database
* Advanced ATS Scoring
* Docker Deployment
* FastAPI Backend Integration

---

# 👨‍💻 Author

Pratiksha Biradar
Gen AI Developer | Data Scientist | AI Engineer

GitHub: https://github.com/Palakbiradar119

---

# ⭐ Support

If you like this project, give it a star ⭐
