import streamlit as st

def setup_sidebar():
    st.sidebar.title("Configurações")
    model = st.sidebar.selectbox("Modelo:", ["llama3.1:8b", "mistral:7b", "granite3-dense:8b"])
    temperature = st.sidebar.slider("Temperatura", 0.0, 1.5, 1.0, 0.1)
    return model, temperature

def display_chat(messages):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
