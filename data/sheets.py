# data/sheets.py
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import json

import streamlit as st


load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def get_sheets_client():
    if "GOOGLE_CREDENTIALS" in st.secrets:
        # It's stored as a string - parse it carefully
        creds_raw = st.secrets["GOOGLE_CREDENTIALS"]
        
        # If it's already a dict (TOML table format)
        if isinstance(creds_raw, dict):
            creds_dict = dict(creds_raw)
        else:
            # It's a string - fix \n and parse
            creds_dict = json.loads(
                str(creds_raw).replace("\\n", "\n")
            )
        
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )
    else:
        # Local
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )
    return gspread.authorize(creds)


def get_secret(key: str) -> str:
    # Works both locally and on Streamlit Cloud
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

def load_table(sheet_name: str) -> pd.DataFrame:
    client = get_sheets_client()
    spreadsheet = client.open_by_key(get_secret("GOOGLE_SHEETS_ID"))
    worksheet = spreadsheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def get_table_schema(sheet_name: str) -> str:
    """Returns a human readable description of each table"""
    schemas = {
        "Sales_Orders": """
            Table: Sales_Orders
            Description: Contains all customer orders from the ERP system
            Key Columns: Order Number, Order Date, Status, Customer ID,
                        Customer Name, Item Description, Quantity, 
                        Unit Price, Total Amount, Fulfillment Status
            Status Values: BOOKED, CLOSED, PENDING, CANCELLED
        """,
        "HR_Employees": """
            Table: HR_Employees  
            Description: Contains all employee records across departments
            Key Columns: Employee ID, Full Name, Department, Job Title,
                        Manager Name, Hire Date, Employment Status, Salary
            Departments: Sales, HR, Finance, Operations, IT, Executive
        """,
        "Customer_Details": """
            Table: Customer_Details
            Description: Contains customer account and contact information
            Key Columns: Customer ID, Customer Name, Contact Person,
                        Email, Phone, Billing Address, Account Status,
                        Credit Limit, Assigned Sales Rep
        """
    }
    return schemas.get(sheet_name, "Schema not found")


def filter_table(df, filters: dict) -> pd.DataFrame:
    """
    filters = {"Status": "BOOKED", "Customer Name": "Acme Corp"}
    """
    result = df.copy()
    for column, value in filters.items():
        result = result[
            result[column].str.upper() == value.upper()
        ]
    return result