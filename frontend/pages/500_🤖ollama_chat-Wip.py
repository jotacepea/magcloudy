import streamlit as st
import ollama
import httpx
import time
from pages.common.globalconf import pageconfig, theend

# Initialize page configuration
pageconfig()

st.title("🤖 AI Chat (Ollama)")
st.markdown("Chat with your local Ollama service.")

# Configuration for Ollama connection
# We could make this configurable through a sidebar if needed
OLLAMA_HOST = st.sidebar.text_input("Ollama Host", value="http://host.docker.internal:11434")

def get_education_context_md(path_to_md_file):
    try:
        with open(path_to_md_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading education context file: {e}. Note, we will use a default context --> 'You are a helpful assistant.'")
        return "You are a helpful assistant. And talk like a cawboy."


context_file = st.sidebar.text_input("Education Context MD Path", value="AGENT.md")
system_instructions = get_education_context_md('llm/' + context_file)


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

def get_education_context_md(path_to_md_file):
    try:
        with open(path_to_md_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading education context file: {e}")
        return "You are a helpful assistant."

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "time_spent" in message:
            st.caption(f"⏱️ Generated in {message['time_spent']:.2f} seconds")

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
                
                # Prepend system role to messages sent to Ollama
                messages_with_system = [{"role": "system", "content": system_instructions}] + st.session_state.messages
                
                start_time = time.time()
                
                response = client.chat(
                    model=selected_model,
                    messages=messages_with_system,
                    stream=True,
                )
                
                for chunk in response:
                    full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                
                end_time = time.time()
                time_spent = end_time - start_time
                
                message_placeholder.markdown(full_response)
                st.caption(f"⏱️ Generated in {time_spent:.2f} seconds")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response,
                    "time_spent": time_spent
                })
            except Exception as e:
                st.error(f"Error communicating with Ollama: {e}")

# Footer/Sidebar Info
theend()
