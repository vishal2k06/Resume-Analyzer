import streamlit as st
import pdfplumber
import spacy
import os
import pandas as pd

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ----------- Keyword Extraction (Dual Match) -----------

def extract_keywords(text):
    doc = nlp(text.lower())
    original_words = set()
    lemmatized_words = set()

    for token in doc:
        if token.is_alpha and not token.is_stop and token.pos_ in ["NOUN", "PROPN", "VERB"]:
            original_words.add(token.text.lower())
            lemmatized_words.add(token.lemma_.lower())

    return original_words.union(lemmatized_words)

# ----------- PDF Text Extraction -----------

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text.lower()

# ----------- Resume vs JD Matching -----------

def analyze_resume(jd_text, resume_text):
    jd_keywords = extract_keywords(jd_text)

    # Preprocess resume text with spaCy
    doc = nlp(resume_text)
    resume_words = set()
    for token in doc:
        if token.is_alpha:
            resume_words.add(token.text.lower())
            resume_words.add(token.lemma_.lower())

    found = []
    missing = []

    for word in jd_keywords:
        if word in resume_words:
            found.append(word)
        else:
            missing.append(word)

    score = round((len(found) / len(jd_keywords)) * 100, 2) if jd_keywords else 0
    return found, missing, score

# ----------- Streamlit GUI -----------

st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("Resume Analyzer for Job Description Match")
st.write("Upload your resume and paste the job description. The tool will analyze the match based on keywords.")

# Upload Resume
resume_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

# Paste Job Description
jd_input = st.text_area("Paste the Job Description here", height=250)

# Analyze Button
if st.button("Analyze Resume"):

    if not resume_file:
        st.warning("Please upload a resume.")
    elif not jd_input.strip():
        st.warning("Please paste a job description.")
    else:
        try:
            # Extract text and analyze
            resume_text = extract_text_from_pdf(resume_file)
            found, missing, score = analyze_resume(jd_input, resume_text)

            # Display results
            st.success(f"Match Score: {score}%")
            st.subheader("Found Keywords:")
            st.write(", ".join(found) if found else "None")

            st.subheader("Missing Keywords:")
            st.write(", ".join(missing) if missing else "None")

            # Save results to Excel
            file_name = resume_file.name
            row = {
                "Resume File": file_name,
                "Match Score": f"{score}%",
                "Found Keywords": ", ".join(found),
                "Missing Keywords": ", ".join(missing)
            }

            excel_file = "results.xlsx"

            if os.path.exists(excel_file):
                df_existing = pd.read_excel(excel_file)
                df_updated = pd.concat([df_existing, pd.DataFrame([row])], ignore_index=True)
            else:
                df_updated = pd.DataFrame([row])

            try:
                df_updated.to_excel(excel_file, index=False)
                st.success(f"Analysis saved to '{excel_file}'")
            except PermissionError:
                st.warning("Please close 'results.xlsx' if it's open and try again.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
