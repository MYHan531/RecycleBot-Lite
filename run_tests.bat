@echo off
echo Running MLflow tracking tests...
echo Make sure FastAPI server is running first!
echo.
python scripts/test_mlflow_tracking.py
pause 