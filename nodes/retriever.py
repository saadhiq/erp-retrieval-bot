# nodes/retriever.py
from data.sheets import load_table, get_table_schema, filter_table
import pandas as pd

def retriever_node(state: dict) -> dict:
    tables_needed = state["tables_needed"]
    filters = state.get("filters", {})  # ← get filters from state
    
    retrieved_data = {}
    
    for table_name in tables_needed:
        # Load the table from Google Sheets
        df = load_table(table_name)
        
        # Get schema description
        schema = get_table_schema(table_name)
        
        # Apply filters if they exist for this table
        table_filters = filters.get(table_name, {})
        if table_filters:
            df = filter_table(df, table_filters)
        
        # Convert to readable format for LLM
        table_data = df.to_dict(orient="records")
        
        retrieved_data[table_name] = {
            "schema": schema,
            "data": table_data,
            "row_count": len(table_data)
        }
    
    state["retrieved_data"] = retrieved_data
    return state