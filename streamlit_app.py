import streamlit as st

# This must be the first Streamlit command
st.set_page_config(page_title="Multi-Provider Chatbot", layout="wide")

from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

# Components
from components.auth import render_auth
from components.sidebar import render_sidebar
from components.chat_interface import render_chat
from components.settings import render_settings

# Utilities
from utils.supabase_client import init_supabase
from utils.local_storage import get_api_keys, save_api_key
from utils.session_state import initialize_session_state

# Initialize session state
initialize_session_state()

# Initialize Supabase client
supabase = init_supabase()

# App title
st.title("💬 Multi-Provider Chatbot")
st.write(
    "Chat with various AI models from OpenAI, Anthropic, Google, and Perplexity. "
    "Your API keys are stored locally on your device."
)

# Authentication section
user = render_auth(supabase)

# If user is authenticated, show the main app
if user:
    # Sidebar for chat management
    selected_chat, selected_provider, selected_model = render_sidebar(supabase, user)
    
    # Main content area - split into two columns
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Render chat interface
        if "selected_chat" in st.session_state:
            selected_chat = st.session_state.selected_chat
            render_chat(
                chat_id=selected_chat["id"],
                provider=selected_chat["provider"],
                model=selected_chat["model"]
            )
        else:
            st.info("Select a chat from the sidebar or create a new one.")
    
    with col2:
        # API settings
        render_settings()
else:
    st.info("Please log in or sign up to use the chatbot.")
