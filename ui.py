import torch
torch.classes.__path__ = []

import streamlit as st
import policy_assistant

st.title('Kelewele AI')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_question := st.chat_input("Which policy do you want to know about today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_question)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})
    response = policy_assistant.answer_and_sources(user_question)
    if response:
          with st.chat_message("assistant"):
                st.markdown(response['answer'])
                if response['answer'] != "I cannot find this information in the policy.":
                    st.markdown('Sources')
                    st.markdown(response['sources'])
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
# 1a1c24
# [#0e1117]