#!/usr/bin/env python3
"""
Ollama Setup Script for NEA RAG System
Helps with Ollama installation and model setup
"""

import subprocess
import sys
import os
import requests
import time
from pathlib import Path

def check_ollama_installation():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] Ollama is not properly installed")
            return False
    except FileNotFoundError:
        print("[ERROR] Ollama is not installed")
        return False

def check_ollama_service():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("[OK] Ollama service is running")
            return True
        else:
            print("[ERROR] Ollama service is not responding properly")
            return False
    except requests.exceptions.RequestException:
        print("[ERROR] Ollama service is not running")
        return False

def check_llama3_model():
    """Check if llama3 model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m['name'] for m in models]
            
            if 'llama3' in model_names:
                print("[OK] Llama3 model is available")
                return True
            else:
                print("[ERROR] Llama3 model is not available")
                print(f"Available models: {model_names}")
                return False
        else:
            print("[ERROR] Cannot check models - Ollama service not responding")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking models: {e}")
        return False

def pull_llama3_model():
    """Pull the llama3 model"""
    print("[DOWNLOAD] Pulling Llama3 model (this may take several minutes)...")
    print("Note: This will download a large model file. Please wait...")
    
    try:
        # Run the pull command directly without capturing output
        result = subprocess.run(
            ['ollama', 'pull', 'llama3'],
            capture_output=False,  # Let output go directly to console
            text=True
        )
        
        # Check if successful
        if result.returncode == 0:
            print("[OK] Llama3 model pulled successfully")
            return True
        else:
            print("[ERROR] Failed to pull Llama3 model")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error pulling model: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("[PACKAGE] Installing Python dependencies...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Dependencies installed successfully")
            return True
        else:
            print(f"[ERROR] Error installing dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error installing dependencies: {e}")
        return False

def test_rag_system():
    """Test the RAG system"""
    print("[TEST] Testing RAG system...")
    
    try:
        # Import and test basic functionality
        from rag_system import test_ollama_connection, NEARAGSystem
        
        if test_ollama_connection():
            print("[OK] RAG system test passed")
            return True
        else:
            print("[ERROR] RAG system test failed")
            return False
    except Exception as e:
        print(f"[ERROR] Error testing RAG system: {e}")
        return False

def main():
    """Main setup function"""
    print("Ollama Setup for NEA RAG System")
    print("=" * 50)
    
    # Step 1: Check Ollama installation
    print("\n1. Checking Ollama installation...")
    if not check_ollama_installation():
        print("\n[DOWNLOAD] Ollama Installation Instructions:")
        print("Windows:")
        print("  1. Download from: https://ollama.ai/download")
        print("  2. Run the installer")
        print("  3. Restart your terminal")
        print("\nmacOS:")
        print("  brew install ollama")
        print("\nLinux:")
        print("  curl -fsSL https://ollama.ai/install.sh | sh")
        return
    
    # Step 2: Check Ollama service
    print("\n2. Checking Ollama service...")
    if not check_ollama_service():
        print("\n[SETUP] Starting Ollama service...")
        try:
            # Try to start Ollama service
            subprocess.run(['ollama', 'serve'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         start_new_session=True)
            
            # Wait a moment for service to start
            time.sleep(3)
            
            if check_ollama_service():
                print("[OK] Ollama service started successfully")
            else:
                print("[ERROR] Failed to start Ollama service")
                print("Please start Ollama manually: ollama serve")
                return
        except Exception as e:
            print(f"[ERROR] Error starting Ollama service: {e}")
            return
    
    # Step 3: Check Llama3 model
    print("\n3. Checking Llama3 model...")
    if not check_llama3_model():
        print("\n[DOWNLOAD] Llama3 model not found. Pulling...")
        if not pull_llama3_model():
            print("[ERROR] Failed to pull Llama3 model")
            print("You can try manually: ollama pull llama3")
            return
    
    # Step 4: Install Python dependencies
    print("\n4. Installing Python dependencies...")
    if not install_dependencies():
        print("[ERROR] Failed to install dependencies")
        print("Try manually: pip install -r requirements.txt")
        return
    
    # Step 5: Test RAG system
    print("\n5. Testing RAG system...")
    if not test_rag_system():
        print("[ERROR] RAG system test failed")
        return
    
    print("\n[SUCCESS] Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the RAG system: python rag_system.py")
    print("2. Ask questions about NEA waste management")
    print("3. The system will use your knowledge base to provide answers")

if __name__ == "__main__":
    main() 