import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    
    if "user" not in st.session_state:
        st.session_state.user = None
        
    if "selected_chat" not in st.session_state:
        st.session_state.selected_chat = None 