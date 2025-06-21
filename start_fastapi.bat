@echo off
echo Starting FastAPI RAG Server...
echo MLflow UI will be available at: http://localhost:5000
echo FastAPI docs will be available at: http://localhost:8000/docs
echo.
python scripts/fastapi_rag.py
pause 