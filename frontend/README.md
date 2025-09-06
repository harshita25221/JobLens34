# JobLens – AI-Powered Resume Rater

## Overview
**JobLens** is an AI-driven web application designed to help job seekers optimize their resumes and increase their chances of getting shortlisted. The platform analyzes a resume against a target job description (JD), highlights missing skills, computes a relevance score, and provides actionable improvement suggestions. It also assists recruiters with faster pre-screening tools.

---

## Features

### Core Features
- **Resume & JD Upload:** Upload PDF/DOCX resumes and paste or upload JDs.
- **Keyword Extraction:** Extract skills, entities, and relevant terms from both resumes and JDs using NLP.
- **Similarity Scoring:** Compute match score using TF-IDF and cosine similarity.
- **Missing Skill Highlighting:** Identify skills or keywords present in JD but missing in the resume.
- **Improvement Suggestions:** Provide actionable recommendations for optimizing resumes.
- **Visual Dashboard:** Charts and highlights for keyword coverage and alignment.

### Benefits
- ⏳ **Time-Saving:** Get instant resume feedback.
- 🎯 **Improved Shortlisting:** Tailor resumes to match recruiter expectations.
- 📊 **Recruiter Utility:** Use as a pre-screening filter to rank candidates.
- 🌐 **Accessible:** Free, lightweight, and user-friendly interface.

---

## Tech Stack

- **Frontend:** React + Tailwind CSS, Recharts for visualizations.
- **Backend:** FastAPI (Python) with CORS enabled for frontend-backend integration.
- **AI/NLP:**
  - spaCy → Named Entity Recognition (skills, roles, education)
  - KeyBERT → Keyword extraction
  - TF-IDF + Cosine Similarity → Relevance scoring
- **File Handling:** pdfplumber (PDF) and python-docx (DOCX)
- **Database (Optional):** SQLite/PostgreSQL for storing user history and analytics.

---

## Architecture

**Workflow:**
1. User uploads resume (PDF/DOCX) and JD.
2. Backend extracts text from files.
3. NLP pipeline identifies skills, keywords, and entities.
4. Scoring engine calculates similarity score.
5. Improvement suggestions highlight missing or weakly represented skills.
6. Results returned as JSON for frontend visualization (charts, progress bars, highlights).


## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

```bash
# Clone the repository
git clone https://github.com/yourusername/JobLens.git

# Navigate to frontend directory
cd JobLens/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Deployment

For detailed deployment instructions, please refer to the [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) in the root directory.

### Quick Deployment Options

**Frontend:**
- Deploy to Netlify or Vercel using the configuration files provided

**Backend:**
- Deploy to Heroku, Railway, or any platform supporting Python applications

See the deployment guide for step-by-step instructions.
