# main.py
from langgraph.graph import StateGraph, END
from state import BotState
from nodes.router import router_node
from nodes.retriever import retriever_node
from nodes.responder import responder_node

# def should_continue(state: dict) -> str:
#     """
#     Conditional edge - checks if retrieval was successful
#     """
#     if not state["tables_needed"]:
#         return "end"
#     if not state["retrieved_data"]:
#         return "end"
#     return "continue"

def should_continue(state: dict) -> str:
    if not state.get("tables_needed"):
        return "end"
    return "continue"

# Build the graph
workflow = StateGraph(BotState)

# Add nodes
workflow.add_node("router", router_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("responder", responder_node)

# Add edges
workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    should_continue,
    {
        "continue": "retriever",
        "end": END
    }
)

workflow.add_edge("retriever", "responder")
workflow.add_edge("responder", END)

# Compile the graph
app = workflow.compile()

def ask(question: str) -> str:
    result = app.invoke({"question": question})
    return result["final_answer"]

# Test it!
if __name__ == "__main__":
    questions = [
        "Show me all BOOKED orders",
        "Who is the manager of James Carter?",
        "What is the email of Acme Corp?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print(f"Answer: {ask(question)}")
        print("-" * 50)