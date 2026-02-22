from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from PyPDF2 import PdfReader
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def extract_keywords(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]

def detect_sections(text):
    sections = []
    lower = text.lower()

    if "project" in lower:
        sections.append("Projects")
    if "experience" in lower:
        sections.append("Experience")
    if "education" in lower:
        sections.append("Education")
    if "skill" in lower:
        sections.append("Skills")

    missing_sections = list(set(["Projects","Experience","Education","Skills"]) - set(sections))
    return missing_sections

def analyze_resume(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # TF-IDF Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    overall_score = round(similarity * 100, 2)

    # NLP Keyword Extraction
    job_keywords = set(extract_keywords(job_description))
    resume_keywords = set(extract_keywords(resume_text))

    missing_keywords = list(job_keywords - resume_keywords)

    # Category Scoring
    tech_keywords = {"python","java","react","node","fastapi","sql","aws","docker","machine","learning"}
    tools_keywords = {"git","github","docker","aws","linux","jira"}
    soft_keywords = {"communication","teamwork","leadership","collaboration"}

    def category_score(category_set):
        matched = len(category_set & resume_keywords)
        total = len(category_set & job_keywords) or 1
        return round((matched/total)*100,2)

    tech_score = category_score(tech_keywords)
    tools_score = category_score(tools_keywords)
    soft_score = category_score(soft_keywords)

    # Smarter Suggestions
    if overall_score >= 75:
        suggestion = "Excellent match. Try adding measurable achievements for stronger impact."
    elif overall_score >= 50:
        suggestion = "Good match. Improve by adding more job-specific keywords."
    else:
        suggestion = "Low match. Align resume skills closely with job description."

    # Section Detection
    missing_sections = detect_sections(resume_text)

    return {
        "match_score": overall_score,
        "tech_score": tech_score,
        "tools_score": tools_score,
        "soft_score": soft_score,
        "match_strength": "Strong 🟢" if overall_score > 75 else "Moderate 🟡" if overall_score >= 50 else "Weak 🔴",
        "missing_keywords": missing_keywords[:10],
        "missing_sections": missing_sections,
        "suggestion": suggestion
    }