# Quick Start Guide

## 🚀 Fastest Way to Get Started

### Option 1: Docker Compose (Recommended)

1. **Start everything:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Stop everything:**
   ```bash
   docker-compose down
   ```

### Option 2: Local Development

#### Backend (Terminal 1)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

## 📝 Testing

### Backend Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

## 🐛 Troubleshooting

### Backend won't start
- Make sure Python 3.11+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

### Frontend won't start
- Make sure Node.js 18+ is installed
- Run `npm install` in the frontend directory
- Check that port 5173 is not in use

### PDF upload fails
- Ensure the file is a valid PDF
- Check that the PDF contains extractable text (not just images)
- Verify backend is running and accessible

### CORS errors
- Make sure backend CORS is configured correctly
- Check that frontend is using the correct API URL
- Verify both services are running

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check API documentation at http://localhost:8000/docs
- Review the scoring algorithm in `backend/app/analyzer.py`

