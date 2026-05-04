import os
import shutil
from dotenv import load_dotenv
load_dotenv()

from collections import defaultdict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# ---------------------------
# CONFIG
# ---------------------------
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------
# EMBEDDINGS
# ---------------------------
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# ---------------------------
# LLM
# ---------------------------
def get_llm():
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

# ---------------------------
# INGEST PDF
# ---------------------------
def ingest_pdf(pdf_paths: list):
    documents = []

    for path, original_name in pdf_paths:
        loader = PyPDFLoader(path)
        docs = loader.load()

        for doc in docs:
            # ✅ Keep original filename
            doc.metadata["source"] = original_name

            # ✅ Detect file type
            name = original_name.lower()
            if "resume" in name or "cv" in name:
                doc.metadata["type"] = "resume"
            elif "job" in name or "jd" in name or "description" in name:
                doc.metadata["type"] = "job_description"
            else:
                doc.metadata["type"] = "unknown"

        documents.extend(docs)

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(documents)

    embeddings = get_embeddings()

    # Clear old DB
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create vector DB
    vectorstore = Chroma.from_documents(
        split_docs,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    vectorstore.persist()

    return len(split_docs)

# ---------------------------
# QUERY PDF (STRICT VERSION)
# ---------------------------
def query_pdf(query):
    embeddings = get_embeddings()

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    # ✅ Better retrieval
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 20}
    )

    docs = retriever.get_relevant_documents(query)

    if not docs:
        return "No relevant information found.", []

    # ---------------------------
    # GROUP DOCUMENTS
    # ---------------------------
    grouped_docs = defaultdict(list)

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        doc_type = doc.metadata.get("type", "unknown")
        grouped_docs[(source, doc_type)].append(doc.page_content)

    # ---------------------------
    # BUILD CONTEXT
    # ---------------------------
    resume_context = ""
    jd_context = ""

    for (source, doc_type), contents in grouped_docs.items():
        combined = "\n".join(contents[:3])  # limit chunks

        if doc_type == "resume":
            resume_context += f"\nRESUME: {source}\n{combined}\n"
        elif doc_type == "job_description":
            jd_context += f"\nJOB DESCRIPTION: {source}\n{combined}\n"
        else:
            resume_context += f"\nDOCUMENT: {source}\n{combined}\n"

    # ---------------------------
    # 🔥 STRICT PROMPT
    # ---------------------------
    prompt = f"""
You are an expert AI Hiring Assistant.

STRICT RULES:
- Do NOT guess
- Use ONLY given context
- Each RESUME = one candidate
- Be very strict like a real recruiter

SCORING RULES (VERY STRICT):

- 0/10 → No relevant skills
- 1–3/10 → Weak / unrelated background
- 4–6/10 → Partial match
- 7–8/10 → Good match
- 9–10/10 → Excellent match

IMPORTANT:
- If candidate has ZERO Gen AI / LLM / Python / AI skills → MUST give 0/10
- Do NOT give sympathy scores

TASKS:
1. Extract:
   - Name
   - Skills
   - Education

2. If job description exists:
   - Match candidates to job
   - Give score

3. Rank candidates

OUTPUT FORMAT:

CANDIDATES:

Candidate 1:
- Name:
- Skills:
- Education:
- Score: X/10

Candidate 2:
...

FINAL:
Best Candidate:
Reason:

--------------------------------

JOB DESCRIPTION:
{jd_context}

RESUMES:
{resume_context}

Question:
{query}

Answer:
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return str(response.content), docs