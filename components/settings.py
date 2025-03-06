import streamlit as st
from utils.local_storage import get_api_keys, save_api_key

def render_settings():
    """Render API settings panel"""
    
    st.subheader("API Settings")
    st.write("Your API keys are stored locally on your device and never sent to our servers.")
    
    # Get existing API keys
    api_keys = get_api_keys()
    
    # API key inputs
    with st.expander("OpenAI API Key", expanded=True):
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=api_keys.get("openai", ""),
            help="Get your API key from https://platform.openai.com/account/api-keys"
        )
        if st.button("Save OpenAI Key"):
            save_api_key("openai", openai_key)
    
    with st.expander("Anthropic API Key"):
        anthropic_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=api_keys.get("anthropic", ""),
            help="Get your API key from https://console.anthropic.com/settings/keys"
        )
        if st.button("Save Anthropic Key"):
            save_api_key("anthropic", anthropic_key)
    
    with st.expander("Google AI API Key"):
        google_key = st.text_input(
            "Google AI API Key",
            type="password",
            value=api_keys.get("google", ""),
            help="Get your API key from Google AI Studio"
        )
        if st.button("Save Google Key"):
            save_api_key("google", google_key)
    
    with st.expander("Perplexity API Key"):
        perplexity_key = st.text_input(
            "Perplexity API Key",
            type="password",
            value=api_keys.get("perplexity", ""),
            help="Get your API key from https://www.perplexity.ai/settings/api"
        )
        if st.button("Save Perplexity Key"):
            save_api_key("perplexity", perplexity_key) 