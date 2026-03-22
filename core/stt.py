from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download

MODEL_SIZE = "base.en"
MODEL_REPO = f"Systran/faster-whisper-{MODEL_SIZE}"


def _download_model_with_progress(repo_id: str) -> str:
    """
    Downloads the Whisper model from HuggingFace.
    Returns the local cache path.
    """
    print(f"[stt] Checking model cache for '{repo_id}'...")
    print("[stt] If downloading for first time, this may take 1-2 mins...")

    local_path = snapshot_download(
        repo_id=repo_id,
        local_files_only=False,
    )
    return local_path


print("[stt] Initialising Whisper model...")
_model_path = _download_model_with_progress(MODEL_REPO)
_model = WhisperModel(_model_path, device="auto", compute_type="int8")
print("[stt] Whisper model ready.")


def transcribe(audio_path: str) -> dict:
    """
    Transcribes a WAV file using Whisper.
    Returns a dict with transcript text and confidence info.
    """
    print(f"[stt] Transcribing: {audio_path}")

    segments, info = _model.transcribe(
        audio_path,
        beam_size=5,
        language="en",
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=500
        ),
    )

    full_text = ""
    segment_list = []

    for segment in segments:
        full_text += segment.text.strip() + " "
        segment_list.append({
            "text": segment.text.strip(),
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "no_speech_prob": round(segment.no_speech_prob, 3),
        })

    full_text = full_text.strip()

    return {
        "transcript": full_text,
        "language": info.language,
        "language_probability": round(info.language_probability, 3),
        "segments": segment_list,
        "low_confidence": _is_low_confidence(segment_list),
    }


def _is_low_confidence(segments: list) -> bool:
    if not segments:
        return True
    avg_no_speech = sum(s["no_speech_prob"] for s in segments) / len(segments)
    return avg_no_speech > 0.5