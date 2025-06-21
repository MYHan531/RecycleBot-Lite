#!/bin/bash
echo "Running MLflow tracking tests..."
echo "Make sure FastAPI server is running first!"
echo ""
python3 scripts/test_mlflow_tracking.py
