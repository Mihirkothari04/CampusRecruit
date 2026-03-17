from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

# Architecture documentation as required by the docs.
class GraphState(TypedDict):
    drive_config: dict
    candidates: Annotated[list, operator.add]
    parsing_complete: bool
    screening_complete: bool
    shortlist_approved: bool
    briefs_generated: bool
    communications_generated: bool

def parse_resumes_node(state: GraphState): return state
def quality_check_node(state: GraphState): return state
def hard_filter_node(state: GraphState): return state
def ai_screening_node(state: GraphState): return state

def human_review_shortlist_node(state: GraphState):
    decision = interrupt({
        "message": "Please review the shortlist and approve or request changes"
    })
    if decision.get("approved"):
        return {"shortlist_approved": True}
    return {"shortlist_approved": False}

def generate_briefs_node(state: GraphState): return state
def generate_comms_node(state: GraphState): return state

def get_orchestrator():
    builder = StateGraph(GraphState)
    builder.add_node("parse_resumes", parse_resumes_node)
    builder.add_node("quality_check", quality_check_node)
    builder.add_node("hard_filter", hard_filter_node)
    builder.add_node("ai_screening", ai_screening_node)
    builder.add_node("human_review_shortlist", human_review_shortlist_node)
    builder.add_node("generate_briefs", generate_briefs_node)
    builder.add_node("generate_communications", generate_comms_node)

    builder.add_edge(START, "parse_resumes")
    builder.add_edge("parse_resumes", "quality_check")
    builder.add_edge("quality_check", "hard_filter")
    builder.add_edge("hard_filter", "ai_screening")
    builder.add_edge("ai_screening", "human_review_shortlist")
    
    builder.add_conditional_edges(
        "human_review_shortlist",
        lambda s: "proceed" if s.get("shortlist_approved") else "revise",
        {"proceed": "generate_briefs", "revise": "ai_screening"}
    )
    
    builder.add_edge("generate_briefs", "generate_communications")
    builder.add_edge("generate_communications", END)
    
    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)
