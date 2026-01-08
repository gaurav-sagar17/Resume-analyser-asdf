"""
FastAPI application for Resume Analyzer.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.models import AnalysisResponse
from app.analyzer import ResumeAnalyzer
from app.utils.pdf_extractor import extract_text_from_pdf_bytes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="Analyze resumes and provide scores and feedback",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://resume-analyser-asdf-3.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Resume Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "POST /analyze - Upload and analyze a PDF resume"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze a PDF resume and return scores and feedback.
    IMPORTANT:
    We ignore file.filename completely because Windows adds characters like ?\ that break Python.
    We validate using file.content_type instead.
    """

    # SAFEST validation
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed."
        )

    try:
        # Read file content into memory
        file_content = await file.read()

        if len(file_content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        # Extract text from PDF bytes only
        logger.info("Extracting text from uploaded PDF")
        text = extract_text_from_pdf_bytes(file_content)

        if not text or len(text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract enough text. This PDF may be image-based or corrupted."
            )

        # Analyze resume
        logger.info("Analyzing resume...")
        analyzer = ResumeAnalyzer(text)
        analysis_result = analyzer.analyze()

        return AnalysisResponse(**analysis_result)

    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the resume: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
