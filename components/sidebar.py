import streamlit as st
import time
import uuid

def render_sidebar(supabase, user):
    """Render sidebar with chat management"""
    
    st.sidebar.title("Chats")
    
    # Debug user ID
    st.sidebar.write(f"User ID: {user.id}")
    st.sidebar.write(f"User ID type: {type(user.id)}")
    
    # Fetch user's chats from Supabase
    try:
        chats_response = supabase.table("chats").select("*").eq("user_id", user.id).execute()
        # Make sure we have the correct format
        chats_data = chats_response.data if hasattr(chats_response, 'data') else []
    except Exception as e:
        st.sidebar.error(f"Error loading chats: {str(e)}")
        chats_data = []  # Just store the data directly as a list
    
    # New chat button
    if st.sidebar.button("+ New Chat"):
        # Get provider and model for new chat
        new_provider = "openai"  # Default provider
        new_model = "gpt-3.5-turbo"  # Default model
        
        # Create a new chat in Supabase
        new_chat = {
            "user_id": user.id,
            "title": f"New Chat {time.strftime('%Y-%m-%d %H:%M')}",
            "provider": new_provider,
            "model": new_model,
            "created_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            result = supabase.table("chats").insert(new_chat).execute()
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error creating chat: {str(e)}")
    
    # Display existing chats
    selected_chat_id = None
    selected_provider = None
    selected_model = None
    
    if chats_data:
        st.sidebar.write("Your Chats:")
        for chat in chats_data:
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                if st.button(chat["title"], key=f"chat_{chat['id']}"):
                    selected_chat_id = chat["id"]
                    selected_provider = chat["provider"]
                    selected_model = chat["model"]
                    
                    # Store in session state
                    st.session_state.selected_chat = chat
            
            with col2:
                if st.button("⚙️", key=f"settings_{chat['id']}"):
                    st.session_state.edit_chat = chat
    else:
        st.sidebar.info("No chats yet. Create a new one!")
    
    # Chat editing modal (could be implemented with a custom component or a separate section)
    if "edit_chat" in st.session_state:
        chat = st.session_state.edit_chat
        
        st.sidebar.subheader("Edit Chat")
        
        new_title = st.sidebar.text_input("Title", value=chat["title"])
        
        # Provider selection
        provider_options = ["openai", "anthropic", "google", "perplexity", "meta", "mistral"]
        new_provider = st.sidebar.selectbox(
            "Provider",
            provider_options,
            index=provider_options.index(chat["provider"]) if chat["provider"] in provider_options else 0
        )
        
        # Model suggestions (but allow free text input)
        suggested_models = get_model_options(new_provider)
        with st.sidebar.expander("View suggested models"):
            st.write(", ".join(suggested_models))
        
        # Text input for any model name
        new_model = st.sidebar.text_input(
            "Model Name", 
            value=chat["model"],
            help="You can enter any model name supported by the provider"
        )
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Save"):
                # Update chat in Supabase
                supabase.table("chats").update({
                    "title": new_title,
                    "provider": new_provider,
                    "model": new_model
                }).eq("id", chat["id"]).execute()
                
                del st.session_state.edit_chat
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                del st.session_state.edit_chat
                st.rerun()
            
        if st.sidebar.button("Delete Chat", type="primary", use_container_width=True):
            supabase.table("chats").delete().eq("id", chat["id"]).execute()
            del st.session_state.edit_chat
            if "selected_chat" in st.session_state and st.session_state.selected_chat["id"] == chat["id"]:
                del st.session_state.selected_chat
            st.rerun()
    
    return selected_chat_id, selected_provider, selected_model

def get_model_options(provider):
    """Get suggested models for a provider (informational only)"""
    if provider == "openai":
        return [
            # Latest models
            "gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "o1-preview", "o3-mini",
            # Core models
            "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo",
            # Dated versions
            "gpt-4o-2024-05-13", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"
        ]
    elif provider == "anthropic":
        return [
            # Latest Claude 3.5 models
            "claude-3-5-sonnet-20241022", "claude-3-5-sonnet-20240620", 
            "claude-3-5-haiku-20241022",
            # Claude 3 models
            "claude-3-opus-20240229", "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307",
            # Legacy models
            "claude-2.1", "claude-2", "claude-instant-1.2"
        ]
    elif provider == "google":
        return [
            "gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro", "gemini-ultra"
        ]
    elif provider == "perplexity":
        return [
            "sonar", "sonar-pro", "sonar-reasoning", "sonar-reasoning-pro"
        ]
    elif provider == "meta" or provider == "llama":
        return [
            "meta-llama/Llama-3.3-70B-Instruct-Turbo", 
            "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", 
            "meta-llama/Meta-Llama-3-70B-Instruct-Turbo"
        ]
    elif provider == "mistral":
        return [
            "mistralai/Mistral-Small-24B-Instruct-2501",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "mistral", "mistral-medium", "mistral-large"
        ]
    return [] 