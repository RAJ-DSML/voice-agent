# agents/validator.py

from langchain_ollama import ChatOllama
from utils.prompts import VALIDATOR_PROMPT

_llm = ChatOllama(model="llama3.2", temperature=0)


def validate_transcript(state: dict) -> dict:
    """
    Agent 1 — Validator
    Checks if the transcript is a valid, meaningful query.
    Updates state with 'is_valid' boolean and passes through.
    """
    transcript = state.get("transcript", "").strip()

    # Fast path — no need to call LLM if transcript is empty
    if not transcript:
        print("[validator] Empty transcript, marking invalid.")
        return {**state, "is_valid": False, "error": "No speech detected."}

    print(f"[validator] Checking transcript: '{transcript}'")

    prompt = VALIDATOR_PROMPT.format(transcript=transcript)
    response = _llm.invoke(prompt)
    result = response.content.strip().upper()

    is_valid = result == "VALID"
    print(f"[validator] Result: {result} → is_valid={is_valid}")

    return {
        **state,
        "is_valid": is_valid,
        "error": None if is_valid else "Transcript was flagged as invalid or unclear.",
    }