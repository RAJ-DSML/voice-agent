# core/graph.py

from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.validator import validate_transcript
from agents.router import route_query, decide_route
from agents.web_search import search_web
from agents.local_llm import answer_locally
from agents.synthesizer import synthesize_web_answer


# ── State schema ──────────────────────────────────────────────────────────────

class AgentState(TypedDict, total=False):
    transcript:     str
    is_valid:       bool
    error:          str | None
    route:          str
    search_results: str
    final_answer:   str
    sources:        list[str]


# ── Graph definition ──────────────────────────────────────────────────────────

def build_graph():
    """
    Builds and compiles the LangGraph agent pipeline.
    Returns a compiled runnable graph.
    """
    graph = StateGraph(AgentState)

    # Register all nodes
    graph.add_node("validator",   validate_transcript)
    graph.add_node("router",      route_query)
    graph.add_node("web_search",  search_web)
    graph.add_node("local_llm",   answer_locally)
    graph.add_node("synthesizer", synthesize_web_answer)

    # Entry point
    graph.set_entry_point("validator")

    # validator → router (always)
    graph.add_edge("validator", "router")

    # router → web_search or local_llm (conditional)
    graph.add_conditional_edges(
        "router",
        decide_route,
        {
            "web":   "web_search",
            "local": "local_llm",
            "end":   END,
        }
    )

    # web_search → synthesizer
    graph.add_edge("web_search", "synthesizer")

    # synthesizer → END
    graph.add_edge("synthesizer", END)

    # local_llm → END
    graph.add_edge("local_llm", END)

    return graph.compile()


# Compile once at import time
pipeline = build_graph()


# ── Runner ────────────────────────────────────────────────────────────────────

def run_pipeline(transcript: str) -> dict:
    """
    Main entry point for the agent pipeline.
    Takes a transcript string, runs it through all agents,
    returns the final state dict.
    """
    initial_state: AgentState = {
        "transcript":     transcript,
        "is_valid":       False,
        "error":          None,
        "route":          "",
        "search_results": "",
        "final_answer":   "",
        "sources":        [],
    }

    print(f"\n[graph] Starting pipeline for: '{transcript}'")
    final_state = pipeline.invoke(initial_state)
    print(f"[graph] Pipeline complete. Route: {final_state.get('route')}")

    return final_state