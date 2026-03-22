# agents/synthesizer.py

from langchain_ollama import ChatOllama
from utils.prompts import WEB_SEARCH_SYNTHESIZER_PROMPT

_llm = ChatOllama(model="llama3.2", temperature=0.3)


def synthesize_web_answer(state: dict) -> dict:
    """
    Agent 5 — Synthesizer (Web route only)
    Takes raw search results and formats a clean structured answer.
    Updates state with 'final_answer' and 'sources' keys.
    """
    query = state.get("transcript", "").strip()
    search_results = state.get("search_results", "")

    print(f"[synthesizer] Synthesizing web results for: '{query}'")

    prompt = WEB_SEARCH_SYNTHESIZER_PROMPT.format(
        query=query,
        search_results=search_results,
    )

    response = _llm.invoke(prompt)
    answer = response.content.strip()

    # Extract source URLs from search results for display in UI
    sources = []
    for line in search_results.splitlines():
        if line.startswith("URL:"):
            url = line.replace("URL:", "").strip()
            if url:
                sources.append(url)

    print(f"[synthesizer] Done. chars: {len(answer)}, sources: {len(sources)}")

    return {
        **state,
        "final_answer": answer,
        "sources": sources,
    }