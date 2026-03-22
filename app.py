# app.py

import streamlit as st
from utils.audio import record_audio, cleanup_audio
from core.stt import transcribe
from core.graph import run_pipeline

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Voice Agent",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ Voice Agent")
st.caption("Speak your query — the agent will search the web or answer locally.")

# ── Session state init ────────────────────────────────────────────────────────

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "recording" not in st.session_state:
    st.session_state.recording = False

# ── Sidebar settings ──────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Settings")
    duration = st.slider(
        "Recording duration (seconds)",
        min_value=3,
        max_value=15,
        value=8,
        step=1,
    )
    st.divider()
    st.markdown("**Models in use**")
    st.markdown("- 🎤 STT: `faster-whisper base.en`")
    st.markdown("- 🧠 LLM: `ollama/llama3.2`")
    st.markdown("- 🔍 Search: `DuckDuckGo (free)`")

# ── Record button ─────────────────────────────────────────────────────────────

col1, col2 = st.columns([1, 1])

with col1:
    record_btn = st.button(
        "🎤 Hold to Record",
        use_container_width=True,
        type="primary",
    )

with col2:
    clear_btn = st.button(
        "🗑️ Clear",
        use_container_width=True,
    )

if clear_btn:
    st.session_state.transcript = ""
    st.session_state.result = None
    st.rerun()

# ── Recording + pipeline flow ─────────────────────────────────────────────────

if record_btn:
    # Step 1 — Record
    with st.status("🎤 Recording...", expanded=True) as status:
        st.write(f"Speak now — recording for {duration} seconds...")
        audio_path = record_audio(duration=duration)
        status.update(label="✅ Recording complete.")

    # Step 2 — Transcribe
    with st.status("🧠 Transcribing...", expanded=True) as status:
        st.write("Converting speech to text via Whisper...")
        stt_result = transcribe(audio_path)
        cleanup_audio(audio_path)
        transcript = stt_result["transcript"]
        st.session_state.transcript = transcript

        if stt_result["low_confidence"]:
            status.update(label="⚠️ Low confidence transcript.", state="error")
            st.warning("Whisper flagged this transcript as low confidence. Try speaking more clearly.")
        else:
            status.update(label=f"✅ Transcript ready.")

    # Step 3 — Show transcript
    if transcript:
        st.markdown("### 📝 Your Query")
        st.info(transcript)

        # Step 4 — Run agent pipeline
        with st.status("⚙️ Running agents...", expanded=True) as status:
            st.write("Validating transcript...")
            st.write("Routing query...")
            result = run_pipeline(transcript)
            route = result.get("route", "unknown")
            st.write(f"Route decided: `{route}`")
            status.update(label=f"✅ Pipeline complete — route: `{route}`")

        st.session_state.result = result

# ── Results display ───────────────────────────────────────────────────────────

if st.session_state.result:
    result = st.session_state.result

    # Error state
    if not result.get("is_valid"):
        st.error(result.get("error", "Something went wrong."))

    else:
        # Route badge
        route = result.get("route", "")
        if route == "web":
            st.markdown("🌐 **Answered via web search**")
        else:
            st.markdown("🧠 **Answered from local knowledge**")

        # Final answer
        st.markdown("### 💡 Answer")
        st.markdown(result.get("final_answer", "No answer generated."))

        # Sources
        sources = result.get("sources", [])
        if sources:
            st.markdown("### 🔗 Sources")
            for url in sources:
                st.markdown(f"- [{url}]({url})")

        st.divider()
        st.caption("Voice Agent · runs fully on your machine · powered by Whisper + Ollama + LangGraph")