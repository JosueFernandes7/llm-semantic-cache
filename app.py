import streamlit as st
from core.settings import redis_config
from services.ollama import generate_response
from services.vectorstore import create_vector_store, save_doc, get_similar_answer
from components.ui import setup_sidebar, display_chat

vector_store = create_vector_store(redis_config)

st.title("💬 Ollama Webchat")

selected_model, temperature = setup_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

display_chat(st.session_state.messages)

if prompt := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    similar = get_similar_answer(vector_store, prompt, 0.85)
    if similar:
        st.session_state.messages.append({"role": "assistant", "content": similar})
        with st.chat_message("assistant"):
            st.markdown(similar)
    else:
        with st.spinner("Gerando resposta..."):
            full_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
            full_prompt += "\nAssistente:"
            response = generate_response(selected_model, full_prompt)
            save_doc(vector_store, prompt, response)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
