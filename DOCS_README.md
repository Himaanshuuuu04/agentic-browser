# 📚 API Documentation

This directory contains comprehensive documentation for the Agentic Browser API.

## Documentation Files

### 📖 [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
Complete markdown documentation with:
- Detailed endpoint descriptions
- Request/response examples
- Authentication guide
- Error handling
- Code examples in multiple languages

### 🌐 [docs.html](./docs.html)
Interactive HTML documentation with:
- Clean, easy-to-read format
- Quick navigation
- Live links to interactive docs
- Status indicators

## Quick Access

### Interactive Documentation (When Server is Running)
- **Swagger UI**: http://localhost:5454/docs
- **ReDoc**: http://localhost:5454/redoc
- **OpenAPI JSON**: http://localhost:5454/openapi.json

### Key Endpoints
- `GET /health` - Health check
- `POST /v1/chat/generate` - AI chat generation
- `POST /v1/github/answer` - GitHub repository analysis
- `POST /v1/website/markdown` - Website to markdown conversion
- `POST /v1/website/html-to-md` - HTML to markdown conversion

### Supported LLM Providers
- Google (Gemini)
- OpenAI (GPT models)
- Anthropic (Claude)
- Ollama (Local models)
- DeepSeek
- OpenRouter

## Getting Started

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 5454
   ```

2. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_key
   export GOOGLE_API_KEY=your_key
   export ANTHROPIC_API_KEY=your_key
   ```

3. **Test the API**:
   ```bash
   curl -X GET "http://localhost:5454/health"
   ```

4. **View interactive docs**:
   Open http://localhost:5454/docs in your browser

## Examples

### Chat Generation
```bash
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain machine learning",
    "provider": "openai",
    "temperature": 0.7
  }'
```

### Website to Markdown
```bash
curl -X POST "http://localhost:5454/v1/website/markdown" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

For more detailed examples and complete documentation, see the files above.