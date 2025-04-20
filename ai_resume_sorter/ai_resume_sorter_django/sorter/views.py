import os
import zipfile
import re
import spacy
import tempfile
from django.shortcuts import render, redirect # Ensure redirect is imported
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Import necessary utility functions
from .utils.job_titles import job_titles
# NOTE: The line below imports from skills_helper, but suggest_title_view uses extract_skills from skill_matcher.
# This might be intentional if upload_resume needs skills_helper's version, but double-check consistency if needed.
from .utils.skills_helper import extract_skills_from_text as extract_skills_helper # Renamed import to avoid conflict
# Import functions from skill_matcher
from .utils.skill_matcher import match_resume_to_job, suggest_job_titles, extract_skills # extract_skills is used by suggest_title_view
from .resume_parser import extract_text

# Initialize spaCy (handled within skills_helper.py now)

# -----------------------------------------------
# 🔍 Helper: Get required skills (Used by upload_resume)
# -----------------------------------------------
# This function seems specific to upload_resume's direct matching logic.
# Consider if it should use the main job_titles dict for consistency.
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
# 📊 Relevance Score (Used by upload_resume)
# -----------------------------------------------
def calculate_relevance_score(job_role, resume_text):
    match_result = match_resume_to_job(resume_text, job_role) # Uses skill_matcher's version
    matched = match_result.get('matched_skills', []) # Use .get for safety
    total = match_result.get('required_skills', []) # Use .get for safety
    return len(matched) / len(total) if total else 0.0

# -----------------------------------------------
# 📤 Upload Resume View
# -----------------------------------------------
@login_required # Ensures user is logged in
def upload_resume(request):
    results, error_message, required_skills, matched_skills_per_resume = [], "", [], []
    job_role = request.POST.get('job_role', '') if request.method == 'POST' else ''

    if request.method == 'POST':
        if not request.FILES.getlist('resumes'):
             messages.error(request, "Please upload at least one resume file.")
             # Re-render the form page if no files uploaded on POST
             return render(request, 'sorter/upload.html', {'job_role': job_role})

        resumes = request.FILES.getlist('resumes')
        shortlisted_dir = os.path.join(settings.MEDIA_ROOT, 'shortlisted')
        os.makedirs(shortlisted_dir, exist_ok=True)
        temp_files_to_clean = [] # Keep track of temp files if using them

        for resume_file in resumes:
            file_name = resume_file.name
            # --- Using temporary file for processing is safer ---
            file_extension = os.path.splitext(resume_file.name)[1]
            try:
                 with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                     for chunk in resume_file.chunks():
                         temp_file.write(chunk)
                     temp_file_path = temp_file.name
                 temp_files_to_clean.append(temp_file_path) # Add to cleanup list

                 extracted_text = extract_text(temp_file_path)
                 if not extracted_text:
                     print(f"Warning: Could not extract text from {file_name}")
                     # Skip this file or add error? Let's add an error message part
                     error_message += f"⚠️ Could not extract text from {file_name}. Skipping.\n"
                     continue # Skip to next file

                 match_result = match_resume_to_job(extracted_text, job_role) # Uses skill_matcher
                 required_skills_for_role = match_result.get('required_skills', [])
                 matched_skills = match_result.get('matched_skills', [])
                 missing_skills = match_result.get('missing_skills', [])
                 matched_skills_per_resume.append(matched_skills)
                 score = calculate_relevance_score(job_role, extracted_text)

                 results.append({
                     'file_name': file_name, 'score': round(score * 100, 2),
                     'text': extracted_text[:500] + "..." if extracted_text and len(extracted_text) > 500 else extracted_text, # Truncate text for display
                     # 'path': temp_file_path, # Avoid exposing temp path
                     'required_skills': required_skills_for_role,
                     'matched_skills': matched_skills, 'missing_skills': missing_skills
                 })

                 if score >= 0.5:
                     # Copy from temp file to shortlisted dir
                     shortlist_path = os.path.join(shortlisted_dir, file_name)
                     with open(shortlist_path, 'wb') as out_file, open(temp_file_path, 'rb') as in_file:
                         out_file.write(in_file.read())

            except Exception as e:
                 error_message += f"❌ Failed to process {file_name}: {str(e)}\n"
                 # Log full traceback for debugging
                 import traceback
                 print(f"Error processing {file_name}:\n{traceback.format_exc()}")
            # --- Temp file cleanup happens after the loop ---

        # --- Cleanup all temporary files ---
        for path in temp_files_to_clean:
             if os.path.exists(path):
                 try:
                     os.remove(path)
                 except OSError as e:
                     print(f"Error deleting temp file {path}: {e}")

        # Sort results and determine required skills for context
        results.sort(key=lambda x: x['score'], reverse=True)
        if results:
             required_skills = results[0]['required_skills']
        elif job_role:
              required_skills = get_required_skills(job_role) # Check get_required_skills logic

        if job_role and not required_skills:
             error_message += f"⚠️ No required skills could be determined for the job role '{job_role}'. Check role or definitions.\n"

    # Render results or the initial form
    return render(request, 'sorter/upload.html', {
        'results': results, 'job_role': job_role, 'error': error_message,
        'file_names': [res['file_name'] for res in results],
        'scores': [res['score'] for res in results],
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
        messages.info(request, "No shortlisted resumes found to download.")
        # --- UPDATE REDIRECT: Use namespace ---
        # Decide whether to redirect back or to the upload page
        # return redirect(request.META.get('HTTP_REFERER', 'sorter:upload_resume'))
        # Or render the upload page with the message
        return render(request, 'sorter/upload.html', {'info': "No shortlisted resumes found to download."})

    zip_filename_base = "shortlisted_resumes.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename_base)

    try:
        # ... (zip creation logic remains the same) ...
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(shortlisted_folder):
                file_path = os.path.join(shortlisted_folder, filename)
                if os.path.isfile(file_path):
                    zipf.write(file_path, filename)

        if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{zip_filename_base}"'
            os.remove(zip_path)
            # Optional: Clean up individual files after zipping
            # for filename in os.listdir(shortlisted_folder):
            #    os.remove(os.path.join(shortlisted_folder, filename))
            return response
        else:
            if os.path.exists(zip_path):
                 os.remove(zip_path)
            messages.error(request, "Could not create the zip file or no files were added.")
             # --- UPDATE REDIRECT: Use namespace ---
            # Redirect back if possible, otherwise to upload page
            referer = request.META.get('HTTP_REFERER')
            # Basic check to avoid redirect loops if referer is the download URL itself
            if referer and 'download_shortlisted' not in referer:
                 return redirect(referer)
            else:
                 return redirect('sorter:upload_resume')


    except Exception as e:
        print(f"Error creating zip file: {e}")
        messages.error(request, "An error occurred while creating the zip file.")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        # --- UPDATE REDIRECT: Use namespace ---
        referer = request.META.get('HTTP_REFERER')
        if referer and 'download_shortlisted' not in referer:
             return redirect(referer)
        else:
             return redirect('sorter:upload_resume')


# -----------------------------------------------
# 👤 User Registration
# -----------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
         # --- UPDATE REDIRECT: Use namespace ---
         return redirect('sorter:home') # Redirect logged-in users away from register page

    if request.method == "POST":
        # ... (validation logic remains the same) ...
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password or not confirm_password:
             messages.error(request, "All fields are required.")
             return render(request, "auth/register.html")
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            messages.error(request, "Username can only contain letters, numbers, _, ., and -")
            return render(request, "auth/register.html")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/register.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
            return render(request, "auth/register.html")
        if User.objects.filter(email=email).exists():
            messages.error(request, f"Email '{email}' is already registered.")
            return render(request, "auth/register.html")

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            messages.success(request, f"Registration successful! Welcome, {username}.")
            # --- UPDATE REDIRECT: Use namespace ---
            # Redirect to home page after registration
            return redirect("sorter:home")
        except Exception as e:
             messages.error(request, f"An error occurred during registration: {e}")
             return render(request, "auth/register.html")

    # For GET request
    return render(request, "auth/register.html")

# -----------------------------------------------
# 🔐 User Login
# -----------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
         # --- UPDATE REDIRECT: Use namespace ---
         # Redirect already logged-in users to the home page
         return redirect('sorter:home')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")

        if not username or not password:
             messages.error(request, "Both username and password are required.")
             return render(request, "auth/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the 'next' page if specified, otherwise to the app home page
            next_url = request.GET.get('next')
            if next_url:
                 # Basic security check: ensure next_url is internal or safe
                 # Add more robust validation if needed (e.g., using url_has_allowed_host_and_scheme)
                 if next_url.startswith('/app/') or next_url.startswith('/admin/'): # Allow app or admin urls
                    return redirect(next_url)
                 else:
                    # --- UPDATE REDIRECT: Use namespace (fallback) ---
                    return redirect('sorter:home')
            else:
                 # --- UPDATE REDIRECT: Use namespace (default after login) ---
                 return redirect("sorter:home") # Default redirect after login to home
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "auth/login.html") # Render login page again with error

    # For GET request
    return render(request, "auth/login.html")

# -----------------------------------------------
# 🔑 User Logout
# -----------------------------------------------
# Use login_required decorator for logout view for consistency
@login_required
def logout_view(request):
    # Ensure logout is done via POST for security best practices
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        # --- UPDATE REDIRECT: Use namespace ---
        return redirect('sorter:login') # Redirect to namespaced login page
    else:
        # If accessed via GET, perhaps redirect to home or show a confirmation page?
        # For simplicity, redirecting to login might be okay here, but POST is preferred.
         # --- UPDATE REDIRECT: Use namespace ---
        return redirect('sorter:login')


# -----------------------------------------------
# ✨ Suggest Job Titles View
# -----------------------------------------------
@login_required # Protect this view
def suggest_title_view(request):
    context = {} # Initialize context dictionary

    if request.method == 'POST':
        if 'resume' not in request.FILES:
            context['error'] = "No resume file was uploaded. Please select a file."
            return render(request, 'sorter/suggest_title.html', context)

        resume_file = request.FILES['resume']

        # --- File Validation ---
        allowed_extensions = ['.pdf', '.docx']
        file_name, file_extension = os.path.splitext(resume_file.name)
        if file_extension.lower() not in allowed_extensions:
             context['error'] = f"Invalid file type ({file_extension}). Please upload a supported file ({', '.join(allowed_extensions)})."
             return render(request, 'sorter/suggest_title.html', context)
        # Optional: Add file size validation
        # MAX_UPLOAD_SIZE = 10 * 1024 * 1024 # 10 MB
        # if resume_file.size > MAX_UPLOAD_SIZE:
        #     context['error'] = f"File size exceeds the limit ({MAX_UPLOAD_SIZE // (1024*1024)} MB)."
        #     return render(request, 'sorter/suggest_title.html', context)

        # --- Processing with Temporary File ---
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                for chunk in resume_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            resume_text = extract_text(temp_file_path)
            if not resume_text:
                 context['error'] = "Could not extract text from the resume. File might be empty, image-based, or corrupted."
                 # Cleanup handled in finally block
                 return render(request, 'sorter/suggest_title.html', context)

            # Use extract_skills from skill_matcher (more comprehensive)
            extracted_skills = extract_skills(resume_text)
            context['skills'] = extracted_skills

            suggested_titles = suggest_job_titles(extracted_skills, job_titles) # Uses skill_matcher's suggest
            context['titles'] = suggested_titles

            if not suggested_titles and extracted_skills: # Info only if skills were found but no match
                 context['info'] = "Based on the detected skills, no specific job titles from our list were strongly matched."
            elif not extracted_skills:
                 context['info'] = "Could not detect relevant skills from the resume to suggest titles."


        except Exception as e:
            print(f"Error processing resume for suggestions: {e}")
            import traceback
            print(traceback.format_exc())
            context['error'] = f"An error occurred while processing the resume. Please ensure it's a valid text-based PDF or DOCX."
        finally:
            # --- Cleanup ---
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except OSError as e:
                     print(f"Error deleting temporary file {temp_file_path}: {e}")

    # --- Render Template ---
    return render(request, 'sorter/suggest_title.html', context)


# -----------------------------------------------
# 🏠 Homepage View
# -----------------------------------------------
def home_view(request):
    """Renders the homepage."""
    # If the user is not logged in, maybe redirect to login? Or let template handle display.
    # Let's assume the template handles the display for logged-in/out states.
    context = {}
    return render(request, 'sorter/home.html', context)