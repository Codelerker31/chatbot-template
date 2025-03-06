import streamlit as st
import json
import os
from pathlib import Path

# We'll use this as a fallback if cookies don't work
def get_local_storage_path():
    """Get path to local storage file"""
    # Store in user's home directory
    home = Path.home()
    config_dir = home / ".streamlit_chatbot"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "api_keys.json"

def get_api_keys():
    """Get API keys from session state or local file"""
    api_keys = {}
    
    # First check session state (for current session)
    if "api_keys" in st.session_state:
        api_keys = st.session_state.api_keys
        return api_keys
    
    # Then try to load from file as fallback
    try:
        file_path = get_local_storage_path()
        if file_path.exists():
            with open(file_path, "r") as f:
                api_keys = json.load(f)
                # Also store in session state for faster access
                st.session_state.api_keys = api_keys
    except Exception as e:
        st.error(f"Error loading API keys: {str(e)}")
    
    return api_keys

def save_api_key(provider, key):
    """Save API key to session state and local file"""
    # Save to session state
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {}
    
    st.session_state.api_keys[provider] = key
    
    # Also save to file for persistence
    try:
        file_path = get_local_storage_path()
        api_keys = get_api_keys()  # Get existing keys
        api_keys[provider] = key  # Update with new key
        
        with open(file_path, "w") as f:
            json.dump(api_keys, f)
        
        st.success(f"{provider.capitalize()} API key saved successfully!")
        return True
    except Exception as e:
        st.error(f"Error saving API key: {str(e)}")
        st.info("Your API key is saved for this session only.")
        return False 