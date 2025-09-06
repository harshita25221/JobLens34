import docx
import spacy 
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from keybert import KeyBERT
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from spacy.lang.en.stop_words import STOP_WORDS
import pandas as pd
from flask_cors import CORS
from rapidfuzz import process, fuzz
import gc
import threading

app = Flask(__name__)
CORS(app)

# Lazy loading of NLP models
nlp = None
kw_model = None

# Thread-local storage for models
thread_local = threading.local()

# Function to get NLP model when needed
def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp

# Function to get KeyBERT model when needed
def get_keybert():
    global kw_model
    if kw_model is None:
        kw_model = KeyBERT()
    return kw_model

import openai
import os
import functools
openai.api_key = os.getenv("OPENAI_API_KEY")

# Lazy loading of skills data
skills_df = None
GLOBAL_SKILLS = None

@functools.lru_cache(maxsize=1)
def get_global_skills():
    global skills_df, GLOBAL_SKILLS
    if GLOBAL_SKILLS is None:
        skills_df = pd.read_csv("merged_skills.csv")
        GLOBAL_SKILLS = set(skills_df["skill"].dropna().str.lower().str.strip())
        # Free up memory
        skills_df = None
        gc.collect()
    return GLOBAL_SKILLS



def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        # Process paragraphs in batches to reduce memory usage
        text_parts = []
        batch_size = 50
        paragraphs = list(doc.paragraphs)
        
        for i in range(0, len(paragraphs), batch_size):
            batch = paragraphs[i:i+batch_size]
            text_parts.append("\n".join([para.text for para in batch]))
            # Free memory after each batch
            gc.collect()
        
        text = "\n".join(text_parts)
        # Clear references to free memory
        doc = None
        paragraphs = None
        text_parts = None
        gc.collect()
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_text_from_pdf(file):
    try:
        text_parts = []
        file_content = BytesIO(file.read())
        with pdfplumber.open(file_content) as pdf:
            # Process pages in batches
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                text_parts.append(page_text + "\n")
                
                # Free memory every few pages
                if i % 5 == 0:
                    gc.collect()
        
        text = "".join(text_parts)
        # Clear references to free memory
        text_parts = None
        file_content = None
        gc.collect()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+"," ", text)
    return text



def get_keywords(text, num_keywords=20):
    model = get_keybert()
    keywords = model.extract_keywords(
        text, keyphrase_ngram_range=(1, 3), 
        stop_words='english',
        top_n=num_keywords
    )
    result = [kw[0] for kw in keywords]
    # Force garbage collection after processing
    gc.collect()
    return result

def extract_spacy_skills(text):
    model = get_nlp()
    # Process text in smaller chunks if it's large
    if len(text) > 10000:
        chunks = [text[i:i+10000] for i in range(0, len(text), 10000)]
        skills = set()
        for chunk in chunks:
            doc = model(chunk)
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                    word = token.text.strip()
                    if word.lower() not in STOP_WORDS:
                        if word[0].isupper() or re.search(r"[A-Za-z0-9\+\#]", word):
                            skills.add(word)
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                    skills.add(ent.text.lower())
    else:
        doc = model(text)
        skills = set()
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                word = token.text.strip()
                if word.lower() not in STOP_WORDS:
                    if word[0].isupper() or re.search(r"[A-Za-z0-9\+\#]", word):
                        skills.add(word)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                skills.add(ent.text.lower())
    
    # Force garbage collection after processing
    gc.collect()
    return list(skills)

def normalize_skills_with_fuzzy(extracted_skills, global_skills, threshold=85):
    """ ✅ Use rapidfuzz to map extracted skills to closest taxonomy skills """
    normalized = set()
    # Process in smaller batches to reduce memory usage
    batch_size = 100
    for i in range(0, len(extracted_skills), batch_size):
        batch = extracted_skills[i:i+batch_size]
        for skill in batch:
            match = process.extractOne(skill, global_skills, scorer=fuzz.token_sort_ratio)
            if match and match[1] >= threshold:  
                normalized.add(match[0])
        # Force garbage collection after each batch
        gc.collect()
    return normalized

def extract_multiword_skills(text, global_skills):
    found = set()
    # Process in smaller batches to reduce memory usage
    text_lower = text.lower()
    batch_size = 500
    skills_list = list(global_skills)
    for i in range(0, len(skills_list), batch_size):
        batch = skills_list[i:i+batch_size]
        for skill in batch:
            if " " in skill and skill in text_lower:
                found.add(skill)
        # Force garbage collection after each batch
        gc.collect()
    return found



def get_combined_skills(text):
    # Get global skills using lazy loading
    global_skills = get_global_skills()
    
    # Extract skills in stages to manage memory
    kw_skills = set(get_keywords(text))
    gc.collect()  # Force garbage collection between stages
    
    spacy_skills = set(extract_spacy_skills(text))
    gc.collect()  # Force garbage collection between stages
    
    multiword_skills = extract_multiword_skills(text, global_skills)
    gc.collect()  # Force garbage collection between stages

    # Process in smaller steps
    all_extracted = {s.lower().strip() for s in kw_skills}
    all_extracted.update({s.lower().strip() for s in spacy_skills})
    all_extracted.update({s.lower().strip() for s in multiword_skills})
    
    # Clear intermediate results to free memory
    kw_skills = None
    spacy_skills = None
    multiword_skills = None
    gc.collect()

    # Convert to list for batch processing
    all_extracted_list = list(all_extracted)
    all_extracted = None  # Free memory
    gc.collect()
    
    filtered = normalize_skills_with_fuzzy(all_extracted_list, global_skills)
    
    return filtered



# -------------------- Scoring --------------------
def get_skills_and_score(resume_text, job_description, alpha=0.3):
    # Process in stages with memory cleanup between steps
    resume_skills = set(get_combined_skills(resume_text))
    gc.collect()  # Force garbage collection between stages
    
    job_req_skills = set(get_combined_skills(job_description))
    gc.collect()  # Force garbage collection between stages

    # Get stop words once
    stop_words = STOP_WORDS
    
    # Filter skills in batches
    filtered_resume_skills = set()
    for skill in resume_skills:
        if skill not in stop_words and len(skill) > 2:
            filtered_resume_skills.add(skill)
    
    # Free memory
    resume_skills = None
    gc.collect()
    
    filtered_job_skills = set()
    for skill in job_req_skills:
        if skill not in stop_words and len(skill) > 2:
            filtered_job_skills.add(skill)
    
    # Reassign to original variable names for clarity
    resume_skills = filtered_resume_skills
    job_req_skills = filtered_job_skills
    
    # Free memory
    filtered_resume_skills = None
    filtered_job_skills = None
    gc.collect()

    if not resume_skills or not job_req_skills:
        return 0.0, [], [], 0.0

    # Calculate overlap
    overlap_skills = resume_skills.intersection(job_req_skills)
    overlap = len(overlap_skills) / len(job_req_skills) if job_req_skills else 0

    # Use smaller text representations for vectorization
    resume_text_for_vec = " ".join(list(resume_skills)[:500])  # Limit to 500 skills max
    job_text_for_vec = " ".join(list(job_req_skills)[:500])  # Limit to 500 skills max
    
    # Vectorize with memory optimization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text_for_vec, job_text_for_vec])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except Exception:
        # Fallback if vectorization fails due to memory
        cosine_sim = overlap  # Use overlap as approximation
    
    # Free memory
    vectorizer = None
    tfidf_matrix = None
    resume_text_for_vec = None
    job_text_for_vec = None
    gc.collect()

    final_score = (alpha * cosine_sim + (1 - alpha) * overlap) * 100

    # Calculate differences
    missing_skills = sorted(list(job_req_skills - resume_skills))[:100]  # Limit to top 100
    highlighted_skills = sorted(list(overlap_skills))[:100]  # Limit to top 100
    
    # Final cleanup
    resume_skills = None
    job_req_skills = None
    overlap_skills = None
    gc.collect()

    return final_score, missing_skills, highlighted_skills, cosine_sim



def generate_ai_text(prompt: str) -> str:
    # Truncate prompt if too long to reduce memory usage
    max_prompt_length = 4000
    if len(prompt) > max_prompt_length:
        prompt = prompt[:max_prompt_length]
        
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are an AI-powered career coach that analyzes resumes and job descriptions, rewrites resumes for better alignment, crafts tailored cover letters, and provides suggestions to maximize a candidate's chances of getting hired."},
                {"role": "user", "content": prompt}
            ], 
            max_tokens=500,
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        # Free memory
        response = None
        gc.collect()
        return result
    except Exception as e:
        print(f"Error in generate_ai_text: {str(e)}")
        return "Error generating content. Please try again with a smaller file."

def generate_tailored_resume(resume_text, job_description):
    # Truncate inputs if they're too long to reduce memory usage
    max_length = 3000
    resume_text = resume_text[:max_length] if len(resume_text) > max_length else resume_text
    job_description = job_description[:max_length] if len(job_description) > max_length else job_description
    
    prompt = f"""
    Resume: \n{resume_text}\n
    Job description: \n{job_description}\n
    Rewrite the resume so it better matches the job description.
    Focus on aligning skills, experience, and phrasing with the job description while keeping authenticity.
    """
    result = generate_ai_text(prompt)
    # Free memory
    prompt = None
    gc.collect()
    return result

def generate_cover_letter(resume_text, job_description):
    # Truncate inputs if they're too long to reduce memory usage
    max_length = 2500
    resume_text = resume_text[:max_length] if len(resume_text) > max_length else resume_text
    job_description = job_description[:max_length] if len(job_description) > max_length else job_description
    
    prompt = f"""
    Write a professional cover letter tailored to the following job description: \n{job_description}\n
    Resume content: \n{resume_text}\n
    Make it concise, skill-focused, and role-specific."""
    result = generate_ai_text(prompt)
    # Free memory
    prompt = None
    gc.collect()
    return result

import re 

def generate_suggestions(resume_text, job_description, cosine_sim, missing_skills):
    # Truncate inputs if they're too long to reduce memory usage
    max_length = 2000
    resume_text = resume_text[:max_length] if len(resume_text) > max_length else resume_text
    job_description = job_description[:max_length] if len(job_description) > max_length else job_description
    
    # Limit number of missing skills to include in prompt
    missing_skills_text = ', '.join(missing_skills[:10]) if missing_skills else 'None'
    
    prompt = f"""
    You are an expert career coach. 
    A candidate has a resume and is applying for this job description.
    Their resume-Job description match score is {round(cosine_sim*100,2)}%
    Missing Skills: {missing_skills_text}

    Provide a numbered list of 3-5 clear, practical suggestions.
    Each suggestion must be on a new line.
    """
    
    response_text = generate_ai_text(prompt)
    
    suggestions_list = [
        re.sub(r'^\d+\.\s*', '', line).strip() 
        for line in response_text.split('\n') 
        if line.strip()
    ]
    
    # Free memory
    prompt = None
    response_text = None
    gc.collect()
    
    return suggestions_list



@app.route("/")
def index():  
    return jsonify({"status": "healthy", "message": "JobLens API is running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "message": "JobLens API is running"})

@app.route("/analyze", methods=["POST"])  
def analyze():  
    try:
        resume_file = request.files.get("resume")  
        jd_file = request.files.get("job_description")
        if not resume_file or not jd_file:
            return jsonify({"error": "Please upload both resume and job description files."})  

        # Process resume file
        if resume_file.filename.endswith(".docx"):
            resume_raw = extract_text_from_docx(resume_file)
        elif resume_file.filename.endswith(".pdf"):
            resume_raw = extract_text_from_pdf(resume_file)
        else:
            return jsonify({"error": "Unsupported resume file format."})  
        
        resume_clean = clean_text(resume_raw)
        resume_raw = None  # Free memory
        gc.collect()

        # Process job description file
        if jd_file.filename.endswith(".docx"):
            jd_raw = extract_text_from_docx(jd_file)
        elif jd_file.filename.endswith(".pdf"):
            jd_raw = extract_text_from_pdf(jd_file)
        else:
            return jsonify({"error": "Unsupported job description file format."})  

        jd_clean = clean_text(jd_raw)
        jd_raw = None  # Free memory
        gc.collect()

        # Get skills and score
        final_score, missing_skills, highlighted_skills, cosine_sim = get_skills_and_score(resume_clean, jd_clean)
        gc.collect()

        # Generate AI content one at a time to reduce memory usage
        tailored_resume = generate_tailored_resume(resume_clean, jd_clean)
        gc.collect()
        
        cover_letter = generate_cover_letter(resume_clean, jd_clean)
        gc.collect()
        
        suggestions = generate_suggestions(resume_clean, jd_clean, cosine_sim, missing_skills)
        gc.collect()

        # Clear large text variables
        resume_clean = None
        jd_clean = None
        gc.collect()

        return jsonify({  
            "match_score": round(final_score,2),
            "missing_skills": missing_skills[:100],  # Limit array size
            "highlighted_skills": highlighted_skills[:100],  # Limit array size
            "tailored_resume": tailored_resume,
            "cover_letter": cover_letter,
            "suggestions": suggestions
        })
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": "An error occurred during analysis. Try with smaller files or contact support."}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
