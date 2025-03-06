import streamlit as st
from supabase import create_client

@st.cache_resource
def init_supabase():
    """Initialize Supabase client"""
    
    # Get Supabase credentials from Streamlit secrets
    supabase_url = st.secrets["supabase"]["url"]
    supabase_key = st.secrets["supabase"]["key"]
    
    # Create Supabase client
    client = create_client(supabase_url, supabase_key)
    
    return client 