\# 📄 RAG PDF Chatbot — Powered by Groq API



> Chat with any PDF document using AI! Upload a PDF and ask questions — get instant, accurate answers with source citations.



!\[RAG PDF Chatbot](screenshot3.png)



\---



\## 🚀 Live Demo

> Upload any PDF → Ask questions → Get answers in seconds!



\---



\## ✨ Features



\- 📤 Upload any PDF document

\- 🔍 Retrieval-Augmented Generation (RAG) pipeline

\- ⚡ Super fast answers using \*\*Groq API\*\* (LLaMA 3.3 70B)

\- 📚 Source citations shown for every answer

\- 🧠 Zero hallucination via grounded prompting

\- 💾 Vector search using \*\*ChromaDB\*\*



\---



\## 🛠️ Tech Stack



| Layer | Technology |

|---|---|

| LLM | Groq API (llama-3.3-70b-versatile) |

| Framework | LangChain |

| Vector Database | ChromaDB |

| Embeddings | HuggingFace (all-MiniLM-L6-v2) |

| PDF Parsing | PyPDFLoader |

| UI | Streamlit |

| Language | Python 3.9+ |



\---



\## 📸 Screenshots



\### 1. Upload PDF

!\[Upload](screenshot1.png)



\### 2. PDF Processed

!\[Processed](screenshot2.png)



\### 3. Ask Questions \& Get Answers

!\[Answer](screenshot3.png)



\---



\## ⚙️ How to Run Locally



\### 1. Clone the repository

```bash

git clone https://github.com/Palakbiradar119/RAG-PDF-Chatbot.git

cd RAG-PDF-Chatbot

```



\### 2. Create virtual environment

```bash

python -m venv venv

venv\\Scripts\\activate

```



\### 3. Install dependencies

```bash

pip install -r requirements.txt

```



\### 4. Set up your API key

Create a `.env` file in the project root:

