# from sentence_transformers import SentenceTransformer
# from app.utils import get_similarity_score

# model = SentenceTransformer('all-MiniLM-L6-v2')  # Free & fast

# def get_match_score(cv_text, jd_text):
#     cv_vector = model.encode(cv_text)
#     jd_vector = model.encode(jd_text)
#     return get_similarity_score(cv_vector, jd_vector)
#
#
#
#--------------- After AI Reason----------------
import re
from sentence_transformers import SentenceTransformer
from app.utils import get_similarity_score

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Basic: returns only the AI similarity score
def get_match_score(cv_text, jd_text):
    cv_vector = model.encode(cv_text)
    jd_vector = model.encode(jd_text)
    return get_similarity_score(cv_vector, jd_vector)

# Advanced: returns both score + shortlisting reason
def extract_skills(text, skill_keywords):
    text = text.lower()
    matched = [skill for skill in skill_keywords if skill.lower() in text]
    return matched

def extract_years_experience(text):
    match = re.search(r'(\d+)\+?\s+years?', text.lower())
    return int(match.group(1)) if match else 0

def get_match_score_and_reason(cv_text, jd_text):
    cv_vector = model.encode(cv_text)
    jd_vector = model.encode(jd_text)
    score = get_similarity_score(cv_vector, jd_vector)

    # You can customize this list as needed
    skill_keywords = ['python', 'django', 'rest', 'api', 'git', 'docker', 'sql', 'html', 'flask', 'Java', 'Core Java', 'Spring boot', 'OOP', '.Net' ,'C#']
    skills = extract_skills(cv_text, skill_keywords)
    years = extract_years_experience(cv_text)
    print("years tolal-------",years)
    reason = f"Matched skills: {', '.join(skills) if skills else 'None found'}."
    if years:
        reason += f" Has approximately {years} years of experience."
    else:
        reason += " Experience duration not found."

    return round(score, 2), reason
