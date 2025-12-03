# Resume Analyzer Web Application

A complete full-stack web application that analyzes PDF resumes and provides detailed feedback with scores out of 10. Built with FastAPI (Python) backend and React + Vite frontend.

## 🚀 Features

- **PDF Resume Upload**: Upload and analyze PDF resumes
- **Section Detection**: Automatically detects Skills, Experience, Education, Projects, and more
- **Rule-Based Scoring**: Comprehensive scoring algorithm (10 points total)
  - Skills (2 points)
  - Experience (3 points)
  - Education (1 point)
  - Projects (2 points)
  - Formatting (2 points)
- **Detailed Feedback**: Provides strengths and areas for improvement
- **Modern UI**: Clean, responsive interface built with React and TailwindCSS
- **RESTful API**: FastAPI backend with proper error handling

## 📋 Tech Stack

### Backend
- **Python 3.11**
- **FastAPI** - Modern, fast web framework
- **pdfplumber** - PDF text extraction
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18**
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── analyzer.py          # Resume analysis logic
│   │   ├── models.py            # Pydantic models
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── pdf_extractor.py # PDF extraction utility
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_analyzer.py
│   │   └── test_pdf_extractor.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── Loader.jsx
│   │   │   ├── ScoreDashboard.jsx
│   │   │   └── FeedbackCards.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── Dockerfile
│   └── index.html
├── docker-compose.yml
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional, for containerized setup)

### Local Development Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Docker Setup

1. Build and start all services:
```bash
docker-compose up --build
```

2. Access the application:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

3. Stop services:
```bash
docker-compose down
```

## 📡 API Usage

### Analyze Resume

**Endpoint:** `POST /analyze`

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: PDF file (form field: `file`)

**Response:**
```json
{
  "score": 7.5,
  "sections": {
    "skills": 1.8,
    "experience": 2.5,
    "education": 0.8,
    "projects": 1.6,
    "formatting": 0.8
  },
  "strengths": [
    "Good variety of skills (12 skills listed)",
    "Strong technical skills with relevant technologies",
    "Multiple positions listed (2 positions)"
  ],
  "weaknesses": [
    "Consider using bullet points for better readability",
    "Add more quantifiable achievements (numbers, percentages, metrics)"
  ],
  "detected_sections": {
    "contact": true,
    "skills": true,
    "experience": true,
    "education": true,
    "projects": true,
    "certifications": false
  }
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

### Backend Tests

1. Install test dependencies:
```bash
cd backend
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Run tests with coverage:
```bash
pytest --cov=app tests/
```

## 📊 Scoring Algorithm

The analyzer uses a rule-based scoring system (no AI/LLM):

### Skills (2 points)
- Variety of skills (0.3-0.5 points)
- Relevant technical keywords (0.5-0.8 points)
- Organization/categorization (0.3-0.7 points)

### Experience (3 points)
- Number of positions (0.5-1.0 points)
- Quantifiable achievements (0.3-1.5 points)
- Action verbs (0.2-0.5 points)

### Education (1 point)
- Degree information (0.5 points)
- Institution name (0.3 points)
- Dates (0.2 points)

### Projects (2 points)
- Number of projects (0.4-1.0 points)
- Technical details (0.4-0.7 points)
- Links/references (0.3 points)

### Formatting (2 points)
- Bullet points (0.5 points)
- Appropriate length (0.4-0.7 points)
- Section organization (0.2-0.5 points)
- Contact information (0.3 points)

## 🐛 Error Handling

The application handles various error scenarios:
- Invalid file types (non-PDF)
- Corrupted or unreadable PDFs
- Empty files
- Image-based PDFs (no extractable text)
- Network errors

## 🔧 Configuration

### Environment Variables

**Frontend:**
- `VITE_API_URL` - Backend API URL (default: `http://localhost:8000`)

**Backend:**
- `PYTHONUNBUFFERED=1` - For Docker logging

## 📝 Development Notes

- The analyzer uses regex patterns and keyword matching (no LLM calls)
- All scoring is rule-based and deterministic
- The frontend uses TailwindCSS for styling
- CORS is configured to allow frontend-backend communication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with FastAPI and React
- PDF processing with pdfplumber
- UI styling with TailwindCSS

