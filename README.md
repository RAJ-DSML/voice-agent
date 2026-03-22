# 🎙️ Voice Agent

A voice-first local AI assistant that listens to your query, routes it intelligently,
and returns a concise structured answer — all running on your machine.

Built with **Whisper + Ollama + LangGraph + Streamlit**.

---

## 📸 Demo

![Voice Agent Demo](streamlit-app.gif)

---

## 🧠 How It Works
```
🎤 Voice Input
     ↓
🔊 Whisper STT (local, faster-whisper)
     ↓
✅ Agent 1 — Validator (checks transcript quality)
     ↓
🔀 Agent 2 — Router (web or local?)
     ↙           ↘
🌐 Agent 3      🧠 Agent 4
Web Search      Local LLM
(DuckDuckGo)    (Ollama)
     ↘           ↙
  🧹 Agent 5 — Synthesizer
     ↓
💡 Structured Answer in UI
```

---

## ✨ Features

- 🎤 **Push-to-talk** recording via browser UI
- 🔊 **Local STT** using `faster-whisper` (no cloud, no API key)
- 🤖 **Multi-agent pipeline** built with LangGraph
- 🔀 **Smart routing** — decides web vs local automatically
- 🌐 **Free web search** via DuckDuckGo (no API key needed)
- 🧠 **Fully local LLM** via Ollama (runs on-device)
- 💡 **Structured answers** with sources when available
- 🔒 **100% private** — nothing leaves your machine except web search queries

---

## 🏗️ Project Structure
```
voice-agent/
├── app.py                   # Streamlit entry point
├── core/
│   ├── stt.py               # Whisper STT engine
│   └── graph.py             # LangGraph pipeline
├── agents/
│   ├── validator.py         # Agent 1 — transcript quality check
│   ├── router.py            # Agent 2 — intent classification
│   ├── web_search.py        # Agent 3 — DuckDuckGo search
│   ├── local_llm.py         # Agent 4 — Ollama local answer
│   └── synthesizer.py       # Agent 5 — format final output
├── utils/
│   ├── audio.py             # Mic recording
│   └── prompts.py           # All prompt templates
└── pyproject.toml           # uv project config
```

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Speech to Text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) |
| LLM | [Ollama](https://ollama.com) — llama3.2 |
| Agent Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Web Search | [ddgs](https://github.com/deedy5/ddgs) (DuckDuckGo, free) |
| GUI | [Streamlit](https://streamlit.io) |
| Scraping | BeautifulSoup4 |
| Package Manager | [uv](https://github.com/astral-sh/uv) |

---

## ⚙️ Requirements

- macOS (Apple Silicon recommended) or Linux
- [Ollama](https://ollama.com) installed and running
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) installed

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/RAJ-DSML/voice-agent.git
cd voice-agent
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Pull the Ollama model
```bash
ollama pull llama3.2
```

### 4. Start Ollama
```bash
ollama serve
```

### 5. Run the app
```bash
uv run streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🎮 Usage

1. Open the app at `http://localhost:8501`
2. Adjust recording duration in the sidebar (default 8 seconds)
3. Click **🎤 Hold to Record** and speak your query
4. Watch the agents work in real time
5. Get a structured answer with sources (for web queries)

### Example queries

| Query | Route |
|---|---|
| "What is machine learning?" | 🧠 Local |
| "Explain how transformers work" | 🧠 Local |
| "What is the news today?" | 🌐 Web |
| "Latest developments in AI" | 🌐 Web |
| "What is the capital of France?" | 🧠 Local |
| "Current Bitcoin price" | 🌐 Web |

---

## 🤖 Agent Pipeline

| Agent | Role |
|---|---|
| **Validator** | Checks if transcript is a real query or noise |
| **Router** | Classifies intent — needs web or local knowledge? |
| **Web Search** | Searches DuckDuckGo, scrapes top 3 results |
| **Local LLM** | Answers directly from Ollama's knowledge |
| **Synthesizer** | Formats raw results into a clean structured answer |

---

## 📦 Environment Variables

Create a `.env` file in the root (optional — no keys needed for default setup):
```env
# No API keys required for default configuration
# DuckDuckGo search is free and keyless
# Ollama runs locally
```

---

## 🔧 Configuration

You can tweak the following in the respective files:

| Setting | File | Default |
|---|---|---|
| Whisper model size | `core/stt.py` | `base.en` |
| Ollama model | `agents/*.py` | `llama3.2` |
| Max search results | `agents/web_search.py` | `3` |
| Max chars per page | `agents/web_search.py` | `500` |
| Recording duration | Streamlit sidebar | `8s` |

---

## 🗺️ Roadmap

- [ ] Wake word detection
- [ ] Streaming answer output
- [ ] Conversation memory across turns
- [ ] Voice response (TTS)
- [ ] Support for more Ollama models
- [ ] Docker setup

---

## 🙏 Acknowledgements

- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [Ollama](https://ollama.com)
- [LangChain / LangGraph](https://github.com/langchain-ai/langgraph)
- [ddgs](https://github.com/deedy5/ddgs)
- [Streamlit](https://streamlit.io)

---

## 📄 License

MIT License — feel free to use, modify and share.