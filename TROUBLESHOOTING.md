# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Google Provider - "max_retries" Error

**Error**: `GenerativeServiceClient.generate_content() got an unexpected keyword argument 'max_retries'`

**Cause**: Version incompatibility between langchain-google-genai and Google's client library.

**Solutions**:

#### Option A: Use Valid Google Models
Make sure to use valid Google/Gemini models:
```json
{
  "prompt": "Your question here",
  "provider": "google",
  "model": "gemini-1.5-flash"
}
```

**Valid Google Models**:
- `gemini-1.5-flash` (recommended)
- `gemini-1.5-pro`
- `gemini-1.0-pro`
- `gemini-pro`
- `gemini-pro-vision`

❌ **Don't use**: `llama3.2`, `gpt-4`, etc. with Google provider

#### Option B: Update Dependencies
```bash
uv add "langchain-google-genai>=2.1.12"
# or
pip install --upgrade langchain-google-genai
```

#### Option C: Use Different Provider
If you want to use Llama models, use Ollama provider instead:
```json
{
  "prompt": "Your question here",
  "provider": "ollama",
  "model": "llama3.2",
  "base_url": "http://localhost:11434"
}
```

### 2. Provider-Model Mismatch

**Error**: Various model-related errors

**Solution**: Use correct models for each provider:

| Provider | Example Models |
|----------|----------------|
| `google` | `gemini-1.5-flash`, `gemini-1.5-pro` |
| `openai` | `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo` |
| `anthropic` | `claude-3-5-sonnet-20241022`, `claude-3-opus` |
| `ollama` | `llama3.2`, `mistral`, `codellama` |

### 3. Missing API Keys

**Error**: "API key not found" or authentication errors

**Solution**: Set environment variables:
```bash
# Windows (Command Prompt)
set GOOGLE_API_KEY=your_key_here
set OPENAI_API_KEY=your_key_here
set ANTHROPIC_API_KEY=your_key_here

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your_key_here"
$env:OPENAI_API_KEY="your_key_here"
$env:ANTHROPIC_API_KEY="your_key_here"

# Linux/Mac
export GOOGLE_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

Or pass directly in request:
```json
{
  "prompt": "Your question",
  "provider": "openai",
  "api_key": "your_key_here"
}
```

### 4. Ollama Connection Issues

**Error**: Connection refused or Ollama not available

**Solution**: 
1. Start Ollama service:
   ```bash
   ollama serve
   ```

2. Pull the model:
   ```bash
   ollama pull llama3.2
   ```

3. Set correct base URL:
   ```bash
   set OLLAMA_BASE_URL=http://localhost:11434
   ```

### 5. Server Not Responding

**Error**: Connection refused to localhost:5454

**Solution**: Make sure the server is running:
```bash
cd d:\Minor\agentic-browser
uvicorn app.main:app --reload --host 0.0.0.0 --port 5454
```

## Quick Fixes

### Working Examples

#### 1. Google Provider (Fixed)
```bash
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "provider": "google",
    "model": "gemini-1.5-flash",
    "temperature": 0.7
  }'
```

#### 2. OpenAI Provider
```bash
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain machine learning",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  }'
```

#### 3. Ollama Provider (for Llama models)
```bash
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is AI?",
    "provider": "ollama",
    "model": "llama3.2",
    "base_url": "http://localhost:11434"
  }'
```

## Debug Mode

To get more detailed error information, check the server logs in your terminal where uvicorn is running.

## Still Having Issues?

1. **Check Server Logs**: Look at the terminal where uvicorn is running
2. **Verify API Keys**: Make sure your API keys are valid and have proper permissions
3. **Test with Minimal Request**: Start with the simplest possible request
4. **Check Model Availability**: Verify the model exists for your chosen provider

## Environment Verification

Test your setup:

```bash
# Test health endpoint
curl -X GET "http://localhost:5454/health"

# Should return: {"status":"ok"}
```

```bash
# Test with Google provider
curl -X POST "http://localhost:5454/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello",
    "provider": "google",
    "model": "gemini-1.5-flash"
  }'
```

---

*Updated: September 25, 2025*