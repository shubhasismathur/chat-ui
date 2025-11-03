"""Main application file for the chat interface."""
import streamlit as st
from utils import (
    initialize_session_state,
    add_message,
    get_chat_history,
    clear_chat_history
)

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
        if st.button("Clear Chat"):
            clear_chat_history()
        st.markdown("---")
        st.markdown("""
        ### About
        This is a chat interface built with:
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
        
        # Here you would typically make an API call to get the bot's response
        # For now, we'll just echo the message
        with st.chat_message("assistant"):
            response = f"You said: {prompt}"
            st.markdown(response)
            add_message("assistant", response)

def main():
    """Main application function."""
    setup_page()
    initialize_session_state()
    setup_sidebar()
    
    st.title("💬 Chat Bot UI")
    st.markdown("---")
    
    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    main()