#!/usr/bin/env python3
"""
Complete MLOps Setup for NEA RAG System
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, check_output=False):
    """Run a command and handle errors"""
    print(f"[STEP] {description}...")
    try:
        if check_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"[OK] {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True, result.stdout.strip()
        else:
            result = subprocess.run(command, shell=True, check=True)
            print(f"[OK] {description} completed successfully")
            return True, None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed:")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False, None

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        "fastapi", "uvicorn", "pydantic", "mlflow", "dvc", 
        "requests", "langchain", "faiss-cpu", "ollama"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    """Complete MLOps setup"""
    print("[SETUP] Complete MLOps Setup for NEA RAG System")
    print("=" * 60)
    
    # Step 1: Check and install Python packages
    print("\n[STEP] Step 1: Checking Python packages...")
    missing_packages = check_python_packages()
    
    if missing_packages:
        print(f"[WARN] Missing packages: {', '.join(missing_packages)}")
        print("Installing from requirements.txt...")
        
        if not run_command("pip install -r requirements.txt", "Installing requirements"):
            print("[ERROR] Failed to install requirements. Please install manually:")
            print("   pip install -r requirements.txt")
            return False
    else:
        print("[OK] All required packages are installed")
    
    # Step 2: Setup DVC
    print("\n[STEP] Step 2: Setting up DVC...")
    if not run_command("dvc --version", "Checking DVC installation", check_output=True)[0]:
        print("[ERROR] DVC not found. Installing...")
        if not run_command("pip install dvc", "Installing DVC"):
            return False
    
    # Initialize DVC if not already initialized
    if not Path(".dvc").exists():
        if not run_command("dvc init", "Initializing DVC"):
            return False
    
    # Step 3: Setup MLflow
    print("\n[STEP] Step 3: Setting up MLflow...")
    mlflow_db = Path("mlflow.db")
    if not mlflow_db.exists():
        print("[INFO] MLflow database will be created on first run")
    
    # Step 4: Check data availability
    print("\n[STEP] Step 4: Checking data availability...")
    raw_data_path = Path("data/raw")
    knowledge_base_path = Path("data/knowledge_base/snippets")
    
    if not raw_data_path.exists() or not list(raw_data_path.glob("*.json")):
        print("[WARN] No raw data found. Please run the scraper first:")
        print("   python scrape.py")
        print("   python generate_rag_kb.py")
    
    if not knowledge_base_path.exists() or not list(knowledge_base_path.glob("*.md")):
        print("[WARN] No knowledge base found. Please generate it:")
        print("   python generate_rag_kb.py")
    
    # Step 5: Setup DVC tracking for raw data
    print("\n[STEP] Step 5: Setting up DVC tracking...")
    if raw_data_path.exists() and list(raw_data_path.glob("*.json")):
        dvc_file = raw_data_path.with_suffix('.dvc')
        if not dvc_file.exists():
            if not run_command(f"dvc add {raw_data_path}", f"Adding {raw_data_path} to DVC"):
                print("[WARN] DVC add failed, but continuing...")
    
    # Step 6: Create necessary directories
    print("\n[STEP] Step 6: Creating necessary directories...")
    directories = [
        "logs",
        "mlflow_runs",
        "test_results"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"[OK] Created directory: {directory}")
    
    # Step 7: Create startup scripts
    print("\n[STEP] Step 7: Creating startup scripts...")
    
    # FastAPI startup script
    fastapi_script = "#!/bin/bash\necho 'Starting FastAPI RAG Server...'\necho 'MLflow UI will be available at: http://localhost:5000'\necho 'FastAPI docs will be available at: http://localhost:8000/docs'\necho ''\npython scripts/fastapi_rag.py\n"
    
    with open("start_fastapi.sh", "w") as f:
        f.write(fastapi_script)
    
    # MLflow UI startup script
    mlflow_script = "#!/bin/bash\necho 'Starting MLflow UI...'\necho 'MLflow UI will be available at: http://localhost:5000'\necho ''\nmlflow ui --host 0.0.0.0 --port 5000\n"
    
    with open("start_mlflow.sh", "w") as f:
        f.write(mlflow_script)
    
    # Test script
    test_script = "#!/bin/bash\necho 'Running MLflow tracking tests...'\necho 'Make sure FastAPI server is running first!'\necho ''\npython scripts/test_mlflow_tracking.py\n"
    
    with open("run_tests.sh", "w") as f:
        f.write(test_script)
    
    print("[OK] Created startup scripts")
    
    # Step 8: Final instructions
    print("\n[INFO] Next Steps:")
    print("")
    print("1. Start FastAPI server:")
    print("   python fastapi_rag.py")
    print("   # or")
    print("   bash start_fastapi.sh")
    print("")
    print("2. Start MLflow UI (in another terminal):")
    print("   mlflow ui")
    print("   # or")
    print("   bash start_mlflow.sh")
    print("   # Then visit: http://localhost:5000")
    print("")
    print("3. Run test questions:")
    print("   python test_mlflow_tracking.py")
    print("   # or")
    print("   bash run_tests.sh")
    print("")
    print("4. Check CRM logs:")
    print("   cat cases.json")
    print("")
    print("5. API Documentation:")
    print("   http://localhost:8000/docs")
    print("")
    print("6. Data versioning:")
    print("   dvc status")
    print("   dvc list .")
    print("")
    print("Metrics tracked:")
    print("   - Latency (ms)")
    print("   - Token count")
    print("   - Retrieval score")
    print("   - Number of sources")
    print("   - User sessions")
    print("")
    print("Data lineage:")
    print("   - Raw data versioned with DVC")
    print("   - Experiments tracked with MLflow")
    print("   - Chat interactions logged to CRM")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 