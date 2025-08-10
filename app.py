import os
import json
import streamlit as st
import importlib.util
import fitz  # PyMuPDF to read PDFs

# Dynamic module loader
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules dynamically
BASE_DIR = os.path.dirname(__file__)
extractor = load_module_from_path("extractor", os.path.join(BASE_DIR, "resume_parser", "extractor.py"))
matcher = load_module_from_path("matcher_tfidf", os.path.join(BASE_DIR, "resume_parser", "matcher_tfidf.py"))

# Read PDF text function
def read_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

# Load job descriptions from json file
def load_job_descriptions(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    return jobs

st.title("Resume Matcher - Multi Job Description")

# Upload multiple resumes
uploaded_files = st.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)

# Load job descriptions
job_desc_path = os.path.join(BASE_DIR, "job_descriptions.json")
jobs = load_job_descriptions(job_desc_path)

if uploaded_files:
    resumes = {}
    for file in uploaded_files:
        resumes[file.name] = read_pdf(file)
    
    st.sidebar.header("Job Descriptions:")
    for jd_index, jd in enumerate(jobs):
        st.sidebar.markdown(f"**{jd.get('title', 'Unknown Title')} **")
    
    
    for jd in jobs:
        st.header(f"Job: {jd.get('title', 'Unknown Title')} ")
        skills_required = jd.get("skills_required", [])
        
        for resume_name, resume_text in resumes.items():
            
            skills_found = extractor.extract_skills(resume_text)

            
            
            match_score = matcher.match_resume_with_jd({resume_name: resume_text}, jd).get(resume_name, 0)
            
            st.subheader(f"Resume: {resume_name}")
            st.write(f"Skills found: {', '.join(skills_found) if skills_found else 'None'}")
            st.progress(match_score / 100)
            st.write(f"Match Score: {match_score}%")
            st.markdown("---")

else:
    st.info("Please upload one or more PDF resumes to start matching.")


