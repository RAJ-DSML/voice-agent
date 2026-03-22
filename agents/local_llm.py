# agents/local_llm.py

from langchain_ollama import ChatOllama
from utils.prompts import LOCAL_SYNTHESIZER_PROMPT

_llm = ChatOllama(model="llama3.2", temperature=0.3)


def answer_locally(state: dict) -> dict:
    """
    Agent 4 — Local LLM
    Answers the query entirely from Ollama's knowledge.
    Updates state with 'final_answer' key.
    """
    query = state.get("transcript", "").strip()

    print(f"[local_llm] Answering locally: '{query}'")

    prompt = LOCAL_SYNTHESIZER_PROMPT.format(query=query)
    response = _llm.invoke(prompt)
    answer = response.content.strip()

    print(f"[local_llm] Answer generated, chars: {len(answer)}")

    return {
        **state,
        "final_answer": answer,
        "sources": [],      # No sources for local answers
    }