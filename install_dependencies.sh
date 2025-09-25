#!/bin/bash

# Install all project dependencies using pip
echo "Installing project dependencies..."

pip install \
    "bs4>=0.0.2" \
    "gitingest>=0.3.1" \
    "html2text>=2025.4.15" \
    "langchain>=0.3.27" \
    "langchain-anthropic>=0.3.20" \
    "langchain-google-genai>=2.1.12" \
    "langchain-ollama>=0.3.8" \
    "langchain-openai>=0.3.33" \
    "python-dotenv>=1.1.1" \
    "yt-dlp>=2025.9.23" \
    "fastapi>=0.115.0" \
    "uvicorn>=0.30.6" \
    "pydantic>=2.9.0" \
    "mcp>=1.2.0" \
    "requests>=2.32.3"

echo "Dependencies installation completed!"