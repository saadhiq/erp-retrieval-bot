# nodes/router.py
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

ROUTER_PROMPT = """
You are a data routing assistant for an ERP system.
You have three tables with these EXACT column names:

Sales_Orders columns: Order Number, Order Date, Status, 
    Customer ID, Customer Name, Item Code, Item Description,
    Quantity, Unit Price ($), Total Amount ($), 
    Requested Ship Date, Fulfillment Status, Sales Rep ID

HR_Employees columns: Employee ID, Full Name, Department, 
    Job Title, Manager Name, Hire Date, 
    Employment Status, Location, Business Unit, Salary ($)

Customer_Details columns: Customer ID, Customer Name, 
    Account Number, Contact Person, Email, Phone, 
    Billing Address, Shipping Address, Customer Segment, 
    Account Status, Credit Limit ($), Assigned Sales Rep

IMPORTANT: When building filters, use ONLY the exact 
column names listed above!


Given the user question, identify:
1. Which tables are needed
2. What filters should be applied to each table

Respond ONLY in JSON format like this:

{{
    "tables": ["Sales_Orders"],
    "reason": "Question is about order status",
    "filters": {{
        "Sales_Orders": {{
            "Status": "BOOKED"
        }}
    }}
}}

If no filters needed, return "filters": {{}}

User Question: {question}
"""

def router_node(state: dict) -> dict:
    question = state["question"]
    
    response = llm.invoke(
        ROUTER_PROMPT.format(question=question)
    )
    
    result = json.loads(response.content)
    
    state["tables_needed"] = result["tables"]
    state["routing_reason"] = result["reason"]
    state["filters"] = result.get("filters", {})  # ← new!
    
    return state