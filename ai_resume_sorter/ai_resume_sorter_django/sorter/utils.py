import re
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ai_resume_sorter.ai_resume_sorter_django.sorter.utils.job_titles import job_titles


def extract_text_from_resume(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return docx2txt.process(uploaded_file)
    return ""


def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text


def extract_skills(text):
    all_skills = set()
    for job in job_titles:
        for skill in job['required_skills']:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text.lower()):
                all_skills.add(skill)
    return list(all_skills)


def suggest_job_titles(text):
    suggestions = []
    if "python" in text.lower():
        suggestions += ['Python Developer', 'Backend Developer', 'Data Analyst']
    if "project manager" in text.lower():
        suggestions += ['Project Manager', 'Scrum Master', 'Program Manager']
    if "sql" in text.lower():
        suggestions += ['Database Administrator', 'Data Analyst', 'BI Developer']
    if not suggestions:
        suggestions = ['Software Engineer', 'Full Stack Developer', 'Technical Associate']
    return suggestions


def calculate_relevance_score(job_description, resume_text):
    documents = [job_description, resume_text]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]
