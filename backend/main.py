from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import analyze_resume

app = FastAPI(title="AI Resume-Job Match Engine")

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/analyze")
def analyze(data: ResumeRequest):
    result = analyze_resume(data.resume_text, data.job_description)
    return result

@app.get("/")
def home():
    return {"message": "AI Resume Matcher Running 🚀"}