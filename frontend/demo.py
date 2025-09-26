"""
Agentic Browser Frontend Demo

This script demonstrates how to test the frontend functionality
by making direct API calls to verify backend integration.
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5454"

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy!")
            return True
        else:
            print(f"❌ API returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_chat_generation():
    """Test chat generation endpoint"""
    print("\n💬 Testing Chat Generation...")
    
    data = {
        "prompt": "What is the capital of France?",
        "provider": "google",
        "temperature": 0.4
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/v1/chat/generate", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat generation successful!")
            print(f"Response: {result.get('content', 'No content')[:100]}...")
            return True
        else:
            print(f"❌ Chat generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat generation error: {e}")
        return False

def test_website_markdown():
    """Test website to markdown endpoint"""
    print("\n🌐 Testing Website to Markdown...")
    
    data = {
        "url": "https://httpbin.org/html"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/v1/website/markdown", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Website to markdown successful!")
            print(f"Markdown length: {len(result.get('markdown', ''))} characters")
            return True
        else:
            print(f"❌ Website to markdown failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Website to markdown error: {e}")
        return False

def test_html_markdown():
    """Test HTML to markdown endpoint"""
    print("\n🔄 Testing HTML to Markdown...")
    
    data = {
        "html": "<h1>Test Title</h1><p>This is a <strong>test</strong> paragraph.</p>"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/v1/website/html-to-md", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ HTML to markdown successful!")
            print(f"Markdown: {result.get('markdown', 'No content')}")
            return True
        else:
            print(f"❌ HTML to markdown failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ HTML to markdown error: {e}")
        return False

def test_github_analysis():
    """Test GitHub analysis endpoint"""
    print("\n🐙 Testing GitHub Analysis...")
    
    data = {
        "question": "What is this project about?",
        "text": "# My Project\nThis is a simple web application built with Python.",
        "tree": "src/\n  main.py\n  utils.py\nREADME.md",
        "summary": "A Python web application"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/v1/github/answer", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ GitHub analysis successful!")
            print(f"Answer: {result.get('answer', 'No answer')[:100]}...")
            return True
        else:
            print(f"❌ GitHub analysis failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ GitHub analysis error: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Agentic Browser Frontend Demo")
    print("=" * 50)
    print(f"Testing backend API at: {API_BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ Cannot proceed - API is not available.")
        print("Please make sure the backend is running:")
        print("  python -m app.run")
        return
    
    # Run all endpoint tests
    tests = [
        test_chat_generation,
        test_website_markdown,
        test_html_markdown,
        test_github_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The frontend should work perfectly.")
        print("\nTo start the frontend:")
        print("  python run_frontend.py")
        print("  or")
        print("  streamlit run streamlit_app.py")
    else:
        print("⚠️  Some tests failed. Check the backend configuration.")
        print("Make sure you have the required API keys set as environment variables.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()