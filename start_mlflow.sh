#!/bin/bash
echo "Starting MLflow UI..."
echo "MLflow UI will be available at: http://localhost:5000"
echo ""
mlflow ui --host 0.0.0.0 --port 5000
