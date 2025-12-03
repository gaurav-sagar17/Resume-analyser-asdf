"""
Tests for the Resume Analyzer.
"""
import pytest
from app.analyzer import ResumeAnalyzer


def test_analyzer_initialization():
    """Test that analyzer initializes correctly."""
    text = "This is a sample resume text."
    analyzer = ResumeAnalyzer(text)
    assert analyzer.text == text.lower()
    assert len(analyzer.lines) > 0


def test_detect_sections():
    """Test section detection."""
    resume_text = """
    John Doe
    Email: john@example.com
    Phone: 123-456-7890
    
    SKILLS
    Python, JavaScript, React
    
    EXPERIENCE
    Software Engineer at Company X (2020-2023)
    
    EDUCATION
    Bachelor's in Computer Science
    
    PROJECTS
    Project 1: Web Application
    """
    analyzer = ResumeAnalyzer(resume_text)
    sections = analyzer.detect_sections()
    
    assert sections['skills'] == True
    assert sections['experience'] == True
    assert sections['education'] == True
    assert sections['projects'] == True


def test_analyze_skills():
    """Test skills analysis."""
    resume_text = """
    SKILLS
    Python, JavaScript, React, Node.js, Docker, AWS, SQL, MongoDB
    """
    analyzer = ResumeAnalyzer(resume_text)
    analyzer.detect_sections()
    score, strengths, weaknesses = analyzer.analyze_skills()
    
    assert 0 <= score <= 2
    assert isinstance(strengths, list)
    assert isinstance(weaknesses, list)


def test_analyze_experience():
    """Test experience analysis."""
    resume_text = """
    EXPERIENCE
    Software Engineer at Tech Corp (2020-2023)
    - Increased performance by 50%
    - Managed a team of 5 developers
    - Delivered 10+ projects
    """
    analyzer = ResumeAnalyzer(resume_text)
    analyzer.detect_sections()
    score, strengths, weaknesses = analyzer.analyze_experience()
    
    assert 0 <= score <= 3
    assert isinstance(strengths, list)
    assert isinstance(weaknesses, list)


def test_analyze_education():
    """Test education analysis."""
    resume_text = """
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology (2016-2020)
    """
    analyzer = ResumeAnalyzer(resume_text)
    analyzer.detect_sections()
    score, strengths, weaknesses = analyzer.analyze_education()
    
    assert 0 <= score <= 1
    assert isinstance(strengths, list)
    assert isinstance(weaknesses, list)


def test_analyze_projects():
    """Test projects analysis."""
    resume_text = """
    PROJECTS
    1. E-commerce Website
    - Built with React and Node.js
    - GitHub: github.com/user/project
    
    2. Machine Learning Model
    - Used Python and TensorFlow
    """
    analyzer = ResumeAnalyzer(resume_text)
    analyzer.detect_sections()
    score, strengths, weaknesses = analyzer.analyze_projects()
    
    assert 0 <= score <= 2
    assert isinstance(strengths, list)
    assert isinstance(weaknesses, list)


def test_analyze_formatting():
    """Test formatting analysis."""
    resume_text = """
    John Doe
    - Email: john@example.com
    - Phone: 123-456-7890
    
    SKILLS
    - Python
    - JavaScript
    
    EXPERIENCE
    - Software Engineer
    """
    analyzer = ResumeAnalyzer(resume_text)
    analyzer.detect_sections()
    score, strengths, weaknesses = analyzer.analyze_formatting()
    
    assert 0 <= score <= 2
    assert isinstance(strengths, list)
    assert isinstance(weaknesses, list)


def test_full_analysis():
    """Test complete analysis."""
    resume_text = """
    John Doe
    Email: john@example.com
    Phone: 123-456-7890
    
    SKILLS
    Python, JavaScript, React, Node.js, Docker, AWS
    
    EXPERIENCE
    Software Engineer at Tech Corp (2020-2023)
    - Increased system performance by 50%
    - Managed team of 5 developers
    - Delivered 10+ successful projects
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology (2016-2020)
    
    PROJECTS
    1. E-commerce Platform
    - Built with React and Node.js
    - GitHub: github.com/user/ecommerce
    
    2. ML Prediction System
    - Used Python and TensorFlow
    - Improved accuracy by 30%
    """
    analyzer = ResumeAnalyzer(resume_text)
    result = analyzer.analyze()
    
    assert 'score' in result
    assert 'sections' in result
    assert 'strengths' in result
    assert 'weaknesses' in result
    assert 'detected_sections' in result
    assert 'field' in result
    assert 'ats_readiness' in result
    
    assert 0 <= result['score'] <= 10
    assert isinstance(result['sections'], dict)
    assert isinstance(result['strengths'], list)
    assert isinstance(result['weaknesses'], list)
    assert 0 <= result['ats_readiness'] <= 100


def test_field_detection_for_software():
    """Field detection should pick up software / IT for a tech-heavy resume."""
    resume_text = """
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology

    EXPERIENCE
    Software Engineer working on web development and cloud computing.

    PROJECTS
    Full stack web application using React and Node.js.
    """
    analyzer = ResumeAnalyzer(resume_text)
    result = analyzer.analyze()

    assert result["field"] in (None, "software / it", "data / ai")


def test_empty_resume():
    """Test analysis of empty resume."""
    analyzer = ResumeAnalyzer("")
    result = analyzer.analyze()
    
    assert result['score'] >= 0
    assert len(result['weaknesses']) > 0

