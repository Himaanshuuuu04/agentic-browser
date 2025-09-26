#!/bin/bash

# Streamlit Frontend Runner for Agentic Browser
echo "🤖 Starting Agentic Browser Frontend..."
echo "Make sure your backend API is running on http://localhost:5454"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Installing..."
    pip install -r requirements.txt
fi

# Run the Streamlit app
echo "🚀 Launching Streamlit app..."
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0