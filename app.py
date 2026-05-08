import streamlit as st
import pandas as pd
import plotly.express as px
from screener import screen_multiple_resumes, generate_interview_questions
import os
from groq import Groq
from dotenv import load_dotenv
import pdfplumber

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="AI Hiring Assistant Pro",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Hiring Assistant Pro")
st.markdown("**Complete AI powered recruitment platform — screen, rank, and interview candidates automatically.**")

tab1, tab2, tab3 = st.tabs([
    "📋 Resume Screener & Ranker",
    "💬 HR Chatbot",
    "❓ Interview Question Generator"
])

# ============================================================
# TAB 1 — RESUME SCREENER AND RANKER
# ============================================================
with tab1:
    st.header("📋 Bulk Resume Screener & Ranker")
    st.markdown("Upload multiple resumes and paste the job description — AI screens and ranks all candidates.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1️⃣ Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload resume PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            key="screener_files"
        )
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} resume(s) uploaded")
            for f in uploaded_files:
                st.caption(f"📄 {f.name}")

    with col2:
        st.subheader("2️⃣ Paste Job Description")
        job_description = st.text_area(
            "Paste the complete job description here:",
            height=200,
            placeholder="e.g. We are looking for a Python Developer with 2+ years experience..."
        )

    st.divider()

    if st.button("🚀 Screen & Rank All Candidates", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one resume!")
        elif not job_description.strip():
            st.error("Please paste the job description!")
        else:
            with st.spinner(f"Screening {len(uploaded_files)} resume(s)..."):
                results = screen_multiple_resumes(uploaded_files, job_description)
            st.session_state.screening_results = results
            st.success(f"✅ Done! {len(results)} candidates evaluated.")

    if "screening_results" in st.session_state and st.session_state.screening_results:
        results = st.session_state.screening_results
        valid = [r for r in results if "overall_score" in r]

        if valid:
            st.subheader("🏆 Candidate Rankings")

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Candidates", len(valid))
            with m2:
                recommended = len([r for r in valid if "Recommended" in r.get("recommendation", "")])
                st.metric("Recommended", recommended)
            with m3:
                avg_score = sum(r["overall_score"] for r in valid) / len(valid)
                st.metric("Average Score", f"{avg_score:.0f}/100")
            with m4:
                st.metric("Top Score", f"{valid[0]['overall_score']}/100")

            if len(valid) > 1:
                chart_data = pd.DataFrame({
                    "Candidate": [r.get("candidate_name", r["filename"]) for r in valid],
                    "Score": [r["overall_score"] for r in valid]
                })
                fig = px.bar(
                    chart_data,
                    x="Candidate",
                    y="Score",
                    color="Score",
                    color_continuous_scale="RdYlGn",
                    title="Candidate Score Comparison",
                    range_y=[0, 100]
                )
                st.plotly_chart(fig, use_container_width=True)

            table_data = []
            for r in valid:
                rec = r.get("recommendation", "")
                badge = ("🟢 " if "Strongly" in rec else "🟡 " if "Recommended" in rec else "🟠 " if "Maybe" in rec else "🔴 ") + rec
                table_data.append({
                    "Rank": f"#{r['rank']}",
                    "Candidate": r.get("candidate_name", "Unknown"),
                    "Score": f"{r['overall_score']}/100",
                    "Experience": r.get("experience_match", "N/A"),
                    "Education": r.get("education_match", "N/A"),
                    "Recommendation": badge,
                })

            st.dataframe(pd.DataFrame(table_data), use_container_width=True)

            csv = pd.DataFrame(table_data).to_csv(index=False)
            st.download_button("⬇️ Download Rankings CSV", csv, "rankings.csv", "text/csv")

            st.divider()
            st.subheader("📊 Detailed Candidate Analysis")

            for r in valid:
                score = r["overall_score"]
                icon = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"

                with st.expander(f"{icon} #{r['rank']} {r.get('candidate_name','Unknown')} — {score}/100 — {r.get('recommendation','')}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**✅ Matching Skills:**")
                        for skill in r.get("skills_match", []):
                            st.markdown(f"- {skill}")
                    with c2:
                        st.markdown("**❌ Skills Gap:**")
                        gaps = r.get("skills_gap", [])
                        if gaps:
                            for gap in gaps:
                                st.markdown(f"- {gap}")
                        else:
                            st.markdown("- No major gaps found")

                    st.markdown("**📝 AI Summary:**")
                    st.info(r.get("summary", ""))

                    st.markdown("**❓ Suggested Interview Questions:**")
                    for i, q in enumerate(r.get("interview_questions", []), 1):
                        st.markdown(f"{i}. {q}")

# ============================================================
# TAB 2 — HR CHATBOT
# ============================================================
with tab2:
    st.header("💬 HR Assistant Chatbot")
    st.markdown("Ask anything about hiring, candidates, HR policies, or interview tips.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask me anything about hiring...")

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                messages = [
                    {
                        "role": "system",
                        "content": """You are an expert HR assistant and talent acquisition specialist.
You help with resume evaluation, interview tips, HR policies, job descriptions,
salary benchmarking, and candidate comparison.
Be concise, professional and helpful."""
                    }
                ]
                for msg in st.session_state.chat_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800
                )
                reply = response.choices[0].message.content

            st.write(reply)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": reply
            })

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================
# TAB 3 — INTERVIEW QUESTION GENERATOR
# ============================================================
with tab3:
    st.header("❓ Interview Question Generator")
    st.markdown("Upload a resume and paste the job description — get 8 custom interview questions instantly.")

    col1, col2 = st.columns([1, 1])
    with col1:
        resume_file = st.file_uploader(
            "Upload candidate resume PDF",
            type=["pdf"],
            key="interview_resume"
        )
    with col2:
        jd_for_interview = st.text_area(
            "Paste job description:",
            height=150,
            key="interview_jd"
        )

    candidate_name = st.text_input(
        "Candidate name (optional):",
        placeholder="e.g. Rahul Verma"
    )

    if st.button("🎯 Generate Interview Questions", type="primary"):
        if not resume_file:
            st.error("Please upload a resume!")
        elif not jd_for_interview.strip():
            st.error("Please paste the job description!")
        else:
            with st.spinner("Generating questions..."):
                with pdfplumber.open(resume_file) as pdf:
                    resume_text = ""
                    for page in pdf.pages:
                        resume_text += page.extract_text() or ""
                name = candidate_name if candidate_name else "Candidate"
                questions, error = generate_interview_questions(
                    resume_text, jd_for_interview, name
                )

            if error:
                st.error(f"Error: {error}")
            elif questions:
                st.subheader(f"Interview Questions for {name}")
                type_colors = {
                    "Technical": "🔵",
                    "Behavioral": "🟢",
                    "Situational": "🟡",
                    "Gap Analysis": "🔴",
                    "Motivation": "🟣"
                }
                for i, q in enumerate(questions, 1):
                    q_type = q.get("type", "General")
                    icon = type_colors.get(q_type, "⚪")
                    with st.expander(f"{icon} Question {i} — {q_type}"):
                        st.markdown(f"**{q.get('question', '')}**")

                q_text = "\n\n".join([
                    f"Q{i} ({q.get('type','General')}): {q.get('question','')}"
                    for i, q in enumerate(questions, 1)
                ])
                st.download_button(
                    "⬇️ Download Questions",
                    q_text,
                    f"questions_{name}.txt",
                    "text/plain"
                )
