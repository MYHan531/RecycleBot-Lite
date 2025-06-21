# NEA RAG System - MLOps Integration

This document describes the MLOps integration for the NEA Waste Management RAG System, including FastAPI, MLflow tracking, DVC data versioning, and CRM-like logging.

## 🚀 Quick Start

### 1. Complete Setup
```bash
# Run the complete MLOps setup
python scripts/setup_mlops.py
```

### 2. Start Services
```bash
# Terminal 1: Start FastAPI server
python scripts/fastapi_rag.py

# Terminal 2: Start MLflow UI
mlflow ui

# Terminal 3: Run test questions
python scripts/test_mlflow_tracking.py
```

### 3. Access Interfaces
- **FastAPI Docs**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **Health Check**: http://localhost:8000/health

## 📊 MLOps Components

### FastAPI Integration
The system now includes a complete FastAPI application (`fastapi_rag.py`) that:

- **Integrates RAG System**: Uses the existing `NEARAGSystem` class
- **CRM Logging**: Logs every chat interaction to `cases.json`
- **MLflow Tracking**: Tracks metrics for each interaction
- **RESTful API**: Provides clean HTTP endpoints
- **Auto-documentation**: Interactive API docs at `/docs`

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Main chat endpoint with CRM logging |
| `/health` | GET | System health check |
| `/metrics` | GET | System performance metrics |
| `/test-questions` | GET | Get predefined test questions |

#### Example Chat Request
```json
{
  "question": "What is the total waste generated in Singapore in 2023?",
  "user_id": "user123",
  "session_id": "session456",
  "metadata": {
    "source": "web_interface",
    "timestamp": "2025-01-21T10:00:00Z"
  }
}
```

#### Example Chat Response
```json
{
  "question": "What is the total waste generated in Singapore in 2023?",
  "answer": "According to the 2023 waste statistics...",
  "sources": ["annual_data_2023.md", "key_highlights_2023.md"],
  "session_id": "session456",
  "request_id": "uuid-1234-5678-9abc",
  "latency_ms": 1250.5,
  "token_count": 45,
  "retrieval_score": 0.667,
  "timestamp": "2025-01-21T10:00:01Z"
}
```

### MLflow Tracking
MLflow is configured to track:

- **Latency**: Response time in milliseconds
- **Token Count**: Estimated tokens (question + answer)
- **Retrieval Score**: Normalized score based on sources found
- **Question Length**: Number of characters in question
- **User/Session IDs**: For user tracking
- **Artifacts**: Complete chat data as JSON files

#### MLflow Setup
```python
# SQLite backend for local development
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nea_rag_system")
```

#### Viewing Experiments
1. Start MLflow UI: `mlflow ui`
2. Open browser: http://localhost:5000
3. Navigate to experiments and runs
4. View metrics, parameters, and artifacts

### DVC Data Versioning
DVC is used to version the raw data:

```bash
# Initialize DVC
dvc init

# Add raw data to versioning
dvc add data/raw

# Commit DVC files
git add data/raw.dvc .dvc
git commit -m "Add raw docs with DVC"
```

#### DVC Commands
```bash
# Check status
dvc status

# List tracked files
dvc list .

# Update data
dvc add data/raw
git add data/raw.dvc
git commit -m "Update data"
```

### CRM Logging
Every chat interaction is logged to `cases.json` with:

- **Request ID**: Unique identifier for each request
- **Session ID**: User session tracking
- **User ID**: User identification
- **Question/Answer**: Complete conversation
- **Performance Metrics**: Latency, tokens, retrieval score
- **Timestamp**: ISO format timestamp
- **Metadata**: Additional context

#### Example CRM Log Entry
```json
{
  "request_id": "uuid-1234-5678-9abc",
  "session_id": "session456",
  "user_id": "user123",
  "question": "What is the total waste generated in Singapore in 2023?",
  "answer": "According to the 2023 waste statistics...",
  "sources": ["annual_data_2023.md", "key_highlights_2023.md"],
  "latency_ms": 1250.5,
  "token_count": 45,
  "retrieval_score": 0.667,
  "timestamp": "2025-01-21T10:00:01Z",
  "metadata": {
    "source": "web_interface",
    "test_run": false
  }
}
```

## 🧪 Testing

### Automated Test Questions
The system includes 5 predefined test questions:

1. "What is the total waste generated in Singapore in 2023?"
2. "How much of the waste was recycled in 2023?"
3. "What are the key highlights of waste management in Singapore?"
4. "What is the recycling rate for different waste streams?"
5. "How has waste generation changed over the years?"

### Running Tests
```bash
# Run automated tests
python scripts/test_mlflow_tracking.py

# View results
cat mlflow_test_results.json
```

### Test Results
Tests generate:
- **Console Output**: Real-time test progress
- **MLflow Runs**: Individual runs for each question
- **CRM Logs**: All interactions logged to `cases.json`
- **Summary Report**: `mlflow_test_results.json` with statistics

## 📈 Metrics and Monitoring

### Key Metrics Tracked
- **Latency**: Average response time
- **Token Count**: Average tokens per interaction
- **Retrieval Score**: Average retrieval quality
- **Success Rate**: Percentage of successful responses
- **Source Count**: Average number of sources retrieved

### Monitoring Endpoints
```bash
# System health
curl http://localhost:8000/health

# Performance metrics
curl http://localhost:8000/metrics
```

### Example Metrics Response
```json
{
  "total_interactions": 25,
  "avg_latency_ms": 1200.5,
  "avg_token_count": 42.3,
  "avg_retrieval_score": 0.75
}
```

## 🔧 Setup Scripts

### Complete Setup
```bash
python scripts/setup_mlops.py
```

This script:
- Checks and installs dependencies
- Sets up DVC and MLflow
- Creates necessary directories
- Generates startup scripts
- Provides comprehensive instructions

### Individual Setup Scripts
```bash
# DVC setup only
python scripts/setup_dvc.py

# Start FastAPI
bash start_fastapi.sh

# Start MLflow UI
bash start_mlflow.sh

# Run tests
bash run_tests.sh
```

## 📁 File Structure

```
RecycleBot-Lite/
├── fastapi_rag.py              # Main FastAPI application
├── test_mlflow_tracking.py     # MLflow testing script
├── setup_mlops.py              # Complete MLOps setup
├── setup_dvc.py                # DVC setup script
├── start_fastapi.sh            # FastAPI startup script
├── start_mlflow.sh             # MLflow UI startup script
├── run_tests.sh                # Test execution script
├── cases.json                  # CRM interaction logs
├── mlflow.db                   # MLflow SQLite database
├── mlflow_test_results.json    # Test results summary
├── .dvc/                       # DVC configuration
├── data/
│   ├── raw/                    # Raw scraped data (versioned)
│   └── raw.dvc                 # DVC tracking file
└── logs/                       # Application logs
```

## 🚀 Production Deployment

### Environment Variables
```bash
# Optional: Set custom MLflow tracking URI
export MLFLOW_TRACKING_URI="sqlite:///mlflow.db"

# Optional: Set custom FastAPI host/port
export FASTAPI_HOST="0.0.0.0"
export FASTAPI_PORT="8000"
```

### Docker Deployment (Future)
```dockerfile
# Example Dockerfile for production
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "fastapi_rag:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Monitoring in Production
- **Health Checks**: `/health` endpoint for load balancers
- **Metrics**: `/metrics` endpoint for monitoring systems
- **Logs**: Structured logging to `cases.json`
- **MLflow**: Centralized experiment tracking
- **DVC**: Data lineage and versioning

## 🔍 Troubleshooting

### Common Issues

1. **FastAPI Server Won't Start**
   ```bash
   # Check if RAG system is initialized
   python -c "from rag_system import NEARAGSystem; NEARAGSystem()"
   ```

2. **MLflow UI Not Accessible**
   ```bash
   # Check if MLflow is running
   curl http://localhost:5000
   
   # Restart MLflow UI
   mlflow ui --host 0.0.0.0 --port 5000
   ```

3. **DVC Issues**
   ```bash
   # Reinitialize DVC
   dvc init
   
   # Check DVC status
   dvc status
   ```

4. **Missing Dependencies**
   ```bash
   # Install all dependencies
   pip install -r requirements.txt
   ```

### Log Files
- **Application Logs**: Check console output
- **CRM Logs**: `cat cases.json`
- **MLflow Logs**: Check MLflow UI
- **DVC Logs**: `dvc status`

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [DVC Documentation](https://dvc.org/doc)
- [NEA RAG System README](README_RAG.md)

## 🤝 Contributing

When adding new features:

1. **Update Dependencies**: Add to `requirements.txt`
2. **Add Tests**: Include in `test_mlflow_tracking.py`
3. **Update Documentation**: Modify this README
4. **Version Data**: Use DVC for new data files
5. **Track Experiments**: Use MLflow for new metrics

---

This MLOps integration provides a complete, production-ready system with full observability, data versioning, and experiment tracking capabilities. 