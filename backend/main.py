from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import analyze_resume

app = FastAPI(title="AI Resume-Job Match Engine")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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