import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

load_dotenv()

CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def store_agent_results_in_chroma(agent_results):

    documents = []

    for r in agent_results:

        content = f"""
Candidate: {r.get('candidate_name')}
Score: {r.get('overall_score')}
Decision: {r.get('hire_decision')}
Matched Skills: {', '.join(r.get('matched_skills', []))}
Missing Skills: {', '.join(r.get('missing_skills', []))}
Reasoning: {r.get('reasoning')}
"""

        doc = Document(
            page_content=content,
            metadata={
                "candidate": r.get("candidate_name"),
                "score": r.get("overall_score")
            }
        )

        documents.append(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    split_docs = splitter.split_documents(documents)

    embeddings = get_embeddings()

    if os.path.exists(CHROMA_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )

        vectorstore.add_documents(split_docs)

    else:
        vectorstore = Chroma.from_documents(
            split_docs,
            embedding=embeddings,
            persist_directory=CHROMA_PATH
        )

    vectorstore.persist()