"""
Pydantic models for the Resume Analyzer API.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class SectionScores(BaseModel):
    """Scores for each section of the resume."""
    skills: float = Field(..., ge=0, le=2, description="Skills section score (0-2)")
    experience: float = Field(..., ge=0, le=3, description="Experience section score (0-3)")
    education: float = Field(..., ge=0, le=1, description="Education section score (0-1)")
    projects: float = Field(..., ge=0, le=2, description="Projects section score (0-2)")
    formatting: float = Field(..., ge=0, le=2, description="Formatting score (0-2)")


class AnalysisResponse(BaseModel):
    """Response model for resume analysis."""
    score: float = Field(..., ge=0, le=10, description="Total score out of 10")
    sections: SectionScores = Field(..., description="Individual section scores")
    strengths: List[str] = Field(..., description="List of strengths identified")
    weaknesses: List[str] = Field(..., description="List of weaknesses identified")
    detected_sections: Dict[str, bool] = Field(..., description="Which sections were detected")
    ats_readiness: int = Field(
        ...,
        ge=0,
        le=100,
        description="Approximate ATS-readiness score (0-100, higher is better)",
    )
    field: Optional[str] = Field(
        None,
        description="Detected primary field of study/work (e.g., 'software / it', 'data / ai')",
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")

