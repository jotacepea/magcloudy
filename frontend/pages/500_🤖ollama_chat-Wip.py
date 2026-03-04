import streamlit as st
import ollama
import httpx
from pages.common.globalconf import pageconfig, theend

# Initialize page configuration
pageconfig()

st.title("🤖 AI Chat (Ollama)")
st.markdown("Chat with your local Ollama service.")

# Configuration for Ollama connection
# We could make this configurable through a sidebar if needed
OLLAMA_HOST = st.sidebar.text_input("Ollama Host", value="http://host.docker.internal:11434")

def get_models():
    try:
        # Check connection first
        try:
            httpx_response = httpx.get(OLLAMA_HOST)
            if httpx_response.status_code != 200:
                st.error(f"Ollama connection error at {OLLAMA_HOST}: {httpx_response.text}")
                return []
        except Exception as conn_err:
            st.error(f"Connection failed to {OLLAMA_HOST}: {conn_err}")
            return []
        print(httpx_response.text)
        
        # Get models
        client = ollama.Client(host=OLLAMA_HOST)
        thelist = client.list()
        
        # Accessing the models from the ListResponse object
        # Each model in the list has a 'model' attribute containing its name
        result = [model.model for model in thelist.models]
        return result
    except Exception as e:
        st.error(f"Error parsing Ollama models: {e}")
        return []

# Sidebar for model selection
available_models = get_models()
if available_models:
    selected_model = st.sidebar.selectbox("Select Model", available_models)
else:
    st.sidebar.warning("No models found. Make sure Ollama is running.")
    selected_model = None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    if not selected_model:
        st.error("Please select a model first.")
    else:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                client = ollama.Client(host=OLLAMA_HOST)
                response = client.chat(
                    model=selected_model,
                    messages=st.session_state.messages,
                    stream=True,
                )
                
                for chunk in response:
                    full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error communicating with Ollama: {e}")

# Footer/Sidebar Info
theend()
