#!/usr/bin/env python3
"""
Agentic Browser Frontend Runner

This script starts the Streamlit frontend for the Agentic Browser API.
Make sure the backend API is running on http://localhost:5454 before starting.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_backend_status():
    """Check if the backend API is running"""
    try:
        response = requests.get("http://localhost:5454/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed successfully!")

def main():
    print("🤖 Agentic Browser Frontend Runner")
    print("=" * 40)
    
    # Check current directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing dependencies. Installing...")
        try:
            install_dependencies()
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    
    # Check backend status
    print("🔍 Checking backend API status...")
    if not check_backend_status():
        print("⚠️  Backend API is not running at http://localhost:5454")
        print("   Please start the backend first:")
        print("   python -m app.run")
        print("\n   The frontend will still start, but functionality will be limited.")
        
        response = input("\n   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Exiting...")
            sys.exit(1)
    else:
        print("✅ Backend API is running!")
    
    # Start Streamlit
    print("\n🚀 Starting Streamlit frontend...")
    print("   URL: http://localhost:8501")
    print("   Press Ctrl+C to stop")
    print("-" * 40)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Frontend stopped. Thank you for using Agentic Browser!")
    except Exception as e:
        print(f"\n❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()