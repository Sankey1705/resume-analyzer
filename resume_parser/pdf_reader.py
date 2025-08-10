import os
import fitz  # PyMuPDF

def read_pdf(file_path):
    """Reads PDF and extracts text."""
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def read_all_resumes(resume_folder):
    """Reads all PDFs in a folder."""
    resumes = {}
    for file in os.listdir(resume_folder):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(resume_folder, file)
            resumes[file] = read_pdf(full_path)
    return resumes
