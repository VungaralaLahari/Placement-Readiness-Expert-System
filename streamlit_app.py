import streamlit as st
from expert_system import PlacementExpertSystem

st.set_page_config(page_title="Campus Placement Predictor", layout="wide")

st.markdown("""
# Placement Readiness Expert System
---
""")

expert = PlacementExpertSystem()

# ---------------- INPUT SECTION ----------------
with st.expander("Enter Student Profile", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        branch = st.selectbox("Branch", ['CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CSM', 'CSD', 'CSC'])
        cgpa = st.slider("CGPA", 5.0, 10.0, 7.0, 0.1)
        backlogs = st.number_input("Backlogs", 0, 10, 2)
        leetcode = st.number_input("LeetCode solved", 0, 500, 100)
        projects = st.number_input("Projects", 0, 20, 7)

    with col2:
        cdc_band = st.selectbox("CDC Band", ['A', 'B', 'C', 'D'])
        weekly_problems = st.number_input("Weekly coding problems", 0, 50, 14)
        internships = st.number_input("Internships", 0, 10, 5)
        github_commits = st.number_input("GitHub commits (90 days)", 0, 500, 10)
        certs = st.number_input("Certificates", 0, 50, 15)
        mocks = st.number_input("Mock interviews", 0, 20, 2)

data = {
    'branch': branch,
    'cgpa': cgpa,
    'backlogs': backlogs,
    'leetcode': leetcode,
    'projects': projects,
    'cdc_band': cdc_band,
    'weekly_problems': weekly_problems,
    'internships': internships,
    'github_commits': github_commits,
    'certs': certs,
    'mocks': mocks
}

# ---------------- ANALYSIS ----------------
if st.button("Analyze Placement Readiness", use_container_width=True):

    result = expert.analysis_report(data)

    st.markdown("---")
    st.subheader("Placement Summary")

    colA, colB, colC = st.columns(3)
    colA.metric("Branch", branch)
    colB.metric("Total Score", int(result['total_score']))
    colC.metric("Status", result['status'])

    # ---------------- SCORES ----------------
    st.markdown("---")
    st.subheader("Detailed Scores")
    for metric, score in result['scores'].items():
        explanation = result['explanations'][metric]
        st.write(f"{metric.upper():<15} : {int(score)} → {explanation}")

    # ---------------- RISKS ----------------
    if result['risks']:
        st.markdown("---")
        st.subheader("Risks Identified")
        for r in result['risks']:
            st.warning(r)

    # ---------------- ACTION PLAN ----------------
    if result['action_plan']:
        st.markdown("---")
        st.subheader("Personalized Action Plan")
        for step in result['action_plan']:
            st.info(step)
