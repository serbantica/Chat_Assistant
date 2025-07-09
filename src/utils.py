import streamlit as st
from typing import List, Dict

def setup_page_config():
    """Set up Streamlit page configuration"""
    st.set_page_config(
        page_title="Business Assistant",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    
    .assistant-message {
        background-color: #F1F8E9;
        border-left: 4px solid #4CAF50;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .quick-prompt-btn {
        font-size: 0.8rem !important;
        padding: 0.3rem 0.8rem !important;
        margin: 0.2rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def display_chat_history(messages: List[Dict[str, str]]):
    """Display chat history in the main area"""
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_input() -> str:
    """Get user input from chat input widget"""
    # Check if there's a quick prompt selected
    if "user_input" in st.session_state:
        user_input = st.session_state.user_input
        del st.session_state.user_input  # Remove after using
        return user_input
    
    # Regular chat input
    return st.chat_input("Ask me anything about your business decisions...")

def format_business_metrics(data: Dict) -> str:
    """Format business metrics for display"""
    formatted = "📊 **Business Metrics Summary:**\n\n"
    for key, value in data.items():
        formatted += f"• **{key}**: {value}\n"
    return formatted

def create_quick_analysis_template(analysis_type: str) -> str:
    """Create template prompts for different types of business analysis"""
    templates = {
        "swot": "Help me conduct a SWOT analysis for my business. I need to identify Strengths, Weaknesses, Opportunities, and Threats.",
        "market": "I need help analyzing my target market. Can you guide me through market size, competition, and customer segments?",
        "financial": "Help me understand key financial metrics I should track and how to improve my business's financial health.",
        "marketing": "I need a marketing strategy review. Help me evaluate my current approach and suggest improvements.",
        "operations": "Help me analyze my business operations and identify areas for efficiency improvements."
    }
    return templates.get(analysis_type, "")

def validate_environment() -> Dict[str, bool]:
    """Validate that all required environment variables are set"""
    import os
    
    required_vars = ["OPENAI_API_KEY"]
    validation = {}
    
    for var in required_vars:
        validation[var] = bool(os.getenv(var))
    
    return validation

def format_error_message(error_type: str, details: str = "") -> str:
    """Format error messages consistently"""
    error_formats = {
        "api_key": "🔑 **API Key Error**: Please ensure your OpenAI API key is set correctly in the .env file.",
        "connection": "🌐 **Connection Error**: Unable to connect to OpenAI. Please check your internet connection.",
        "rate_limit": "⏳ **Rate Limit**: Too many requests. Please wait a moment before trying again.",
        "general": f"❌ **Error**: {details}"
    }
    
    return error_formats.get(error_type, error_formats["general"])

def get_business_prompt_suggestions() -> List[str]:
    """Get a list of business-related prompt suggestions"""
    return [
        "How can I improve my customer retention rate?",
        "What pricing strategy should I consider for my product?",
        "Help me create a go-to-market strategy",
        "How do I scale my business operations?",
        "What are the key KPIs I should track?",
        "How can I improve my team's productivity?",
        "What should I consider before expanding internationally?",
        "Help me analyze my competition",
        "How can I improve my cash flow management?",
        "What digital marketing strategies work best for my industry?"
    ]
