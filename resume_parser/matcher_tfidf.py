from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_with_jd(resume_texts, job_description):
    """Matches resumes with job description using TF-IDF similarity."""
    results = {}
    skills_required = job_description.get("skills_required", [])
    job_summary = job_description.get("job_summary", "")

    # Combine skills + summary into one searchable JD text
    jd_text = " ".join(skills_required) + " " + job_summary

    for file_name, text in resume_texts.items():
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([jd_text, text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        results[file_name] = round(similarity * 100, 2)  # percentage match
    return results
