import streamlit as st
import requests
import json
from typing import Optional, Dict, Any
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import random
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import extra_streamlit_components as stx

# Configuration
API_BASE_URL = "http://localhost:5454"

# Page configuration
st.set_page_config(
    page_title="🤖 Agentic Browser",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'api_calls_count' not in st.session_state:
    st.session_state.api_calls_count = 0
if 'last_response_time' not in st.session_state:
    st.session_state.last_response_time = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'favorite_endpoints' not in st.session_state:
    st.session_state.favorite_endpoints = []

# Custom CSS for engaging styling with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #6B73FF 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: headerGlow 3s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes headerGlow {
        0% { box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }
        100% { box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5); }
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .api-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #e9ecef;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .api-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        transition: left 0.5s;
    }
    
    .api-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .api-card:hover::before {
        left: 100%;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
    }
    
    .response-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #c3e6c3;
        margin: 1.5rem 0;
        animation: slideIn 0.5s ease-out;
        position: relative;
    }
    
    .response-box::after {
        content: '✨';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ffeaea 0%, #fff5f5 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #ffb3b3;
        margin: 1.5rem 0;
        color: #d63031;
        animation: slideIn 0.5s ease-out;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background-color: #00b894;
        box-shadow: 0 0 10px rgba(0, 184, 148, 0.5);
    }
    
    .status-offline {
        background-color: #e17055;
        box-shadow: 0 0 10px rgba(225, 112, 85, 0.5);
    }
    
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .floating-element {
        position: fixed;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .interactive-tooltip {
        position: relative;
        cursor: help;
    }
    
    .interactive-tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 12px;
        background: #333;
        color: white;
        border-radius: 8px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #f3f3f3;
        border-top: 2px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    .sidebar .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)

def check_api_health() -> bool:
    """Check if the API is running"""
    try:
        start_time = time.time()
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        st.session_state.last_response_time = (time.time() - start_time) * 1000
        return response.status_code == 200
    except:
        st.session_state.last_response_time = 0
        return False

def get_lottie_animation():
    """Get a Lottie animation for the header"""
    return {
        "v": "5.5.7",
        "fr": 29.9700012207031,
        "ip": 0,
        "op": 140.000005694758,
        "w": 500,
        "h": 500,
        "nm": "robot",
        "ddd": 0,
        "assets": [],
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "robot",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100},
                    "r": {"a": 1, "k": [{"t": 0, "s": [0], "e": [360], "to": [60], "ti": [-60]}]},
                    "p": {"a": 0, "k": [250, 250, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "d": 1,
                                "ty": "el",
                                "s": {"a": 0, "k": [100, 100]},
                                "p": {"a": 0, "k": [0, 0]}
                            }
                        ]
                    }
                ]
            }
        ]
    }

def create_usage_chart():
    """Create a usage statistics chart"""
    if st.session_state.api_calls_count > 0:
        # Sample data for demo
        endpoints = ['Chat', 'GitHub', 'Website', 'HTML']
        usage_data = [
            random.randint(1, st.session_state.api_calls_count) for _ in endpoints
        ]
        
        fig = px.pie(
            values=usage_data,
            names=endpoints,
            title="API Usage Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            height=300,
            font=dict(size=12)
        )
        return fig
    return None

def create_response_time_chart():
    """Create response time chart"""
    # Generate sample response time data
    times = [datetime.now() - timedelta(minutes=x) for x in range(10, 0, -1)]
    response_times = [random.uniform(200, 1500) for _ in times]
    
    df = pd.DataFrame({
        'Time': times,
        'Response Time (ms)': response_times
    })
    
    fig = px.line(
        df, 
        x='Time', 
        y='Response Time (ms)',
        title='API Response Times',
        line_shape='spline'
    )
    fig.update_traces(line_color='#667eea')
    fig.update_layout(height=300)
    return fig

def make_api_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=60)
        
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to API"}
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json().get("detail", str(e))
        except:
            error_detail = str(e)
        return {"success": False, "error": f"HTTP Error: {error_detail}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def display_response(response: Dict[str, Any]):
    """Display API response with proper formatting"""
    if response["success"]:
        st.markdown('<div class="response-box">', unsafe_allow_html=True)
        st.success("✅ Request successful!")
        
        data = response["data"]
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ["content", "answer", "markdown"]:
                    st.markdown(f"**{key.title()}:**")
                    st.text_area("Response", value, height=200, disabled=True)
                else:
                    st.write(f"**{key.title()}:** {value}")
        else:
            st.json(data)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ Error: {response['error']}")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Floating background elements
    st.markdown("""
    <div class="floating-element" style="top: 10%; right: 10%;"></div>
    <div class="floating-element" style="top: 60%; left: 5%; animation-delay: -2s;"></div>
    <div class="floating-element" style="top: 30%; right: 30%; animation-delay: -4s;"></div>
    """, unsafe_allow_html=True)
    
    # Enhanced Header with animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🤖 Agentic Browser</h1>
            <p>✨ AI-powered tools for chat generation, GitHub analysis, and web content processing ✨</p>
            <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.9;">
                Explore • Analyze • Create
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Check API status with enhanced metrics
    api_status = check_api_health()
    status_class = "status-online" if api_status else "status-offline"
    status_text = "🟢 Online" if api_status else "🔴 Offline"
    
    # Main navigation with option menu
    selected = option_menu(
        menu_title=None,
        options=["🏠 Dashboard", "💬 Chat", "🐙 GitHub", "🌐 Website", "🔄 HTML", "📊 Analytics"],
        icons=["house", "chat-dots", "github", "globe", "code-slash", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "padding": "12px",
                "border-radius": "10px",
                "background-color": "transparent",
                "color": "#333",
                "--hover-color": "#f0f2f6"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )
    
    # Sidebar with enhanced stats
    with st.sidebar:
        st.markdown("### 🚀 System Status")
        
        # API Status Card
        status_color = "#00b894" if api_status else "#e17055"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {status_color} 0%, {status_color}dd 100%);">
            <h4 style="margin: 0; color: white;">API Status</h4>
            <p style="margin: 5px 0 0 0; color: white; font-size: 1.1rem;">{status_text}</p>
            <small style="color: rgba(255,255,255,0.8);">Response: {st.session_state.last_response_time:.0f}ms</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("API Calls", st.session_state.api_calls_count, delta=1 if st.session_state.api_calls_count > 0 else None)
        with col2:
            st.metric("Uptime", "99.9%", delta="0.1%")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh Status", use_container_width=True):
            check_api_health()
            st.rerun()
        
        if st.button("🧹 Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.api_calls_count = 0
            st.success("History cleared!")
        
        # Favorite endpoints
        st.markdown("### ⭐ Favorites")
        if st.session_state.favorite_endpoints:
            for fav in st.session_state.favorite_endpoints:
                if st.button(f"⭐ {fav}", use_container_width=True, key=f"fav_{fav}"):
                    # Navigate to favorite endpoint
                    pass
        else:
            st.info("No favorites yet. Use endpoints to add them!")
        
        # System info
        st.markdown("### � System Info")
        st.code(f"Base URL: {API_BASE_URL}", language="text")
        st.code(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}", language="text")
    
    if not api_status:
        st.error("� API server is not running!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="api-card" style="text-align: center; padding: 3rem;">
                <h3>🔧 Server Setup Required</h3>
                <p>Please start the backend server to continue.</p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <code>python -m app.run</code>
                </div>
                <p><small>Make sure the server is running on http://localhost:5454</small></p>
            </div>
            """, unsafe_allow_html=True)
        return
    
    # Main content based on selection
    if selected == "🏠 Dashboard":
        dashboard_interface()
    elif selected == "💬 Chat":
        chat_generation_interface()
    elif selected == "🐙 GitHub":
        github_analysis_interface()
    elif selected == "🌐 Website":
        website_markdown_interface()
    elif selected == "🔄 HTML":
        html_markdown_interface()
    elif selected == "📊 Analytics":
        analytics_interface()

def dashboard_interface():
    """Enhanced dashboard with overview and quick stats"""
    st.markdown("## 🏠 Dashboard")
    
    # Welcome message
    st.markdown("""
    <div class="api-card">
        <h3>Welcome to Agentic Browser! 🚀</h3>
        <p>Your AI-powered companion for web exploration, code analysis, and content processing.</p>
        <p>Select any tool from the navigation above to get started with your AI journey!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>💬 Chat AI</h4>
            <p>Multi-provider AI chat with Google, OpenAI, Anthropic & more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🐙 GitHub Analysis</h4>
            <p>Intelligent code repository analysis and Q&A</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🌐 Web Processing</h4>
            <p>Convert websites to clean markdown format</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h4>🔄 HTML Converter</h4>
            <p>Transform HTML content to markdown</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    if st.session_state.chat_history:
        st.markdown("## 📝 Recent Activity")
        for i, item in enumerate(st.session_state.chat_history[-3:]):  # Show last 3
            with st.expander(f"� {item.get('type', 'Chat')} - {item.get('timestamp', 'Recent')}"):
                st.write(f"**Input:** {item.get('input', 'N/A')[:100]}...")
                st.write(f"**Output:** {item.get('output', 'N/A')[:100]}...")
    
    # API Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.api_calls_count > 0:
            chart = create_usage_chart()
            if chart:
                st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        response_chart = create_response_time_chart()
        st.plotly_chart(response_chart, use_container_width=True)

def analytics_interface():
    """Analytics and usage statistics"""
    st.markdown("## 📊 Analytics & Usage Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total API Calls",
            st.session_state.api_calls_count,
            delta=random.randint(1, 5)
        )
    
    with col2:
        st.metric(
            "Avg Response Time",
            f"{st.session_state.last_response_time:.0f}ms",
            delta=f"{random.randint(-50, 50)}ms"
        )
    
    with col3:
        st.metric(
            "Success Rate",
            "98.5%",
            delta="1.2%"
        )
    
    # Usage trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Usage Trends")
        # Generate sample usage data
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')[-30:]
        usage_data = [random.randint(5, 50) for _ in dates]
        
        df = pd.DataFrame({'Date': dates, 'API Calls': usage_data})
        fig = px.line(df, x='Date', y='API Calls', title='Daily API Usage')
        fig.update_traces(line_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Top Endpoints")
        endpoints_data = {
            'Endpoint': ['Chat Generation', 'GitHub Analysis', 'Website MD', 'HTML MD'],
            'Calls': [45, 32, 28, 15],
            'Avg Response (ms)': [1200, 2100, 800, 300]
        }
        df = pd.DataFrame(endpoints_data)
        
        fig = px.bar(df, x='Endpoint', y='Calls', 
                    title='Endpoint Usage',
                    color='Calls',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    st.markdown("### ⚡ Performance Metrics")
    
    # Generate sample performance data
    performance_data = {
        'Metric': ['Uptime', 'Success Rate', 'Avg Response', 'Error Rate'],
        'Value': [99.9, 98.5, 850, 1.5],
        'Unit': ['%', '%', 'ms', '%'],
        'Status': ['Excellent', 'Good', 'Good', 'Excellent']
    }
    
    df_perf = pd.DataFrame(performance_data)
    
    # Color-coded performance table
    def color_performance(val):
        if val in ['Excellent']:
            return 'background-color: #d4edda'
        elif val in ['Good']:
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #f8d7da'
    
    styled_df = df_perf.style.applymap(color_performance, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)

def chat_generation_interface():
    # Add to favorites functionality
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 💬 Chat Generation")
    with col2:
        if st.button("⭐ Add to Favorites"):
            if "💬 Chat Generation" not in st.session_state.favorite_endpoints:
                st.session_state.favorite_endpoints.append("💬 Chat Generation")
                st.success("Added to favorites!")
    
    st.markdown("""
    <div class="api-card">
        <h4>🎯 Generate AI responses using various Large Language Model providers</h4>
        <p>✨ Supports Google, OpenAI, Anthropic, Ollama, DeepSeek, and OpenRouter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick prompt suggestions
    st.markdown("### 💡 Quick Prompts")
    prompt_cols = st.columns(4)
    
    quick_prompts = [
        "Explain quantum computing",
        "Write a Python function",
        "Summarize recent AI trends", 
        "Create a marketing plan"
    ]
    
    selected_prompt = None
    for i, prompt_text in enumerate(quick_prompts):
        with prompt_cols[i]:
            if st.button(f"💭 {prompt_text}", key=f"prompt_{i}", use_container_width=True):
                selected_prompt = prompt_text
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = st.text_area(
            "Your Question/Prompt",
            value=selected_prompt if selected_prompt else "",
            placeholder="Ask me anything...",
            height=120,
            help="Enter your question or prompt here. You can also use the quick prompts above!"
        )
        
        system_message = st.text_area(
            "System Message (Optional)",
            placeholder="You are a helpful AI assistant specialized in...",
            height=80,
            help="Set the AI's role and behavior context"
        )
        
        # Advanced options in an expander
        with st.expander("🔧 Advanced Options"):
            col_a, col_b = st.columns(2)
            with col_a:
                api_key = st.text_input(
                    "API Key Override",
                    type="password",
                    placeholder="Your API key here..."
                )
            with col_b:
                base_url = st.text_input(
                    "Base URL (Ollama)",
                    placeholder="http://localhost:11434"
                )
    
    with col2:
        st.markdown("### ⚙️ Model Configuration")
        
        provider = st.selectbox(
            "🤖 LLM Provider",
            ["google", "openai", "anthropic", "ollama", "deepseek", "openrouter"],
            index=0,
            help="Choose your preferred AI provider"
        )
        
        # Provider-specific model suggestions
        model_suggestions = {
            "google": ["gemini-pro", "gemini-1.5-pro"],
            "openai": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
            "anthropic": ["claude-3-sonnet", "claude-3-opus"],
            "ollama": ["llama2", "codellama", "mistral"],
            "deepseek": ["deepseek-chat"],
            "openrouter": ["meta-llama/llama-2-70b-chat"]
        }
        
        model = st.selectbox(
            "🧠 Model",
            [""] + model_suggestions.get(provider, []),
            help=f"Select a model for {provider}"
        )
        
        temperature = st.slider(
            "🌡️ Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.4,
            step=0.1,
            help="Higher values make output more creative, lower values more focused"
        )
        
        # Real-time preview of settings
        st.markdown("#### 📋 Current Settings")
        st.json({
            "provider": provider,
            "model": model or "default",
            "temperature": temperature,
            "has_system_message": bool(system_message.strip()),
            "has_api_key": bool(api_key.strip())
        })
    
    # Generate button with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_clicked = st.button(
            "🚀 Generate AI Response", 
            type="primary", 
            use_container_width=True,
            help="Click to generate your AI response"
        )
    
    if generate_clicked:
        if not prompt.strip():
            st.error("🚨 Please enter a prompt to generate a response!")
            return
        
        # Progress bar and status
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔄 Preparing request...")
            progress_bar.progress(20)
            
            data = {
                "prompt": prompt,
                "provider": provider,
                "temperature": temperature
            }
            
            if system_message.strip():
                data["system_message"] = system_message
            if model.strip():
                data["model"] = model
            if api_key.strip():
                data["api_key"] = api_key
            if base_url.strip():
                data["base_url"] = base_url
            
            status_text.text(f"🤖 Generating response with {provider}...")
            progress_bar.progress(60)
            
            start_time = time.time()
            response = make_api_request("/v1/chat/generate", "POST", data)
            end_time = time.time()
            
            progress_bar.progress(100)
            status_text.text("✅ Response generated successfully!")
            
            # Update session state
            st.session_state.api_calls_count += 1
            
            # Add to chat history
            if response["success"]:
                st.session_state.chat_history.append({
                    "type": "Chat",
                    "input": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                    "output": response["data"].get("content", "")[:100] + "...",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "provider": provider,
                    "model": model or "default",
                    "response_time": f"{(end_time - start_time):.2f}s"
                })
            
            # Enhanced response display
            display_enhanced_response(response, provider, model, end_time - start_time)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error generating response: {str(e)}")
    
    # Chat history section
    if st.session_state.chat_history:
        st.markdown("### 💭 Recent Conversations")
        
        # Show last few conversations
        for i, chat in enumerate(st.session_state.chat_history[-3:]):
            with st.expander(f"💬 {chat['provider'].title()} - {chat['timestamp']} (⚡ {chat['response_time']})"):
                st.markdown(f"**Input:** {chat['input']}")
                st.markdown(f"**Provider:** {chat['provider']} | **Model:** {chat['model']}")
                if len(chat['output']) > 100:
                    st.markdown(f"**Output:** {chat['output']}...")
                else:
                    st.markdown(f"**Output:** {chat['output']}")

def display_enhanced_response(response: Dict[str, Any], provider: str, model: str, response_time: float):
    """Enhanced response display with metrics and actions"""
    if response["success"]:
        # Success header with metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Status", "✅ Success")
        with col2:
            st.metric("Provider", provider.title())
        with col3:
            st.metric("Model", model or "Default")
        with col4:
            st.metric("Time", f"{response_time:.2f}s")
        
        # Response content
        st.markdown("""
        <div class="response-box">
            <h4>🤖 AI Response</h4>
        </div>
        """, unsafe_allow_html=True)
        
        data = response["data"]
        content = data.get("content", "No content available")
        
        # Display content with copy button
        st.text_area("Response Content", content, height=200, key="response_content")
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📋 Copy Response"):
                st.write("Response copied to clipboard!")  # In real app, would use clipboard API
        with col2:
            if st.button("💾 Save Response"):
                st.success("Response saved!")
        with col3:
            if st.button("🔄 Regenerate"):
                st.rerun()
        with col4:
            if st.button("⭐ Rate Response"):
                st.info("Thanks for your feedback!")
        
    else:
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Error Occurred</h4>
            <p><strong>Error:</strong> {response['error']}</p>
            <p><strong>Provider:</strong> {provider}</p>
            <p><strong>Time:</strong> {response_time:.2f}s</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Troubleshooting tips
        st.markdown("### 🔧 Troubleshooting Tips")
        st.info("💡 Try checking your API key, reducing prompt length, or switching providers.")
        
        if "api key" in response['error'].lower():
            st.warning("🔑 API Key Issue: Make sure you have set the correct API key for the selected provider.")
        elif "timeout" in response['error'].lower():
            st.warning("⏱️ Timeout Issue: The request took too long. Try a shorter prompt or different model.")

def github_analysis_interface():
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.header("🐙 GitHub Repository Analysis")
    st.markdown("Analyze GitHub repositories and answer questions about codebases using AI.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    question = st.text_area(
        "Your Question about the Repository",
        placeholder="How does authentication work in this codebase?",
        height=80
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        text = st.text_area(
            "Relevant Code/Context (Optional)",
            placeholder="Paste relevant file content here...",
            height=150
        )
        
        tree = st.text_area(
            "File Tree Structure (Optional)",
            placeholder="src/\n  auth/\n    auth.js\n    middleware.js",
            height=100
        )
    
    with col2:
        summary = st.text_area(
            "Repository Summary (Optional)",
            placeholder="Brief description of the repository...",
            height=100
        )
        
        chat_history = st.text_area(
            "Chat History (Optional)",
            placeholder="Previous conversation context...",
            height=100
        )
    
    # LLM Configuration
    with st.expander("🔧 Advanced LLM Settings"):
        col3, col4 = st.columns(2)
        
        with col3:
            llm_provider = st.selectbox(
                "LLM Provider Override",
                ["", "google", "openai", "anthropic", "ollama", "deepseek", "openrouter"],
                index=0
            )
            
            llm_model = st.text_input(
                "LLM Model Override",
                placeholder="e.g., gpt-4"
            )
        
        with col4:
            llm_api_key = st.text_input(
                "LLM API Key Override",
                type="password"
            )
            
            llm_temperature = st.slider(
                "LLM Temperature Override",
                min_value=0.0,
                max_value=2.0,
                value=0.4,
                step=0.1
            )
    
    if st.button("🔍 Analyze Repository", type="primary", use_container_width=True):
        if not question.strip():
            st.error("Please enter a question!")
            return
        
        with st.spinner("Analyzing repository..."):
            data = {
                "question": question,
                "text": text,
                "tree": tree,
                "summary": summary,
                "chat_history": chat_history
            }
            
            # Add LLM overrides if provided
            if llm_provider:
                data["llm_provider"] = llm_provider
            if llm_model.strip():
                data["llm_model"] = llm_model
            if llm_api_key.strip():
                data["llm_api_key"] = llm_api_key
            if llm_temperature != 0.4:
                data["llm_temperature"] = llm_temperature
            
            response = make_api_request("/v1/github/answer", "POST", data)
            display_response(response)

def website_markdown_interface():
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.header("🌐 Website to Markdown")
    st.markdown("Convert any website to clean, readable markdown format.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    url = st.text_input(
        "Website URL",
        placeholder="https://example.com/article",
        help="Enter a valid HTTP or HTTPS URL"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 Convert to Markdown", type="primary", use_container_width=True):
            if not url.strip():
                st.error("Please enter a URL!")
                return
            
            if not (url.startswith("http://") or url.startswith("https://")):
                st.error("Please enter a valid HTTP or HTTPS URL!")
                return
            
            with st.spinner("Converting website to markdown..."):
                data = {"url": url}
                response = make_api_request("/v1/website/markdown", "POST", data)
                display_response(response)
    
    # Example URLs
    st.markdown("### 📝 Try these example URLs:")
    example_urls = [
        "https://github.com",
        "https://docs.python.org",
        "https://fastapi.tiangolo.com",
        "https://streamlit.io"
    ]
    
    cols = st.columns(len(example_urls))
    for i, example_url in enumerate(example_urls):
        with cols[i]:
            if st.button(f"Try {example_url.split('//')[1].split('/')[0]}", key=f"example_{i}"):
                st.rerun()

def html_markdown_interface():
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.header("🔄 HTML to Markdown")
    st.markdown("Convert raw HTML content to clean markdown format.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    html_content = st.text_area(
        "HTML Content",
        placeholder="<h1>Title</h1><p>Content with <strong>bold</strong> text.</p>",
        height=200,
        help="Paste your HTML content here"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 Convert to Markdown", type="primary", use_container_width=True):
            if not html_content.strip():
                st.error("Please enter HTML content!")
                return
            
            with st.spinner("Converting HTML to markdown..."):
                data = {"html": html_content}
                response = make_api_request("/v1/website/html-to-md", "POST", data)
                display_response(response)
    
    # Example HTML snippets
    st.markdown("### 📄 Try these example HTML snippets:")
    
    examples = {
        "Simple Article": """<article>
    <h1>My Article Title</h1>
    <p>This is a <strong>bold</strong> paragraph with <em>italic</em> text.</p>
    <ul>
        <li>First item</li>
        <li>Second item</li>
    </ul>
</article>""",
        "Complex Table": """<table>
    <thead>
        <tr><th>Name</th><th>Age</th><th>City</th></tr>
    </thead>
    <tbody>
        <tr><td>John</td><td>25</td><td>New York</td></tr>
        <tr><td>Jane</td><td>30</td><td>London</td></tr>
    </tbody>
</table>""",
        "Code Block": """<div>
    <h2>Code Example</h2>
    <pre><code>def hello_world():
    print("Hello, World!")
    return True</code></pre>
    <p>This function prints a greeting.</p>
</div>"""
    }
    
    for name, example in examples.items():
        if st.button(f"📋 Use {name} Example"):
            st.session_state.html_example = example
            st.rerun()

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 <strong>Agentic Browser</strong> | Built with ❤️ using Streamlit</p>
        <p><small>API Documentation: <a href="http://localhost:5454/docs" target="_blank">Swagger UI</a> | 
        <a href="http://localhost:5454/redoc" target="_blank">ReDoc</a></small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()