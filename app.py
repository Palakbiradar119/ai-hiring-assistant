import streamlit as st
import pandas as pd
import plotly.express as px
from pdf_utils import extract_text_from_pdf
from orchestrator import run_pipeline

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🤖 AI Hiring Assistant")
st.markdown("### Multi-Agent AI Recruitment Platform")
st.divider()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.header("⚡ AI Agents")
    st.success("✅ Parser Agent")
    st.success("✅ Matcher Agent")
    st.success("✅ Interview Agent")
    st.success("✅ HR Agent")
    st.divider()
    st.info("""
This platform uses multiple AI agents working together.

Workflow:
1. Resume Parsing
2. JD Matching
3. Interview Generation
4. HR Recommendation
""")

# ---------------------------------------------------
# MAIN TABS
# ---------------------------------------------------

tab1, tab2 = st.tabs(["📄 Resume Screening", "📊 Analytics"])

# ===================================================
# TAB 1
# ===================================================

with tab1:

    st.subheader("Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste Job Description Here",
        height=250
    )

    if st.button("🚀 Run Multi-Agent Pipeline", use_container_width=True):

        if not uploaded_files:
            st.error("Please upload at least one resume.")
            st.stop()

        if not job_description.strip():
            st.error("Please paste a job description.")
            st.stop()

        results = []
        progress_bar = st.progress(0)

        for idx, uploaded_file in enumerate(uploaded_files):

            st.divider()
            st.subheader(f"📄 Processing: {uploaded_file.name}")

            try:

                # -----------------------------------------
                # EXTRACT TEXT FROM PDF
                # -----------------------------------------

                resume_text = extract_text_from_pdf(uploaded_file)

                if not resume_text or resume_text.startswith("Error"):
                    st.error(f"Could not extract text: {resume_text}")
                    continue

                st.success(f"✅ Text extracted — {len(resume_text)} characters")

                # -----------------------------------------
                # RUN PIPELINE
                # -----------------------------------------

                with st.spinner(f"Running AI agents on {uploaded_file.name}..."):

                    result = run_pipeline(
                        pdf_bytes=resume_text,        # passing extracted text
                        filename=uploaded_file.name,
                        job_description=job_description
                    )

                # -----------------------------------------
                # SHOW RESULTS IMMEDIATELY
                # -----------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Match Score", result.get("match_result", {}).get("match_percentage", "N/A"))

                with col2:
                    st.metric("Verdict", result.get("match_result", {}).get("verdict", "N/A"))

                with col3:
                    st.metric("HR Decision", result.get("hr_result", {}).get("recommendation", "N/A"))

                with st.expander("📋 View Full Report"):

                    st.markdown("### 👤 Parsed Resume")
                    st.json(result.get("parsed_resume", {}))

                    st.markdown("### 🎯 Match Analysis")
                    st.json(result.get("match_result", {}))

                    st.markdown("### ❓ Interview Questions")
                    questions = result.get("interview_questions", {}).get("questions", [])
                    for q in questions:
                        st.markdown(f"- {q}")

                    st.markdown("### ✅ HR Report")
                    st.write(result.get("hr_result", {}).get("full_report", ""))

                results.append(result)

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                results.append({
                    "candidate_name": uploaded_file.name,
                    "overall_score": 0,
                    "recommendation": "ERROR",
                    "error": str(e)
                })

            progress_bar.progress((idx + 1) / len(uploaded_files))

        st.session_state["results"] = results
        st.success("✅ Multi-Agent Pipeline Completed")

# ===================================================
# TAB 2
# ===================================================

with tab2:

    st.subheader("Candidate Analytics")

    if "results" not in st.session_state:
        st.info("Run the pipeline first to see analytics.")

    else:

        results = st.session_state["results"]

        if not results:
            st.warning("No results available.")

        else:

            # -----------------------------------------
            # SUMMARY TABLE
            # -----------------------------------------

            table_data = []
            for r in results:
                table_data.append({
                    "Candidate": r.get("candidate_name", "Unknown"),
                    "Match Score": r.get("match_result", {}).get("match_percentage", "N/A"),
                    "Verdict": r.get("match_result", {}).get("verdict", "N/A"),
                    "Matched Skills": ", ".join(r.get("match_result", {}).get("matched_skills", [])),
                    "HR Decision": r.get("hr_result", {}).get("recommendation", "N/A")
                })

            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)

            # -----------------------------------------
            # BAR CHART
            # -----------------------------------------

            try:
                chart_df = df.copy()
                chart_df["Score"] = chart_df["Match Score"].str.replace("%", "").astype(float)

                fig = px.bar(
                    chart_df,
                    x="Candidate",
                    y="Score",
                    color="Score",
                    title="Candidate Match Scores",
                    color_continuous_scale="Greens"
                )
                st.plotly_chart(fig, use_container_width=True)

            except Exception:
                st.info("Chart not available.")

            # -----------------------------------------
            # DOWNLOAD CSV
            # -----------------------------------------

            csv = df.to_csv(index=False)
            st.download_button(
                "⬇️ Download Results CSV",
                csv,
                "candidate_results.csv",
                "text/csv"
            )