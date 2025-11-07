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
        
        # System Message Configuration
        st.subheader("🎯 AI Behavior")
        
        # Initialize system message in session state if not present
        if "custom_system_message" not in st.session_state:
            # Use the service's default system message
            if azure_openai_service:
                st.session_state.custom_system_message = azure_openai_service.system_message
            else:
                st.session_state.custom_system_message = "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
        
        # Text area for custom system message
        new_system_message = st.text_area(
            "System Message:",
            value=st.session_state.custom_system_message,
            height=120,
            help="Define the AI's behavior, personality, and restrictions. For example: 'You are an AI assistant that only answers questions about Kubernetes.'"
        )
        
        # Update system message if changed
        if new_system_message != st.session_state.custom_system_message:
            st.session_state.custom_system_message = new_system_message
            # Update the service's system message
            if azure_openai_service:
                azure_openai_service.system_message = new_system_message
            st.success("✅ System message updated!")
        
        # Quick preset buttons
        st.markdown("**Quick Presets:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🤖 General", use_container_width=True):
                preset_msg = "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
                st.session_state.custom_system_message = preset_msg
                if azure_openai_service:
                    azure_openai_service.system_message = preset_msg
                st.rerun()
        
        with col2:
            if st.button("☸️ Kubernetes", use_container_width=True):
                preset_msg = "You are an AI assistant specialized in Kubernetes. Only answer questions related to Kubernetes, container orchestration, Docker, and cloud-native technologies. If asked about unrelated topics, politely redirect the conversation back to Kubernetes."
                st.session_state.custom_system_message = preset_msg
                if azure_openai_service:
                    azure_openai_service.system_message = preset_msg
                st.rerun()
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("☁️ Cloud", use_container_width=True):
                preset_msg = "You are an AI assistant specialized in cloud computing. Focus on topics related to AWS, Azure, Google Cloud, cloud architecture, DevOps, and infrastructure. Provide practical, actionable advice for cloud solutions."
                st.session_state.custom_system_message = preset_msg
                if azure_openai_service:
                    azure_openai_service.system_message = preset_msg
                st.rerun()
        
        with col4:
            if st.button("💻 Code", use_container_width=True):
                preset_msg = "You are an AI programming assistant. Help with coding questions, provide code examples, explain programming concepts, and assist with debugging. Focus on best practices and clean, efficient code."
                st.session_state.custom_system_message = preset_msg
                if azure_openai_service:
                    azure_openai_service.system_message = preset_msg
                st.rerun()
        
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