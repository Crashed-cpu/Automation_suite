import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import agentic_assistant
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.agentic_ai.agentic_assistant import AgenticAssistant

# Load environment variables
load_dotenv()

# Initialize the agentic assistant with error handling
@st.cache_resource
def get_assistant():
    try:
        return AgenticAssistant()
    except Exception as e:
        return None

def show_agentic_assistant():
    """Display the agentic assistant UI."""
    # Set up the Streamlit UI
    st.title("🤖 Agentic Assistant with Tools")
    st.markdown("""
    This is an agentic AI assistant that can interact with tools to perform tasks.

    **Available Tools:**
    - Project Scanner: Scans directories and summarizes README files

    **Example Queries:**
    - "Scan my project folder at 'path/to/folder' and summarize the README files"
    - "What's in the documentation for my project at 'path/to/project'?"
    """)

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your agentic assistant. How can I help you today?"}
        ]

    # Check if assistant is initialized
    assistant = get_assistant()
    if assistant is None:
        st.error("Failed to initialize the AI assistant. Please ensure you have set up your API keys in the .env file")
        return

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def process_agentic_input(prompt: str):
    """Process user input and generate a response using the agent.
    
    Args:
        prompt: The user's input message
    """
    # Add user message to chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get the assistant
        assistant = get_assistant()
        if assistant is None:
            st.error("Failed to initialize the AI assistant. Please check your API key in the .env file")
            return
            
        # Process the input with the assistant
        try:
            # This would be replaced with actual agent processing
            response = f"Processing your request: {prompt}"
            
            # Simulate stream of response with milliseconds delay
            for chunk in response.split():
                full_response += chunk + " "
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
                import time
                time.sleep(0.05)
            
            # Update the final message
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.error(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
