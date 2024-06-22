import os
from pathlib import Path
from typing import Optional

import streamlit as st

from config import Config
from text_helper import TextHelper, load_embedding_model

load_embedding_model(model_name=Config.EMBEDDING_MODEL_NAME)

title = "RAG Bot"
init_msg = "Hello, I'm your assistant. Fill the knowledge base"
model_name = Config.MODEL

ollama_api_base_url = Config.OLLAMA_API_BASE_URL

print(f"Using model: {model_name}")
print(f"Using Ollama base URL: {ollama_api_base_url}")

st.set_page_config(page_title=title)

with st.sidebar:
    st.title(title)
    st.write('This chatbot with Knowledge Input and lets you ask questions on it.')
    docs = st.sidebar.text_area("text")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": init_msg}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    from streamlit_js_eval import streamlit_js_eval
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
    st.session_state.messages = [{"role": "assistant", "content": init_msg}]


st.sidebar.button('Reset', on_click=clear_chat_history)

# User-provided prompt
if prompt := st.chat_input(disabled=False, placeholder="What do you want to know from the base?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    if docs is "":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                placeholder = st.empty()
                full_response = 'Knowledge base should be exist before you can ask questions on it 😟. Please give a knowledge base'
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                question = dict(st.session_state.messages[-1]).get('content')
                text_helper = TextHelper(
                    ollama_api_base_url=ollama_api_base_url,
                    model_name=model_name
                )
                response = text_helper.ask(
                    docs=docs,
                    question=question
                )
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
