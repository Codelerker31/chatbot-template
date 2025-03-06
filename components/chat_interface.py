import streamlit as st
from utils.api_clients import get_chat_completion
from utils.local_storage import get_api_keys

def render_chat(chat_id, provider, model):
    """Render chat interface for a specific chat"""
    
    # Create a unique key for this chat's messages in session state
    chat_messages_key = f"messages_{chat_id}"
    
    # Initialize chat history in session state if it doesn't exist
    if chat_messages_key not in st.session_state:
        st.session_state[chat_messages_key] = []
        
        # Try to load messages from Supabase (commented out until fully implemented)
        # try:
        #     messages = supabase.table("messages").select("*").eq("chat_id", chat_id).order("created_at").execute()
        #     if hasattr(messages, 'data') and messages.data:
        #         st.session_state[chat_messages_key] = [{"role": m["role"], "content": m["content"]} for m in messages.data]
        # except Exception as e:
        #     st.error(f"Error loading messages: {str(e)}")
    
    # Get API keys from local storage
    api_keys = get_api_keys()
    api_key = api_keys.get(provider)
    
    if not api_key:
        st.warning(f"Please add your {provider.capitalize()} API key in the settings panel on the right.")
        st.info("After adding your API key, click 'Save' to store it for future use.")
        return
    
    # Create a container for messages with fixed height and scrolling
    message_container = st.container(height=500, border=False)
    
    # Create a separate container for the input at the bottom
    input_container = st.container()
    
    # Process user input from the bottom container first
    with input_container:
        prompt = st.chat_input(f"Message {provider}/{model}...")
        
        if prompt:
            # Add user message to chat history
            st.session_state[chat_messages_key].append({"role": "user", "content": prompt})
            
            # Process response (outside of both containers)
            try:
                # Get response from the selected AI provider
                response = get_chat_completion(
                    provider=provider,
                    model=model,
                    messages=st.session_state[chat_messages_key],
                    api_key=api_key
                )
                
                # Add assistant response to chat history
                st.session_state[chat_messages_key].append({
                    "role": "assistant",
                    "content": response
                })
                
                # Force a rerun to display new messages
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                # Keep the error visible but don't add to chat history
    
    # Display chat messages in the message container
    with message_container:
        for message in st.session_state[chat_messages_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Save messages to Supabase (commented out until fully implemented)
    # try:
    #     # Save user message
    #     supabase.table("messages").insert({
    #         "chat_id": chat_id,
    #         "role": "user",
    #         "content": prompt,
    #         "created_at": time.strftime('%Y-%m-%d %H:%M:%S')
    #     }).execute()
    #     
    #     # Save assistant message
    #     supabase.table("messages").insert({
    #         "chat_id": chat_id,
    #         "role": "assistant",
    #         "content": response,
    #         "created_at": time.strftime('%Y-%m-%d %H:%M:%S')
    #     }).execute()
    # except Exception as e:
    #     st.error(f"Error saving messages: {str(e)}") 