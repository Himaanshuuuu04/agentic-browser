# 🤖 Agentic Browser Frontend

A sleek, minimalistic Streamlit frontend for the Agentic Browser API. This modern web interface provides an intuitive way to interact with all backend APIs including chat generation, GitHub analysis, and web content processing.

## ✨ Features

- **🎨 Modern UI Design**: Clean, minimalistic interface with gradient headers and responsive layout
- **💬 Chat Generation**: Interactive interface for AI chat with multiple LLM providers
- **🐙 GitHub Analysis**: Comprehensive repository analysis with context input
- **🌐 Website Processing**: Convert websites and HTML to markdown format
- **📊 Real-time API Status**: Live monitoring of backend connectivity
- **🔧 Advanced Settings**: Configurable LLM parameters and provider options
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Agentic Browser backend running on `http://localhost:5454`

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Frontend**
   
   **On Windows:**
   ```bash
   ./run_frontend.bat
   ```
   
   **On Linux/Mac:**
   ```bash
   chmod +x run_frontend.sh
   ./run_frontend.sh
   ```
   
   **Or manually:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the Application**
   
   Open your browser and navigate to: `http://localhost:8501`

## 🎯 Interface Overview

### Navigation
The sidebar provides easy navigation between different API endpoints:

- **💬 Chat Generation** - Generate AI responses using various LLM providers
- **🐙 GitHub Analysis** - Analyze repositories and answer code-related questions  
- **🌐 Website to Markdown** - Convert web pages to clean markdown
- **🔄 HTML to Markdown** - Convert raw HTML to markdown format

### API Status Indicator
- 🟢 **Green**: Backend API is online and responsive
- 🔴 **Red**: Backend API is offline or unreachable

## 📋 Usage Guide

### 1. Chat Generation

**Purpose**: Generate AI responses using multiple LLM providers

**Features**:
- Support for Google, OpenAI, Anthropic, Ollama, DeepSeek, and OpenRouter
- Configurable temperature and model selection
- Optional system messages for context
- API key override for different providers

**Usage**:
1. Enter your question/prompt
2. Optionally add a system message
3. Select your preferred LLM provider
4. Adjust temperature and other settings
5. Click "🚀 Generate Response"

### 2. GitHub Repository Analysis

**Purpose**: Analyze GitHub repositories and answer questions about codebases

**Features**:
- Context-aware analysis with file content
- Repository structure understanding
- Chat history for continuous conversations
- Advanced LLM configuration options

**Usage**:
1. Enter your question about the repository
2. Optionally provide:
   - Relevant code/context
   - File tree structure
   - Repository summary
   - Previous chat history
3. Configure advanced LLM settings if needed
4. Click "🔍 Analyze Repository"

### 3. Website to Markdown

**Purpose**: Convert web pages to clean, readable markdown

**Features**:
- Automatic content extraction
- Clean markdown formatting
- Example URLs for testing
- Support for modern web pages

**Usage**:
1. Enter a valid HTTP/HTTPS URL
2. Click "🔄 Convert to Markdown"
3. View the converted markdown content

### 4. HTML to Markdown

**Purpose**: Convert raw HTML content to markdown format

**Features**:
- Direct HTML input
- Preserves formatting and structure
- Example HTML snippets
- Support for complex HTML elements

**Usage**:
1. Paste your HTML content
2. Click "🔄 Convert to Markdown"
3. View the converted markdown output

## 🎨 Design Features

### Modern Styling
- **Gradient Headers**: Eye-catching gradient backgrounds
- **Card-based Layout**: Clean separation of content sections
- **Color-coded Responses**: Green for success, red for errors
- **Professional Typography**: Clean, readable fonts

### User Experience
- **Real-time Feedback**: Loading spinners and status indicators
- **Error Handling**: Clear error messages with troubleshooting hints
- **Responsive Design**: Adapts to different screen sizes
- **Keyboard Shortcuts**: Streamlit's built-in shortcuts

## ⚙️ Configuration

### API Base URL
The frontend is configured to connect to `http://localhost:5454` by default. To change this:

1. Edit `streamlit_app.py`
2. Update the `API_BASE_URL` variable:
   ```python
   API_BASE_URL = "https://your-api-domain.com"
   ```

### Streamlit Configuration
Create a `.streamlit/config.toml` file for custom Streamlit settings:

```toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🔧 Troubleshooting

### Common Issues

**❌ "API server is not running"**
- Ensure the backend server is started: `python -m app.run`
- Check if the API is accessible at `http://localhost:5454/health`
- Verify firewall settings aren't blocking the connection

**❌ "Request timed out"**
- The AI request is taking too long
- Try reducing the complexity of your prompt
- Check your internet connection
- Verify API keys are valid

**❌ "HTTP Error: No API key provided"**
- Set your API keys as environment variables
- Or provide API keys directly in the interface
- Check the API documentation for required keys

**❌ Streamlit not starting**
- Install requirements: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Try running directly: `python -m streamlit run streamlit_app.py`

### Performance Tips

1. **Use specific models**: Specify model names for better performance
2. **Optimize temperature**: Lower values (0.1-0.4) for focused responses
3. **Provide context**: Include relevant information for GitHub analysis
4. **Clear cache**: Restart Streamlit if responses seem cached

## 🚦 API Endpoints Integration

The frontend integrates with these backend endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check API status |
| `/v1/chat/generate` | POST | Generate AI responses |
| `/v1/github/answer` | POST | Analyze GitHub repositories |
| `/v1/website/markdown` | POST | Convert websites to markdown |
| `/v1/website/html-to-md` | POST | Convert HTML to markdown |

## 📦 Dependencies

- **streamlit>=1.28.0**: Web application framework
- **requests>=2.31.0**: HTTP library for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test the interface thoroughly
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the main repository LICENSE file for details.

## 🔗 Related Links

- [Backend API Documentation](../API_DOCUMENTATION.md)
- [Swagger UI](http://localhost:5454/docs) (when backend is running)
- [ReDoc](http://localhost:5454/redoc) (when backend is running)
- [Streamlit Documentation](https://docs.streamlit.io)

---

*Built with ❤️ using Streamlit and modern web technologies*