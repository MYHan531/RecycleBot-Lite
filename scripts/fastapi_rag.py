#!/usr/bin/env python3
"""
FastAPI RAG System with MLflow Tracking and CRM Integration
"""

import json
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mlflow
import mlflow.tracking

# Import our RAG system
from rag_system import NEARAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NEA Waste Management RAG API",
    description="FastAPI interface for NEA waste management question answering with MLflow tracking",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    session_id: str
    request_id: str
    latency_ms: float
    token_count: Optional[int] = None
    retrieval_score: Optional[float] = None
    timestamp: str

# Initialize MLflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nea_rag_system")

# Initialize RAG system
rag_system = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    try:
        rag_system = NEARAGSystem()
        logger.info("✅ RAG system initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG system: {e}")
        raise

def log_to_crm(chat_data: Dict[str, Any]):
    """Log chat interaction to CRM-like system"""
    try:
        with open("cases.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(chat_data, ensure_ascii=False) + "\n")
        logger.info(f"✅ Logged chat interaction to CRM: {chat_data['request_id']}")
    except Exception as e:
        logger.error(f"❌ Error logging to CRM: {e}")

def track_metrics_with_mlflow(chat_data: Dict[str, Any]):
    """Track metrics with MLflow"""
    try:
        with mlflow.start_run(run_name=f"chat_{chat_data['request_id']}", nested=True):
            # Log parameters
            mlflow.log_param("question_length", len(chat_data['question']))
            mlflow.log_param("user_id", chat_data.get('user_id', 'anonymous'))
            mlflow.log_param("session_id", chat_data['session_id'])
            
            # Log metrics
            mlflow.log_metric("latency_ms", chat_data['latency_ms'])
            if chat_data.get('token_count'):
                mlflow.log_metric("token_count", chat_data['token_count'])
            if chat_data.get('retrieval_score'):
                mlflow.log_metric("retrieval_score", chat_data['retrieval_score'])
            
            # Log artifacts
            mlflow.log_dict(chat_data, f"chat_data_{chat_data['request_id']}.json")
            
        logger.info(f"✅ Tracked metrics with MLflow: {chat_data['request_id']}")
    except Exception as e:
        logger.error(f"❌ Error tracking with MLflow: {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Main chat endpoint with CRM logging and MLflow tracking"""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    start_time = time.time()
    request_id = str(uuid.uuid4())
    session_id = req.session_id or str(uuid.uuid4())
    
    try:
        # Get answer from RAG system
        result = rag_system.ask_question(req.question)
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Estimate token count (rough approximation)
        token_count = len(req.question.split()) + len(result['answer'].split())
        
        # Calculate retrieval score (simplified - based on number of sources)
        retrieval_score = len(result['sources']) / 3.0 if result['sources'] else 0.0
        
        # Prepare response
        response = ChatResponse(
            question=req.question,
            answer=result['answer'],
            sources=result['sources'],
            session_id=session_id,
            request_id=request_id,
            latency_ms=latency_ms,
            token_count=token_count,
            retrieval_score=retrieval_score,
            timestamp=datetime.now().isoformat()
        )
        
        # Prepare CRM data
        crm_data = {
            "request_id": request_id,
            "session_id": session_id,
            "user_id": req.user_id or "anonymous",
            "question": req.question,
            "answer": result['answer'],
            "sources": result['sources'],
            "latency_ms": latency_ms,
            "token_count": token_count,
            "retrieval_score": retrieval_score,
            "timestamp": response.timestamp,
            "metadata": req.metadata or {}
        }
        
        # Log to CRM and track with MLflow
        log_to_crm(crm_data)
        track_metrics_with_mlflow(crm_data)
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_system_ready": rag_system is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    try:
        # Read CRM data to calculate metrics
        metrics = {
            "total_interactions": 0,
            "avg_latency_ms": 0,
            "avg_token_count": 0,
            "avg_retrieval_score": 0
        }
        
        latencies = []
        token_counts = []
        retrieval_scores = []
        
        try:
            with open("cases.json", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        latencies.append(data.get('latency_ms', 0))
                        token_counts.append(data.get('token_count', 0))
                        retrieval_scores.append(data.get('retrieval_score', 0))
        except FileNotFoundError:
            pass
        
        if latencies:
            metrics["total_interactions"] = len(latencies)
            metrics["avg_latency_ms"] = sum(latencies) / len(latencies)
            metrics["avg_token_count"] = sum(token_counts) / len(token_counts)
            metrics["avg_retrieval_score"] = sum(retrieval_scores) / len(retrieval_scores)
        
        return metrics
        
    except Exception as e:
        logger.error(f"❌ Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-questions")
async def get_test_questions():
    """Get predefined test questions for evaluation"""
    return {
        "test_questions": [
            "What is the total waste generated in Singapore in 2023?",
            "How much of the waste was recycled in 2023?",
            "What are the key highlights of waste management in Singapore?",
            "What is the recycling rate for different waste streams?",
            "How has waste generation changed over the years?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 