from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

from core.config import get_logger
from core.llm import LargeLanguageModel
from prompts.github import github_processor_optimized
from tools.website_context.request_md import return_markdown as fetch_markdown
from tools.website_context.html_md import return_html_md as html_to_md


logger = get_logger(__name__)


app = FastAPI(
    title="Agentic Browser API",
    version="0.1.0",
    description="""
    🤖 **Agentic Browser API** - AI-powered tools for chat generation, GitHub analysis, and web content processing.
    
    ## Features
    
    * **Multi-LLM Support**: Google, OpenAI, Anthropic, Ollama, DeepSeek, OpenRouter
    * **GitHub Analysis**: Analyze repositories and answer questions about codebases
    * **Web Processing**: Convert websites and HTML to markdown
    * **MCP Integration**: Model Context Protocol server support
    
    ## Authentication
    
    Set your API keys as environment variables:
    ```bash
    export OPENAI_API_KEY=your_key
    export GOOGLE_API_KEY=your_key
    export ANTHROPIC_API_KEY=your_key
    ```
    """,
    contact={
        "name": "Agentic Browser API",
        "url": "https://github.com/tashifkhan/agentic-browser",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="The user prompt or question to send to the AI", example="Explain quantum computing in simple terms")
    system_message: Optional[str] = Field(None, description="System message to guide AI behavior and context", example="You are a helpful AI assistant specializing in science education.")
    provider: Literal[
        "google", "openai", "anthropic", "ollama", "deepseek", "openrouter"
    ] = Field("google", description="LLM provider to use for generation")
    model: Optional[str] = Field(None, description="Specific model name (e.g., 'gpt-4', 'claude-3-sonnet')", example="gpt-4")
    api_key: Optional[str] = Field(None, description="API key for the provider (overrides environment variable)")
    base_url: Optional[str] = Field(None, description="Custom base URL for the provider (mainly for Ollama)", example="http://localhost:11434")
    temperature: float = Field(0.4, description="Controls randomness in responses (0.0-2.0)", ge=0.0, le=2.0, example=0.7)


class ChatResponse(BaseModel):
    content: str = Field(..., description="The AI-generated response content", example="Quantum computing is a revolutionary approach to computation that harnesses quantum mechanical phenomena...")


class GithubAnswerRequest(BaseModel):
    question: str = Field(..., description="Question about the GitHub repository", example="How does authentication work in this codebase?")
    text: str = Field("", description="Relevant file content or combined context text", example="// auth.js\nfunction authenticate(user) { ... }")
    tree: str = Field("", description="Repository file tree structure", example="src/\n  auth/\n    auth.js\n    middleware.js\n  utils/\n    helpers.js")
    summary: str = Field("", description="Brief repository description", example="A Node.js authentication service with JWT tokens")
    chat_history: Optional[str] = Field("", description="Previous conversation context for continuity")
    # Optional LLM config to override defaults when building the chain
    llm_provider: Optional[str] = Field(None, description="LLM provider override")
    llm_model: Optional[str] = Field(None, description="LLM model override")
    llm_api_key: Optional[str] = Field(None, description="LLM API key override")
    llm_base_url: Optional[str] = Field(None, description="LLM base URL override")
    llm_temperature: Optional[float] = Field(None, description="LLM temperature override", ge=0.0, le=2.0)


class GithubAnswerResponse(BaseModel):
    answer: str = Field(..., description="AI-generated analysis and answer about the repository", example="The authentication in this codebase uses JWT tokens. The auth.js file contains the main authentication logic...")


class WebsiteMarkdownRequest(BaseModel):
    url: str = Field(..., description="Valid HTTP/HTTPS URL to convert to markdown", example="https://example.com/article")


class WebsiteMarkdownResponse(BaseModel):
    markdown: str = Field(..., description="Website content converted to markdown format", example="# Article Title\n\nThis is the article content in markdown format...")


class HtmlToMdRequest(BaseModel):
    html: str = Field(..., description="HTML content to convert to markdown", example="<h1>Title</h1><p>Content with <strong>bold</strong> text.</p>")


class HtmlToMdResponse(BaseModel):
    markdown: str = Field(..., description="HTML content converted to markdown format", example="# Title\n\nContent with **bold** text.")


@app.get("/health", tags=["Health"], summary="Health Check")
def health():
    """
    Check if the API service is running and healthy.
    
    Returns a simple status response to verify the service is operational.
    """
    return {"status": "ok"}


@app.post("/v1/chat/generate", response_model=ChatResponse, tags=["Chat"], summary="Generate AI Chat Response")
def chat_generate(req: ChatRequest):
    """
    Generate AI responses using various Large Language Model providers.
    
    **Supported Providers:**
    - `google`: Google Gemini models
    - `openai`: OpenAI GPT models  
    - `anthropic`: Anthropic Claude models
    - `ollama`: Local Ollama models
    - `deepseek`: DeepSeek models
    - `openrouter`: OpenRouter proxy
    
    **Example Request:**
    ```json
    {
        "prompt": "Explain quantum computing",
        "provider": "openai",
        "model": "gpt-4",
        "temperature": 0.7
    }
    ```
    """
    try:
        llm = LargeLanguageModel(
            model_name=req.model,
            api_key=req.api_key or "",
            provider=req.provider,
            base_url=req.base_url,
            temperature=req.temperature,
        )
        content = llm.generate_text(req.prompt, system_message=req.system_message)
        return ChatResponse(content=content)
    except Exception as e:
        logger.exception("/v1/chat/generate failed")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/v1/github/answer", response_model=GithubAnswerResponse, tags=["GitHub"], summary="Analyze GitHub Repository")
def github_answer(req: GithubAnswerRequest):
    """
    Analyze GitHub repositories and answer questions about codebases using AI.
    
    This endpoint processes repository information and provides intelligent answers
    about code structure, functionality, and implementation details.
    
    **Required:**
    - `question`: Your question about the repository
    
    **Optional Context (improves accuracy):**
    - `text`: Relevant file content or combined context
    - `tree`: Repository file tree structure  
    - `summary`: Brief repository description
    - `chat_history`: Previous conversation context
    
    **Example Request:**
    ```json
    {
        "question": "How does authentication work in this codebase?",
        "text": "// auth.js content here...",
        "tree": "src/\\n  auth/\\n    auth.js\\n    middleware.js",
        "summary": "A Node.js authentication service"
    }
    ```
    """
    try:
        llm_options = {}
        if req.llm_provider:
            llm_options["provider"] = req.llm_provider
        if req.llm_model:
            llm_options["model_name"] = req.llm_model
        if req.llm_api_key:
            llm_options["api_key"] = req.llm_api_key
        if req.llm_base_url:
            llm_options["base_url"] = req.llm_base_url
        if req.llm_temperature is not None:
            llm_options["temperature"] = req.llm_temperature

        answer = github_processor_optimized(
            question=req.question,
            text=req.text,
            tree=req.tree,
            summary=req.summary,
            chat_history=req.chat_history or "",
            llm_options=llm_options or None,
        )
        return GithubAnswerResponse(answer=answer)
    except Exception as e:
        logger.exception("/v1/github/answer failed")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/v1/website/markdown", response_model=WebsiteMarkdownResponse, tags=["Web Processing"], summary="Convert Website to Markdown")
def website_markdown(req: WebsiteMarkdownRequest):
    """
    Convert any website to clean, readable markdown format.
    
    This endpoint fetches a webpage and converts its content to markdown,
    removing unnecessary HTML elements while preserving structure and content.
    
    **Use Cases:**
    - Content extraction for analysis
    - Website archiving
    - Preparing content for AI processing
    - Documentation generation
    
    **Example Request:**
    ```json
    {
        "url": "https://example.com/article"
    }
    ```
    
    **Supported URLs:**
    - HTTP and HTTPS websites
    - Most modern web pages
    - JavaScript-rendered content (limited)
    """
    try:
        md = fetch_markdown(req.url)
        return WebsiteMarkdownResponse(markdown=md)
    except Exception as e:
        logger.exception("/v1/website/markdown failed")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/v1/website/html-to-md", response_model=HtmlToMdResponse, tags=["Web Processing"], summary="Convert HTML to Markdown")
def website_html_to_md(req: HtmlToMdRequest):
    """
    Convert raw HTML content to clean markdown format.
    
    This endpoint takes HTML content directly and converts it to markdown,
    useful when you already have HTML content that needs to be processed.
    
    **Use Cases:**
    - Processing scraped HTML content
    - Converting email HTML to readable format
    - Cleaning up HTML for documentation
    - Preparing HTML for AI analysis
    
    **Example Request:**
    ```json
    {
        "html": "<h1>Title</h1><p>Content with <strong>bold</strong> text.</p>"
    }
    ```
    
    **Features:**
    - Preserves text formatting (bold, italic, links)
    - Maintains heading hierarchy
    - Converts lists and tables appropriately
    - Removes unnecessary HTML attributes
    """
    try:
        md = html_to_md(req.html)
        return HtmlToMdResponse(markdown=md)
    except Exception as e:
        logger.exception("/v1/website/html-to-md failed")
        raise HTTPException(status_code=400, detail=str(e))


# Optional root
@app.get("/", tags=["Info"], summary="API Information")
def root():
    """
    Get basic information about the Agentic Browser API.
    
    Returns the API name and version for service identification.
    """
    return {
        "name": app.title, 
        "version": app.version,
        "description": "AI-powered tools for chat generation, GitHub analysis, and web content processing",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
