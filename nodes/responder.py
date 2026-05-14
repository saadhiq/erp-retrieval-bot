# nodes/responder.py
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

import streamlit as st

def get_secret(key: str) -> str:
    # Works both locally and on Streamlit Cloud
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

# load_dotenv()


llm = ChatGroq(
    api_key=get_secret("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

RESPONDER_PROMPT = """
You are a helpful ERP data assistant.
Answer the user question using ONLY the data provided below.

{table_context}

User Question: {question}

Provide a clear and concise answer based on the data above.
If the answer is not found in the data, say "I could not find that information".
"""

def build_table_context(retrieved_data: dict) -> str:
    context = ""
    for table_name, table_info in retrieved_data.items():
        context += f"""
        Table: {table_name}
        {table_info['schema']}
        Total Rows Found: {table_info['row_count']}
        Data:
        {json.dumps(table_info['data'], indent=2)}
        """
    return context

def responder_node(state: dict) -> dict:
    question = state["question"]
    retrieved_data = state["retrieved_data"]
    
    # Build context from retrieved data
    table_context = build_table_context(retrieved_data)
    
    # Call LLM with schema + data + question
    response = llm.invoke(
        RESPONDER_PROMPT.format(
            table_context=table_context,
            question=question
        )
    )
    
    state["final_answer"] = response.content
    return state