#!/usr/bin/env python3
"""
Test MLflow Tracking with Five Test Questions
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Add parent directory to path to import rag_system if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# FastAPI server URL
API_BASE_URL = "http://localhost:8000"

# Test questions
TEST_QUESTIONS = [
    "What is the total waste generated in Singapore in 2023?",
    "How much of the waste was recycled in 2023?",
    "What are the key highlights of waste management in Singapore?",
    "What is the recycling rate for different waste streams?",
    "How has waste generation changed over the years?"
]

def test_question(question: str, question_num: int):
    """Test a single question and return metrics"""
    print(f"\n--- Testing Question {question_num}: {question} ---")
    
    # Prepare request
    payload = {
        "question": question,
        "user_id": "test_user",
        "session_id": "test_session_001",
        "metadata": {
            "test_run": True,
            "question_number": question_num
        }
    }
    
    try:
        # Make request
        start_time = time.time()
        response = requests.post(f"{API_BASE_URL}/chat", json=payload)
        request_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"[OK] Success!")
            print(f"   Answer: {result['answer'][:100]}...")
            print(f"   Sources: {len(result['sources'])} documents")
            print(f"   Latency: {result['latency_ms']:.2f} ms")
            print(f"   Token Count: {result['token_count']}")
            print(f"   Retrieval Score: {result['retrieval_score']:.3f}")
            print(f"   Request ID: {result['request_id']}")
            
            return {
                "question_num": question_num,
                "question": question,
                "success": True,
                "latency_ms": result['latency_ms'],
                "token_count": result['token_count'],
                "retrieval_score": result['retrieval_score'],
                "sources_count": len(result['sources']),
                "request_id": result['request_id']
            }
        else:
            print(f"[ERROR] Error: {response.status_code} - {response.text}")
            return {
                "question_num": question_num,
                "question": question,
                "success": False,
                "error": response.text
            }
            
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return {
            "question_num": question_num,
            "question": question,
            "success": False,
            "error": str(e)
        }

def main():
    """Run all test questions and collect metrics"""
    print("[STEP] Starting MLflow Tracking Test")
    print(f"📅 Test started at: {datetime.now().isoformat()}")
    print(f"🎯 Testing {len(TEST_QUESTIONS)} questions")
    
    # Check if server is running
    try:
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code != 200:
            print("[ERROR] FastAPI server is not running. Please start it first:")
            print("   python fastapi_rag.py")
            return
        print("[OK] FastAPI server is running")
    except Exception as e:
        print("[ERROR] Cannot connect to FastAPI server. Please start it first:")
        print("   python fastapi_rag.py")
        return
    
    # Run all test questions
    results = []
    for i, question in enumerate(TEST_QUESTIONS, 1):
        result = test_question(question, i)
        results.append(result)
        time.sleep(1)  # Small delay between requests
    
    # Calculate summary statistics
    successful_results = [r for r in results if r['success']]
    
    if successful_results:
        avg_latency = sum(r['latency_ms'] for r in successful_results) / len(successful_results)
        avg_tokens = sum(r['token_count'] for r in successful_results) / len(successful_results)
        avg_retrieval = sum(r['retrieval_score'] for r in successful_results) / len(successful_results)
        avg_sources = sum(r['sources_count'] for r in successful_results) / len(successful_results)
        
        print(f"\n[INFO] Test Summary:")
        print(f"   Total Questions: {len(results)}")
        print(f"   Successful: {len(successful_results)}")
        print(f"   Failed: {len(results) - len(successful_results)}")
        print(f"   Average Latency: {avg_latency:.2f} ms")
        print(f"   Average Token Count: {avg_tokens:.1f}")
        print(f"   Average Retrieval Score: {avg_retrieval:.3f}")
        print(f"   Average Sources: {avg_sources:.1f}")
        
        # Save results to file
        test_results = {
            "test_timestamp": datetime.now().isoformat(),
            "total_questions": len(results),
            "successful_questions": len(successful_results),
            "failed_questions": len(results) - len(successful_results),
            "summary": {
                "avg_latency_ms": avg_latency,
                "avg_token_count": avg_tokens,
                "avg_retrieval_score": avg_retrieval,
                "avg_sources_count": avg_sources
            },
            "detailed_results": results
        }
        
        with open("mlflow_test_results.json", "w", encoding="utf-8") as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Results saved to: mlflow_test_results.json")
        
    else:
        print("[ERROR] No successful tests to summarize")
    
    print(f"\n🔍 Check MLflow UI for detailed tracking:")
    print(f"   mlflow ui")
    print(f"   Then visit: http://localhost:5000")
    
    print(f"\n[INFO] Check CRM logs:")
    print(f"   cat cases.json")

if __name__ == "__main__":
    main() 