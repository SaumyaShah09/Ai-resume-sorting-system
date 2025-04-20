# sorter/utils/skill_matcher.py

import re

# This ontology seems potentially redundant if job_titles.py is the source of truth for required skills.
# It's currently used by extract_skills and get_required_skills below.
# Consider consolidating skill definitions.
SKILL_ONTOLOGY = {
    'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn', 'Data Visualization',
                       'Deep Learning', 'Statistics', 'Power BI', 'Tableau', 'Jupyter'],
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Bootstrap', 'Django', 'Flask', 'MongoDB',
                      'MySQL', 'REST API', 'Git', 'TypeScript', 'Sass'],
    'Android Developer': ['Java', 'Kotlin', 'Android Studio', 'SQLite', 'Firebase', 'Jetpack Compose', 'XML', 'REST API'],
    'AI Engineer': ['Python', 'TensorFlow', 'PyTorch', 'NLP', 'Transformers', 'Hugging Face', 'Scikit-learn', 'OpenCV',
                    'CNN', 'RNN', 'Docker', 'AWS'],
    'Software Engineer': ['Python', 'Java', 'C++', 'Algorithms', 'Data Structures', 'SQL', 'Git', 'Docker', 'REST API', 'Django', 'Flask'],
    'Data Analyst': ['Excel', 'SQL', 'Power BI', 'Tableau', 'Data Visualization', 'Statistics', 'Python', 'Reporting'],
    'ML Engineer': ['Python', 'TensorFlow', 'Keras', 'PyTorch', 'Machine Learning', 'Data Science', 'Neural Networks', 'Pandas', 'Docker', 'AWS'],
    'Business Analyst': ['Excel', 'SQL', 'Business Intelligence', 'Data Visualization', 'Reporting', 'Tableau', 'Power BI', 'Requirements Gathering', 'Jira'],
    'Frontend Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'Bootstrap', 'TypeScript', 'Sass'],
    'Backend Developer': ['Python', 'Django', 'Flask', 'Node.js', 'Express', 'MongoDB', 'SQL', 'REST API', 'Docker', 'Kubernetes', 'AWS'],
     # Add roles corresponding to keys in job_titles.py
}

# ---- Skill Extraction Functions ----

def extract_skills(text):
    """Extracts skills from text based on the SKILL_ONTOLOGY."""
    if not isinstance(text, str):
        # Attempt to handle non-string input, e.g., list
        if isinstance(text, list):
            text = ' '.join(map(str, text))
        else:
            text = str(text) # Force conversion

    all_defined_skills = set()
    for skills in SKILL_ONTOLOGY.values():
        all_defined_skills.update([s.lower() for s in skills])

    found_skills = set() # Use a set to avoid duplicates initially
    text_lower = text.lower()

    # Simple regex match for skills (consider more advanced NLP if needed)
    for skill in all_defined_skills:
        # Use word boundaries to avoid matching substrings (e.g., 'react' in 'reaction')
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            # Find original casing from ontology for better presentation
            original_case_skill = next((s for s_list in SKILL_ONTOLOGY.values() for s in s_list if s.lower() == skill), skill.title())
            found_skills.add(original_case_skill)

    return list(found_skills)


def extract_skills_from_text(text, specific_skill_list):
    """Extracts skills from text ONLY if they appear in the specific_skill_list."""
    if not isinstance(text, str):
        if isinstance(text, list):
            text = ' '.join(map(str, text))
        else:
            text = str(text)

    found_skills = []
    text_lower = text.lower()
    for skill in specific_skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill) # Keep original casing from specific_skill_list
    return list(set(found_skills)) # Return unique matches


# ---- Functions primarily used by 'upload_resume' feature ----

def get_required_skills(job_role):
    """Gets required skills for a role based on SKILL_ONTOLOGY."""
    # Consider fetching from job_titles.py dictionary for consistency?
    job_role_clean = job_role.strip().title()
    return SKILL_ONTOLOGY.get(job_role_clean, [])

def match_resume_to_job(resume_text, job_role):
    """Calculates match between resume text and required skills for a job role."""
    # This uses get_required_skills (based on SKILL_ONTOLOGY) and
    # extract_skills_from_text (from this file)
    required = get_required_skills(job_role)
    if not required: # Handle case where job role isn't in ontology
        return {
            'required_skills': [], 'matched_skills': [], 'missing_skills': [],
            'ideal_vector': [], 'resume_vector': []
        }

    # Extract *only* the required skills found in the resume text
    matched = extract_skills_from_text(resume_text, required)
    missing = [skill for skill in required if skill not in matched]
    ideal_vector = [1] * len(required)
    resume_vector = [1 if skill in matched else 0 for skill in required]
    return {
        'required_skills': required,
        'matched_skills': matched,
        'missing_skills': missing,
        'ideal_vector': ideal_vector,
        'resume_vector': resume_vector
    }


# ---- CORRECTED Function for 'suggest_title_view' ----

def suggest_job_titles(extracted_skills, job_titles_dict):
    """
    Suggests job titles from job_titles_dict based on a list of extracted_skills.

    Args:
        extracted_skills (list): Skills found in the resume (e.g., ['Python', 'SQL']).
                                 This list should come from a skill extraction function called by the view.
        job_titles_dict (dict): The dictionary from job_titles.py
                                (e.g., {"Data Analyst": ["excel", "sql",...]}).

    Returns:
        list: A list of suggested job title strings, ordered by relevance (best first).
              Returns an empty list if no suitable titles are found.
    """
    if not extracted_skills or not job_titles_dict:
        return [] # Cannot suggest without skills or job definitions

    # Use lowercase set for efficient and case-insensitive matching
    extracted_skills_lower = set(skill.lower() for skill in extracted_skills)
    results = []

    # Iterate through the job titles dictionary
    for title, required_skills_list in job_titles_dict.items():
        if not required_skills_list:
            continue # Skip titles with no defined skills

        required_skills_lower = set(s.lower() for s in required_skills_list)
        matched_skills = extracted_skills_lower.intersection(required_skills_lower)
        score = len(matched_skills) # Simple score: number of matched skills

        # --- Thresholding Logic (Adjust as needed) ---
        # Suggest if a minimum number of skills match OR a minimum percentage match
        min_match_count = 2  # e.g., Require at least 2 matching skills...
        min_match_percentage = 0.3 # ...or if 30% or more of required skills match

        is_match = False
        if score >= min_match_count:
            is_match = True
        elif len(required_skills_lower) > 0: # Avoid division by zero
             match_ratio = score / len(required_skills_lower)
             if match_ratio >= min_match_percentage:
                 is_match = True
        # --- End Thresholding ---

        if is_match:
             results.append({
                 "title": title, # The job title string
                 "score": score, # Score used for sorting
             })

    # Sort results by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Extract just the titles in sorted order
    suggested_titles_list = [result["title"] for result in results]

    # Limit the number of suggestions (optional)
    # max_suggestions = 5
    # return suggested_titles_list[:max_suggestions]

    return suggested_titles_list