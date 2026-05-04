import streamlit as st
import tempfile
import os
import re
import pandas as pd
from collections import OrderedDict
from rag_engine import ingest_pdf, query_pdf

st.set_page_config(page_title="AI Hiring Assistant", layout="wide")

st.markdown("""
# 🧠 AI Hiring Assistant
### Analyze resumes, compare candidates, and hire smarter
""")

# ---------------------------
# SESSION STATE
# ---------------------------
if "pdf_ready" not in st.session_state:
    st.session_state["pdf_ready"] = False

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "last_sources" not in st.session_state:
    st.session_state["last_sources"] = []

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Model: LLaMA 3 (Groq)")
    st.write("Retriever: MMR")
    st.write("Chunk size: 800")

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_files = st.file_uploader(
    "Upload Resumes / Job Descriptions",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------------------
# PROCESS PDFs
# ---------------------------
if uploaded_files:
    if st.button("🚀 Process Documents"):
        with st.spinner("Processing..."):
            paths = []

            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    paths.append((tmp.name, file.name))  # store original name

            chunks = ingest_pdf(paths)

            for path, _ in paths:
                os.unlink(path)

            st.success(f"✅ {len(uploaded_files)} files processed | {chunks} chunks")
            st.session_state["pdf_ready"] = True

# ---------------------------
# MAIN DASHBOARD
# ---------------------------
if st.session_state["pdf_ready"]:

    col1, col2 = st.columns([1, 2])

    # LEFT PANEL
    with col1:
        st.subheader("📂 Uploaded Files")
        if uploaded_files:
            for file in uploaded_files:
                st.write(f"📄 {file.name}")

        st.markdown("### 💡 Try these:")
        st.markdown("""
        - Who is the best candidate?
        - Compare all candidates
        - Which candidate matches job best?
        """)

    # RIGHT PANEL
    with col2:
        st.subheader("💬 Ask Questions")

        question = st.text_input("Type your question")

        if st.button("Get Answer"):
            if question.strip() == "":
                st.warning("Enter a question")
            else:
                try:
                    with st.spinner("Analyzing..."):
                        answer, sources = query_pdf(question)

                    st.session_state.chat_history.append(("You", question))
                    st.session_state.chat_history.append(("Bot", answer))
                    st.session_state["last_sources"] = sources

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # ---------------------------
    # CHAT HISTORY
    # ---------------------------
    st.markdown("## 💬 Chat History")

    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")

    # ---------------------------
    # SCORE VISUALIZATION (FIXED)
    # ---------------------------
    if st.session_state.chat_history:
        last_answer = st.session_state.chat_history[-1][1]

        scores = re.findall(r"(\d+)/10", last_answer)

        if scores:
            st.markdown("## 🏆 Candidate Analysis")

            scores_int = [int(s) for s in scores]

            # remove duplicate filenames
            unique_names = list(OrderedDict.fromkeys(
                [doc.metadata.get("source", "Unknown") for doc in st.session_state["last_sources"]]
            ))

            names = unique_names[:len(scores_int)]

            # progress bars
            for i, score in enumerate(scores_int):
                st.write(names[i])
                st.progress(score / 10)
                st.write(f"Score: {score}/10")

            # chart
            df = pd.DataFrame({
                "Candidate": names,
                "Score": scores_int
            })

            st.markdown("## 📊 Comparison Chart")
            st.bar_chart(df.set_index("Candidate"))

            # best candidate
            best_score = max(scores_int)
            best_index = scores_int.index(best_score)

            st.success(f"🏆 Best Candidate: {names[best_index]} ({best_score}/10)")

    # ---------------------------
    # DOWNLOAD REPORT
    # ---------------------------
    if st.session_state.chat_history:
        last_answer = st.session_state.chat_history[-1][1]

        st.download_button(
            "📥 Download Report",
            data=last_answer,
            file_name="hiring_report.txt"
        )

    # ---------------------------
    # SOURCE DOCUMENTS
    # ---------------------------
    if st.session_state["last_sources"]:
        with st.expander("📚 Source Documents"):
            for doc in st.session_state["last_sources"]:
                st.write(f"📄 {doc.metadata.get('source')}")
                st.write(doc.page_content[:200] + "...")
                st.divider()