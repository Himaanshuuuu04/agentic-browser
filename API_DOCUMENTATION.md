# Agentic Browser API Documentation

## Overview

The Agentic Browser API is a FastAPI-based service that provides AI-powered tools for chat generation, GitHub repository analysis, and website content processing. It supports multiple LLM providers and offers both REST API endpoints and MCP (Model Context Protocol) server functionality.

**Base URL**: `http://localhost:5454`  
**Version**: `0.1.0`

## Table of Contents

- [Authentication](#authentication)
- [Supported LLM Providers](#supported-llm-providers)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Chat Generation](#chat-generation)
  - [GitHub Repository Analysis](#github-repository-analysis)
  - [Website to Markdown](#website-to-markdown)
  - [HTML to Markdown](#html-to-markdown)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [MCP Server](#mcp-server)

## Authentication

The API supports multiple authentication methods depending on the LLM provider:

- **Environment Variables**: Set API keys as environment variables
- **Request Headers**: Pass API keys in request body
- **Direct Configuration**: Specify API keys directly in requests

### Environment Variables

```bash
export GOOGLE_API_KEY=your_google_api_key
export OPENAI_API_KEY=your_openai_api_key
export ANTHROPIC_API_KEY=your_anthropic_api_key
export OLLAMA_BASE_URL=http://localhost:11434
```

## Supported LLM Providers

| Provider | Models | Authentication |
|----------|--------|----------------|
| Google | gemini-pro, gemini-1.5-pro | API Key |
| OpenAI | gpt-3.5-turbo, gpt-4, gpt-4-turbo | API Key |
| Anthropic | claude-3-sonnet, claude-3-opus | API Key |
| Ollama | Local models | Base URL |
| DeepSeek | deepseek-chat | API Key |
| OpenRouter | Various models | API Key |

## Endpoints

### Health Check

Check if the API service is running.

- **URL**: `/health`
- **Method**: `GET`
- **Authentication**: None required

#### Response

```json
{
  "status": "ok"
}
```

### Root Information

Get basic API information.

- **URL**: `/`
- **Method**: `GET`
- **Authentication**: None required

#### Response

```json
{
  "name": "Agentic Browser API",
  "version": "0.1.0"
}
```

### Chat Generation

Generate AI responses using various LLM providers.

- **URL**: `/v1/chat/generate`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "prompt": "string (required)",
  "system_message": "string (optional)",
  "provider": "google|openai|anthropic|ollama|deepseek|openrouter (default: google)",
  "model": "string (optional)",
  "api_key": "string (optional)",
  "base_url": "string (optional)",
  "temperature": "number (default: 0.4)"
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | The user prompt/question |
| `system_message` | string | No | null | System message to guide AI behavior |
| `provider` | string | No | "google" | LLM provider to use |
| `model` | string | No | null | Specific model name |
| `api_key` | string | No | null | API key (overrides env var) |
| `base_url` | string | No | null | Custom base URL for provider |
| `temperature` | number | No | 0.4 | Randomness in response (0.0-2.0) |

#### Response

```json
{
  "content": "string"
}
```

#### Example Request

```bash
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.7
  }'
```

### GitHub Repository Analysis

Analyze GitHub repositories and answer questions about codebases.

- **URL**: `/v1/github/answer`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "question": "string (required)",
  "text": "string (default: '')",
  "tree": "string (default: '')",
  "summary": "string (default: '')",
  "chat_history": "string (optional)",
  "llm_provider": "string (optional)",
  "llm_model": "string (optional)",
  "llm_api_key": "string (optional)",
  "llm_base_url": "string (optional)",
  "llm_temperature": "number (optional)"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | Question about the repository |
| `text` | string | No | Relevant file content or combined context |
| `tree` | string | No | Repository file tree structure |
| `summary` | string | No | Repository summary |
| `chat_history` | string | No | Previous conversation context |
| `llm_*` | various | No | LLM configuration overrides |

#### Response

```json
{
  "answer": "string"
}
```

#### Example Request

```bash
curl -X POST "http://localhost:5454/v1/github/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does this repository do?",
    "text": "# My Project\nThis is a web scraping tool...",
    "tree": "src/\n  main.py\n  utils.py\nREADME.md",
    "summary": "A Python web scraping tool"
  }'
```

### Website to Markdown

Convert web pages to markdown format.

- **URL**: `/v1/website/markdown`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "url": "string (required)"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | Valid HTTP/HTTPS URL to convert |

#### Response

```json
{
  "markdown": "string"
}
```

#### Example Request

```bash
curl -X POST "http://localhost:5454/v1/website/markdown" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

### HTML to Markdown

Convert HTML content to markdown format.

- **URL**: `/v1/website/html-to-md`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "html": "string (required)"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `html` | string | Yes | HTML content to convert |

#### Response

```json
{
  "markdown": "string"
}
```

#### Example Request

```bash
curl -X POST "http://localhost:5454/v1/website/html-to-md" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<h1>Hello World</h1><p>This is a paragraph.</p>"
  }'
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

### Success Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully

### Error Codes
- `400 Bad Request`: Invalid request parameters or body
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Endpoint not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "detail": "string"
}
```

### Common Errors

| Error | Cause | Solution |
|-------|--------|----------|
| "No API key provided" | Missing authentication | Set environment variable or include in request |
| "Invalid provider" | Unsupported LLM provider | Use supported provider from list |
| "Model not found" | Invalid model name | Check provider's available models |
| "Rate limit exceeded" | Too many requests | Implement rate limiting or wait |

## Examples

### Python Client Example

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:5454"

# Chat generation
def generate_chat(prompt, provider="google"):
    response = requests.post(
        f"{BASE_URL}/v1/chat/generate",
        json={
            "prompt": prompt,
            "provider": provider,
            "temperature": 0.7
        }
    )
    return response.json()

# Website to markdown
def website_to_markdown(url):
    response = requests.post(
        f"{BASE_URL}/v1/website/markdown",
        json={"url": url}
    )
    return response.json()

# Usage
result = generate_chat("What is machine learning?")
print(result["content"])

markdown = website_to_markdown("https://example.com")
print(markdown["markdown"])
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:5454';

// Chat generation
async function generateChat(prompt, provider = 'google') {
  try {
    const response = await axios.post(`${BASE_URL}/v1/chat/generate`, {
      prompt: prompt,
      provider: provider,
      temperature: 0.7
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

// GitHub analysis
async function analyzeGitHub(question, text, tree, summary) {
  try {
    const response = await axios.post(`${BASE_URL}/v1/github/answer`, {
      question: question,
      text: text,
      tree: tree,
      summary: summary
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

// Usage
generateChat('Explain REST APIs').then(result => {
  console.log(result.content);
});
```

### cURL Examples

```bash
# Health check
curl -X GET "http://localhost:5454/health"

# Generate chat response
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the meaning of life?",
    "provider": "anthropic",
    "temperature": 0.8
  }'

# Convert website to markdown
curl -X POST "http://localhost:5454/v1/website/markdown" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}'

# Convert HTML to markdown
curl -X POST "http://localhost:5454/v1/website/html-to-md" \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1>Title</h1><p>Content</p>"}'
```

## MCP Server

The project also provides a Model Context Protocol (MCP) server for integration with MCP-compatible clients.

### Running MCP Server

```bash
python -m mcp_server.server
```

### Available MCP Tools

1. **llm.generate** - Generate text using LLM
2. **github.answer** - Analyze GitHub repositories
3. **website.fetch_markdown** - Fetch website as markdown
4. **website.html_to_md** - Convert HTML to markdown

### MCP Client Integration

The MCP server communicates over stdio and can be launched directly by MCP clients. Use the entrypoint `python -m mcp_server.server` or the installed script `agentic-mcp`.

## Interactive API Documentation

When the server is running, you can access interactive API documentation at:

- **Swagger UI**: `http://localhost:5454/docs`
- **ReDoc**: `http://localhost:5454/redoc`
- **OpenAPI JSON**: `http://localhost:5454/openapi.json`

## Rate Limiting and Best Practices

1. **API Keys**: Store API keys securely as environment variables
2. **Rate Limiting**: Respect provider rate limits to avoid errors
3. **Error Handling**: Always implement proper error handling in your client code
4. **Timeouts**: Set appropriate timeouts for long-running requests
5. **Validation**: Validate input data before sending requests

## Support and Contributing

For issues, feature requests, or contributions, please visit the project repository.

---

*Last updated: September 25, 2025*