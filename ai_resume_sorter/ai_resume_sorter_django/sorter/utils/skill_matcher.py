import re

SKILL_ONTOLOGY = {
    'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn', 'Data Visualization', 'Deep Learning', 'Statistics', 'Power BI', 'Tableau'],
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Bootstrap', 'Django', 'Flask', 'MongoDB', 'MySQL'],
    'Android Developer': ['Java', 'Kotlin', 'Android Studio', 'SQLite', 'Firebase', 'Jetpack Compose'],
    'AI Engineer': ['Python', 'TensorFlow', 'PyTorch', 'NLP', 'Transformers', 'Hugging Face', 'Scikit-learn', 'OpenCV', 'CNN', 'RNN']
}

# ✅ This was missing earlier
def extract_skills(text):
    all_skills = []
    for skills in SKILL_ONTOLOGY.values():
        all_skills.extend(skills)

    found_skills = []
    for skill in set(all_skills):
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text.lower()):
            found_skills.append(skill)
    return found_skills


def extract_skills_from_text(text, skill_list):
    found_skills = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text.lower()):
            found_skills.append(skill)
    return found_skills


def get_required_skills(job_role):
    job_role_clean = job_role.strip().title()
    return SKILL_ONTOLOGY.get(job_role_clean, [])


def match_resume_to_job(resume_text, job_role):
    required_skills = get_required_skills(job_role)
    matched_skills = extract_skills_from_text(resume_text, required_skills)
    missing_skills = [skill for skill in required_skills if skill not in matched_skills]

    ideal_vector = [1] * len(required_skills)
    resume_vector = [1 if skill in matched_skills else 0 for skill in required_skills]

    return {
        'required_skills': required_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'ideal_vector': ideal_vector,
        'resume_vector': resume_vector
    }


def suggest_job_titles(resume_text, job_titles):
    extracted_skills = extract_skills(resume_text)  # ✅ Now this function exists!
    results = []

    for job in job_titles:
        matched = [skill for skill in extracted_skills if skill.lower() in [s.lower() for s in job['required_skills']]]
        score = len(matched)
        results.append({
            "job_title": job["title"],
            "score": score,
            "matched_skills": matched
        })

    # Sort by score and return top 1 only
    results.sort(key=lambda x: x["score"], reverse=True)

    if not results or results[0]["score"] == 0:
        return [{
            "job_title": "No suitable job role found 😕",
            "score": 0,
            "matched_skills": []
        }]

    return [results[0]]  # Return only the top result
