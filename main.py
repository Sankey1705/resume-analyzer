# main.py
import json
from resume_parser.pdf_reader import read_all_resumes
from resume_parser.extractor import extract_skills  # SkillNer version
from resume_parser.matcher_tfidf import match_resume_with_jd

# Load job descriptions (multiple)
with open("job_descriptions.json", "r") as f:
    job_descriptions = json.load(f)

# Read all resumes
resumes = read_all_resumes("resumes")

# Loop through each job description
for jd in job_descriptions:
    print(f"\n=== Matching for Job: {jd.get('title', 'Unknown')} at {jd.get('company', 'Unknown Company')} ===")

    # Extract skills from each resume using SkillNer
    for file_name, text in resumes.items():
        skills_found = extract_skills(text)
        print(f"\nResume: {file_name}")
        print("Skills Found:", skills_found)

    # Match using TF-IDF
    if "skills_required" in jd and "job_summary" in jd:
        match_results = match_resume_with_jd(resumes, jd)
        print("\nResume Match Scores:")
        for file_name, score in match_results.items():
            print(f"{file_name}: {score}% match")
    else:
        print("⚠ Job description missing 'skills_required' or 'job_summary', skipping match scoring.")
