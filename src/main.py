"""Main application file for the chat interface."""
import streamlit as st
from utils import (
    initialize_session_state,
    add_message,
    get_chat_history,
    clear_chat_history
)
from azure_openai_service import azure_openai_service

def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="Chat Bot UI",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded",
    )

def setup_sidebar():
    """Setup the sidebar with controls."""
    with st.sidebar:
        st.title("Chat Bot Settings")
        
        # Display Azure OpenAI status
        if azure_openai_service and azure_openai_service.is_configured():
            st.success("🟢 Azure OpenAI Connected")
        else:
            st.error("🔴 Azure OpenAI Not Connected")
        
        st.markdown("---")
        
        if st.button("Clear Chat"):
            clear_chat_history()
            
        st.markdown("---")
        st.markdown("""
        ### About
        This is an AI chat interface powered by:
        - Azure OpenAI
        - Streamlit
        - Python
        - ❤️
        """)

def display_chat_history():
    """Display the chat history."""
    for message in get_chat_history():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and generate response."""
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response using Azure OpenAI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if azure_openai_service and azure_openai_service.is_configured():
                    # Get conversation history for context
                    chat_history = get_chat_history()
                    response = azure_openai_service.generate_response(prompt, chat_history)
                else:
                    response = "I'm sorry, Azure OpenAI is not properly configured. Please check your settings."
                
                st.markdown(response)
                add_message("assistant", response)

def main():
    """Main application function."""
    setup_page()
    initialize_session_state()
    setup_sidebar()
    
    st.title("🤖 AI Chat Assistant")
    st.markdown("*Powered by Azure OpenAI*")
    st.markdown("---")
    
    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    main()