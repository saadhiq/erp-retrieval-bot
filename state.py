# state.py
from typing import TypedDict, List

class BotState(TypedDict):
    question: str           # original user question
    tables_needed: List[str] # router decision
    routing_reason: str 
    filters: dict    # filters to apply to each table
    retrieved_data: dict    # data fetched from sheets
    final_answer: str       # LLM generated answer