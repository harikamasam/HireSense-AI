from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from ai_engine import analyze_resume

app = FastAPI(title="HireSense AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.post("/analyze")
async def analyze(
    job_description: str = Form(None),
    resume_file: UploadFile = File(None),
    resume_text: str = Form(None)
):
    if not job_description:
        return {"error": "Job description is required"}

    if resume_file:
        resume_content = extract_text_from_pdf(resume_file.file)
    elif resume_text:
        resume_content = resume_text
    else:
        return {"error": "Resume text or file is required"}

    result = analyze_resume(resume_content, job_description)
    return result

@app.get("/")
def home():
    return {"message": "HireSense AI Running 🚀"}