# skills_helper.py
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined list of skills (You can expand this list)
skills_list = ['Python', 'SQL', 'Excel', 'Tableau', 'Machine Learning', 'Data Analysis', 'Java', 'R']

# Predefined required skills for different job roles
required_skills_dict = {
    'Data Analyst': ['Python', 'SQL', 'Excel', 'Tableau', 'Data Analysis'],
    'Software Engineer': ['Java', 'Python', 'C++', 'Algorithms', 'Data Structures'],
    # Add more roles and skills here
}


def extract_skills_from_text(text):
    # Process the text with spaCy to analyze it
    doc = nlp(text.lower())  # Lowercase text for easier matching
    extracted_skills = []

    # Look for skills in the predefined list
    for skill in skills_list:
        if skill.lower() in text.lower():
            extracted_skills.append(skill)

    return extracted_skills


def compare_skills(extracted_skills, job_role):
    # Get the required skills for the given job role
    required_skills = required_skills_dict.get(job_role, [])

    # Find the missing skills
    missing_skills = [skill for skill in required_skills if skill not in extracted_skills]

    return missing_skills
