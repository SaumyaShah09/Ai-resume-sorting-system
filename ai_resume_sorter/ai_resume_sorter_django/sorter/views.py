import os
import zipfile
import re
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .resume_parser import extract_text
from .utils.job_titles import job_titles
from .utils.skill_matcher import match_resume_to_job, extract_skills_from_text, suggest_job_titles


# -----------------------------------------------
# 🔍 Helper: Get required skills based on job role
# -----------------------------------------------
def get_required_skills(job_role):
    job_role = job_role.lower()
    skills_dict = {
        'data analyst': ['python', 'sql', 'excel', 'power bi', 'tableau', 'statistics', 'data cleaning'],
        'web developer': ['html', 'css', 'javascript', 'react', 'django', 'node.js', 'bootstrap'],
        'python developer': ['python', 'django', 'flask', 'pandas', 'numpy', 'oop'],
        'ml engineer': ['python', 'machine learning', 'tensorflow', 'keras', 'pandas', 'scikit-learn'],
        'android developer': ['kotlin', 'java', 'android studio', 'xml', 'firebase'],
        'ai engineer': ['deep learning', 'tensorflow', 'pytorch', 'nlp', 'huggingface', 'transformers'],
        'business analyst': ['excel', 'sql', 'power bi', 'tableau', 'requirement analysis'],
        'data scientist': ['python', 'machine learning', 'deep learning', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
    }
    for key in skills_dict:
        if key in job_role:
            return skills_dict[key]
    return ['communication', 'teamwork', 'problem-solving']


# -----------------------------------------------
# 🔍 Skill Matching Logic
# -----------------------------------------------
def match_resume_to_job(resume_text, job_role):
    resume_text = resume_text.lower()
    required_skills = get_required_skills(job_role)
    required_skills = [skill.lower().strip() for skill in required_skills]
    matched_skills = [skill for skill in required_skills if skill in resume_text]
    missing_skills = [skill for skill in required_skills if skill not in resume_text]
    return {
        'required_skills': required_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills
    }


# -----------------------------------------------
# 📊 Relevance Score
# -----------------------------------------------
def calculate_relevance_score(job_role, resume_text):
    match_result = match_resume_to_job(resume_text, job_role)
    matched = match_result['matched_skills']
    total = match_result['required_skills']
    return len(matched) / len(total) if total else 0.0


# -----------------------------------------------
# 📤 Upload Resume View
# -----------------------------------------------
@login_required
def upload_resume(request):
    results = []
    error_message = ""
    job_role = ""
    required_skills = []
    matched_skills_per_resume = []

    if request.method == 'POST':
        resumes = request.FILES.getlist('resumes')
        job_role = request.POST.get('job_role', '')

        shortlisted_dir = os.path.join(settings.MEDIA_ROOT, 'shortlisted')
        os.makedirs(shortlisted_dir, exist_ok=True)

        for resume_file in resumes:
            file_name = resume_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            with open(file_path, 'wb+') as destination:
                for chunk in resume_file.chunks():
                    destination.write(chunk)

            try:
                extracted_text = extract_text(file_path)
                match_result = match_resume_to_job(extracted_text, job_role)
                required_skills = match_result['required_skills']
                matched_skills = match_result['matched_skills']
                missing_skills = match_result['missing_skills']
                matched_skills_per_resume.append(matched_skills)
                score = calculate_relevance_score(job_role, extracted_text)

                results.append({
                    'file_name': file_name,
                    'score': round(score * 100, 2),
                    'text': extracted_text,
                    'path': file_path,
                    'required_skills': required_skills,
                    'matched_skills': matched_skills,
                    'missing_skills': missing_skills
                })

                if score >= 0.5:
                    shortlisted_path = os.path.join(shortlisted_dir, file_name)
                    with open(shortlisted_path, 'wb') as out_file:
                        with open(file_path, 'rb') as in_file:
                            out_file.write(in_file.read())

            except Exception as e:
                error_message += f"❌ Failed to process {file_name}: {str(e)}\n"

        results.sort(key=lambda x: x['score'], reverse=True)

        if not get_required_skills(job_role):
            error_message += f"⚠️ No skills found for job role '{job_role}'. Please check spelling or update ontology."

    file_names = [res['file_name'] for res in results]
    scores = [res['score'] for res in results]

    return render(request, 'sorter/upload.html', {
        'results': results,
        'job_role': job_role,
        'error': error_message,
        'file_names': file_names,
        'scores': scores,
        'required_skills': required_skills,
        'matched_skills_per_resume': matched_skills_per_resume
    })


# -----------------------------------------------
# 📥 Download ZIP of Shortlisted Resumes
# -----------------------------------------------
@login_required
def download_shortlisted(request):
    shortlisted_folder = os.path.join(settings.MEDIA_ROOT, 'shortlisted')
    if not os.path.exists(shortlisted_folder) or not os.listdir(shortlisted_folder):
        return HttpResponse("No shortlisted resumes found.", status=404)
    zip_filename = os.path.join(settings.MEDIA_ROOT, "shortlisted_resumes.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for filename in os.listdir(shortlisted_folder):
            file_path = os.path.join(shortlisted_folder, filename)
            zipf.write(file_path, filename)
    with open(zip_filename, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="shortlisted_resumes.zip"'
    os.remove(zip_filename)
    return response


# 👤 User Registration
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            messages.error(request, "Username can only contain letters, numbers, _, ., and -")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect("upload_resume")

    return render(request, "auth/register.html")


# 🔐 User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("upload_resume")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------------------------
# 🧠 Job Title Suggestion Upload Page
# -----------------------------------------------
@login_required
def suggest_title(request):
    return render(request, 'sorter/suggest_title.html')


# -----------------------------------------------
# 📄 Upload Resume for Job Title Suggestion
# -----------------------------------------------
@login_required
def suggest_roles_from_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        uploaded_file = request.FILES['resume']
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_resume.pdf')

        # Save uploaded resume to server
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            # Extract text from resume
            extracted_text = extract_text(file_path).lower()

            # Extract skills
            extracted_skills = extract_skills_from_text(extracted_text)

            # Suggest job titles
            suggestions = suggest_job_titles(extracted_skills, job_titles)

            return render(request, 'sorter/suggested_titles.html', {
                'extracted_skills': extracted_skills,
                'suggestions': suggestions
            })

        except Exception as e:
            messages.error(request, f"Error extracting resume: {str(e)}")
            return redirect('suggest_title')

    return render(request, 'sorter/suggest_title.html')
