@echo off
echo 🤖 Starting Agentic Browser Frontend...
echo Make sure your backend API is running on http://localhost:5454
echo.

REM Check if streamlit is installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit is not installed. Installing...
    pip install -r requirements.txt
)

REM Run the Streamlit app
echo 🚀 Launching Streamlit app...
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0