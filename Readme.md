# Placement Readiness Expert System

This project is a rule-based expert system designed to evaluate a student’s placement readiness in a realistic and practical way.  
Instead of judging a student using only CGPA or coding scores, the system looks at **multiple aspects together** and gives a clear readiness status along with improvement guidance.

The idea came from a simple observation:  
Students are often labeled “ready” or “not ready” based on one strong or weak factor, which is misleading. This system avoids that by balancing all important placement factors.

---

## What Problem Does This Solve?

In most colleges, placement readiness is judged informally and inconsistently.  
Some students have good grades but poor coding consistency, while others are strong coders but have backlogs or weak resumes.

This system:

- Prevents false “READY” results due to one strong skill
- Flags **critical risk conditions** early
- Gives **clear, actionable feedback** instead of vague scores

---

## How the System Works

The expert system uses:

- Predefined rules (like a human placement mentor)
- Dynamic weight adjustment based on branch
- Benchmark comparison using historical student data

Each input is scored, combined, and then validated using **critical failure checks** to ensure the final result is realistic.

---

## Readiness Categories

- **READY** – Eligible and competitive for placements
- **IMPROVE** – Some gaps present, needs focused effort
- **HIGH RISK** – Major blockers that affect placement eligibility

A student cannot be marked READY if critical issues like backlogs, zero projects, or very low coding consistency are present — no matter how good one metric is.

---

## Inputs Considered

- Branch
- CGPA
- Coding practice (LeetCode score, weekly problems)
- Projects
- Internships
- Backlogs
- CDC band
- GitHub commits
- Certificates
- Mock interviews

All inputs together decide the final outcome.

---

## Output Provided

The system generates:

- Overall readiness status
- Total weighted score
- Area-wise performance explanation
- Risk factors (if any)
- Personalized improvement plan

The feedback is written in simple language so students can actually act on it.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Streamlit (for UI)

No black-box machine learning models are used.  
The focus is on **transparent, explainable decision logic**.

---

## Project Structure

Placement Readiness Expert System/
│
├── expertsystem.py # Core expert system logic
├── app.py # Streamlit UI
├── requirements.txt
├── README.md
└── outputs(1,2,3)
