import openai
from anthropic import Anthropic
import google.generativeai as genai
import requests

def get_chat_completion(provider, model, messages, api_key):
    """
    Get chat completion from various providers, supporting any model name
    
    Args:
        provider (str): AI provider (openai, anthropic, google, perplexity, etc.)
        model (str): Any model name supported by the provider
        messages (list): Chat history in the format [{"role": "user", "content": "..."}, ...]
        api_key (str): API key for the selected provider
        
    Returns:
        str: AI response
    """
    
    if provider == "openai":
        return get_openai_completion(model, messages, api_key)
    elif provider == "anthropic":
        return get_anthropic_completion(model, messages, api_key)
    elif provider == "google":
        return get_google_completion(model, messages, api_key)
    elif provider == "perplexity":
        return get_perplexity_completion(model, messages, api_key)
    elif provider == "meta" or provider == "llama":
        return get_meta_completion(model, messages, api_key)
    elif provider == "mistral":
        return get_mistral_completion(model, messages, api_key)
    else:
        # Allow for custom providers by defaulting to OpenAI-compatible API
        return get_generic_completion(provider, model, messages, api_key)

def get_openai_completion(model, messages, api_key):
    """Get completion from OpenAI"""
    client = openai.OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    
    return response.choices[0].message.content

def get_anthropic_completion(model, messages, api_key):
    """Get completion from Anthropic"""
    client = Anthropic(api_key=api_key)
    
    # Convert messages to Anthropic format
    system_message = ""
    human_messages = []
    
    for msg in messages:
        if msg["role"] == "system":
            system_message = msg["content"]
        elif msg["role"] == "user":
            human_messages.append(msg["content"])
        # Assistant messages are included implicitly in the response
    
    # For demonstration, we'll just use the last user message
    if not human_messages:
        raise ValueError("No user messages found")
    
    response = client.messages.create(
        model=model,
        system=system_message,
        messages=[{"role": "user", "content": human_messages[-1]}],
        max_tokens=1024
    )
    
    return response.content[0].text

def get_google_completion(model, messages, api_key):
    """Get completion from Google Gemini"""
    genai.configure(api_key=api_key)
    
    # Convert messages to Gemini format
    gemini_messages = []
    for msg in messages:
        if msg["role"] == "user":
            gemini_messages.append({"role": "user", "parts": [{"text": msg["content"]}]})
        elif msg["role"] == "assistant":
            gemini_messages.append({"role": "model", "parts": [{"text": msg["content"]}]})
    
    model = genai.GenerativeModel(model)
    response = model.generate_content(gemini_messages)
    
    return response.text

def get_perplexity_completion(model, messages, api_key):
    """Get completion from Perplexity"""
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Convert messages format if needed
    data = {
        "model": model,
        "messages": messages
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    return response.json()["choices"][0]["message"]["content"]

def get_meta_completion(model, messages, api_key):
    # Implementation for meta completion
    pass

def get_mistral_completion(model, messages, api_key):
    # Implementation for mistral completion
    pass

def get_generic_completion(provider, model, messages, api_key):
    # Implementation for generic completion
    pass 