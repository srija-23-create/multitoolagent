import streamlit as st
from agent import run_agent

st.title("🤖 Multi Tool Agent")

prompt = st.chat_input("Ask anything")

if prompt:

    with st.chat_message("user"):
        st.write(prompt)

    result = run_agent(prompt)

    with st.chat_message("assistant"):
        st.write(result["answer"])

        with st.expander("Tool Calls"):
            for log in result["logs"]:
                st.write(log)