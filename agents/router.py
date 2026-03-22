# agents/router.py

from langchain_ollama import ChatOllama
from utils.prompts import ROUTER_PROMPT

_llm = ChatOllama(model="llama3.2", temperature=0)


def route_query(state: dict) -> dict:
    """
    Agent 2 — Router
    Classifies the query as 'web' or 'local'.
    Updates state with 'route' key.
    """
    query = state.get("transcript", "").strip()

    print(f"[router] Routing query: '{query}'")

    prompt = ROUTER_PROMPT.format(query=query)
    response = _llm.invoke(prompt)
    result = response.content.strip().lower()

    # Sanitise — if model returns anything unexpected, default to local
    if "web" in result:
        route = "web"
    else:
        route = "local"

    print(f"[router] Route decided: {route}")

    return {
        **state,
        "route": route,
    }


def decide_route(state: dict) -> str:
    """
    LangGraph conditional edge function.
    Returns the name of the next node to run based on state['route'].
    This function is used in graph.py to wire conditional branching.
    """
    if not state.get("is_valid", False):
        return "end"

    return state.get("route", "local")