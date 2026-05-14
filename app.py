# app.py
import streamlit as st
from main import ask

# Page config
st.set_page_config(
    page_title="ERP Assistant",
    page_icon="🤖"
)

st.title("🤖 ERP Data Assistant")
st.caption("Ask questions about Sales Orders, HR, and Customers")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something about your ERP data..."):
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask(prompt)
        st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })