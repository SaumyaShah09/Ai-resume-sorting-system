# sorter/utils/skills_helper.py

import spacy
import os # Import os to handle potential model loading errors

# --- spaCy Model Loading ---
SPACY_MODEL = "en_core_web_sm"
nlp = None
try:
    nlp = spacy.load(SPACY_MODEL)
    print(f"spaCy model '{SPACY_MODEL}' loaded successfully.")
except OSError:
    print(f"spaCy model '{SPACY_MODEL}' not found. Downloading...")
    try:
        spacy.cli.download(SPACY_MODEL)
        nlp = spacy.load(SPACY_MODEL)
        print(f"spaCy model '{SPACY_MODEL}' downloaded and loaded successfully.")
    except Exception as e:
        print(f"ERROR: Failed to download or load spaCy model '{SPACY_MODEL}'. spaCy functionality will be disabled. Error: {e}")
        # Fallback or further error handling could go here
except Exception as e:
    print(f"An unexpected error occurred loading spaCy model '{SPACY_MODEL}': {e}")

# --- Skill Definitions (Used by functions in THIS file) ---

# Predefined list of skills (This is very limited!)
# Consider replacing this with a more comprehensive list or using SKILL_ONTOLOGY from skill_matcher.py
skills_list = [
    'Python', 'SQL', 'Excel', 'Tableau', 'Power BI', 'Statistics', # Data Analyst related
    'Machine Learning', 'Deep Learning', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', # ML/DS related
    'Data Analysis', 'Data Visualization', 'Reporting', # Generic Data
    'Java', 'Kotlin', 'Android Studio', 'SQLite', 'Firebase', # Android
    'HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'Node.js', 'Bootstrap', 'TypeScript', # Web Frontend
    'Django', 'Flask', 'REST API', 'Git', 'Docker', 'AWS', 'MongoDB', # Web Backend / General SW
    'C++', 'Algorithms', 'Data Structures', # Core CS
    'Business Intelligence', 'Requirements Gathering', 'Jira', # Business Analyst
    'NLP', 'Transformers', 'Hugging Face', 'OpenCV', # AI Specific
    'Communication', 'Teamwork', 'Problem Solving' # Soft skills (harder to detect reliably)
]


# Predefined required skills (Seems redundant if job_titles.py is used)
# This might be used by the compare_skills function below.
required_skills_dict = {
    'Data Analyst': ['Python', 'SQL', 'Excel', 'Tableau', 'Data Analysis', 'Power BI'],
    'Software Engineer': ['Java', 'Python', 'C++', 'Algorithms', 'Data Structures', 'SQL', 'Git'],
    'ML Engineer': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Pandas', 'Scikit-learn'],
    # Add more roles matching keys in job_titles.py for consistency if needed
}

# ---- Skill Functions ----

def extract_skills_from_text(text):
    """
    Extracts skills from text using spaCy (if available) and the predefined 'skills_list'.
    NOTE: Currently called by views.suggest_title_view.
    Effectiveness depends heavily on the completeness of 'skills_list'.
    """
    if nlp is None:
        print("Warning: spaCy model not loaded. Skill extraction will be basic.")
        # Basic fallback: simple substring check without NLP context
        extracted_skills = []
        text_lower = text.lower() if isinstance(text, str) else str(text).lower()
        for skill in skills_list:
             # Basic check - might catch unintended words
             if skill.lower() in text_lower:
                 extracted_skills.append(skill)
        return list(set(extracted_skills))


    # Process with spaCy if available
    if not isinstance(text, str):
        text = str(text) # Ensure text is a string

    doc = nlp(text.lower()) # Process lowercase text with spaCy
    extracted_skills = set() # Use a set for efficiency

    # Option 1: Match against predefined skills_list (simple but limited)
    text_lower_for_check = text.lower() # Keep a lowercase version for direct checks
    for skill in skills_list:
        # Check if skill (lowercase) exists in the processed lowercase text
        if skill.lower() in text_lower_for_check:
            extracted_skills.add(skill) # Add the original case skill

    # Option 2 (More Advanced - Uncomment/Adapt if needed): Use spaCy's matcher or entity recognition
    # This requires setting up patterns or training an NER model
    # Example using phrase matcher:
    # from spacy.matcher import PhraseMatcher
    # matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    # patterns = [nlp.make_doc(skill) for skill in skills_list]
    # matcher.add("SKILL", patterns)
    # matches = matcher(doc)
    # for match_id, start, end in matches:
    #     span = doc[start:end]
    #     extracted_skills.add(span.text.title()) # Or keep original casing based on skills_list

    return list(extracted_skills)


def compare_skills(extracted_skills, job_role):
    """
    Compares extracted skills against required skills for a role (using required_skills_dict).
    NOTE: This function seems currently unused by the provided views.
    """
    # Get the required skills for the given job role from the dictionary in this file
    required_skills = required_skills_dict.get(job_role, [])
    if not required_skills:
        print(f"Warning: No required skills defined in skills_helper.required_skills_dict for job role: {job_role}")
        return [] # Return empty list if role not found or has no skills

    # Find the missing skills
    extracted_skills_set = set(extracted_skills) # For efficient lookup
    missing_skills = [skill for skill in required_skills if skill not in extracted_skills_set]

    return missing_skills