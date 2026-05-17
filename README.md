# Meowgotchi

A cute PySide6 desktop pet application with music player, integrated AI chat, and local RAG (Retrieval-Augmented Generation) capabilities powered by Ollama for my research.

## Features

- **Interactive Desktop Pet**: A charming pixel art pet (`Dudu`) that stays on your desktop
- **Local AI Chat**: Chat with a locally-running Ollama model—no API keys or internet required
- **RAG Research**: Query PDF documents using semantic search and local LLMs
- **Spotify Integration**: Control music playback directly from the app (Mac only)
- **Customizable Models**: Switch between different Ollama models via environment variables
- **Transparent UI**: Frameless, transparent windows that blend seamlessly with your desktop

## Setup

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- macOS (for Spotify integration), or Linux/Windows (without Spotify features)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd meowgotchi
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  #On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Pull required Ollama models:
```bash
ollama pull gemma3:1b       # For chat (default)
ollama pull phi3:mini       # For research assistant (optional)
```

## Usage

### Run the App

Start the application:
```bash
python3 main.py
```

### Customize Ollama Models

Use environment variables to override default models:

```bash
#Use a different chat model
OLLAMA_MODEL=tinyllama python3 main.py

#Use a different research assistant model
OLLAMA_MODEL_RESEARCH_ASSISTANT=neural-chat python3 main.py

#Use a different Ollama server URL
OLLAMA_URL=http://localhost:11434 python3 main.py
```

### Available Models

Popular models to try:
- **Chat**: `gemma3:1b`, `tinyllama`, `neural-chat`, `mistral`
- **Research**: `phi3:mini`, `orca-mini`, `mistral`

## App Features

### Chat Page
- Talk to a local Ollama model as `Dudu`, a quirky desktop assistant
- Casual, conversational responses
- No history persistence (fresh conversation each session)

### Research Page
- Upload and analyze PDF documents
- Semantic search powered by `sentence-transformers`
- Query documents with natural language
- Responses grounded in document content via RAG

### Music Player (macOS only)
- Play/pause music via Spotify
- Next/previous track controls
- Requires `spotify_player` CLI tool installed

## Project Layout

```
.
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── main.py                   # App entry point
├── chunking.py               # PDF text chunking for RAG
├── assets/
│   └── papers/               # PDF documents for RAG
│   └── [images, fonts]       # UI assets
└── meowgotchi/               # Main application package
    ├── app.py                # QApplication and page routing
    ├── config.py             # Runtime configuration & Ollama settings
    ├── pet.py                # Main desktop pet widget
    ├── menu_page.py          # Chat UI page
    ├── chat_page.py          # Research/RAG UI page
    ├── ollama_client.py      # Ollama API client wrapper
    ├── paths.py              # Asset path resolver
    ├── ui_helpers.py         # Shared UI utilities
    └── __init__.py
```

## Configuration

Edit `meowgotchi/config.py` to change:
- Default Ollama model and URL
- System prompt for the chat assistant
- Research assistant model and endpoint

Example:
```python
OLLAMA_MODEL = "mistral"                  # Chat model
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL_RESEARCH_ASSISTANT = "phi3:mini"
OLLAMA_RESEARCH_ASSISTANT_URL = "http://localhost:11434/api/generate"
```

## Development

### Running in Development Mode

Debug with verbose output:
```bash
python3 main.py 2>&1 | tee debug.log
```

### Testing RAG

Test document chunking and retrieval:
```bash
conda activate rag-phi3  # If using separate env
python3 -m RAG.try
```

### Troubleshooting

**"Cannot reach Ollama" error:**
- Ensure `ollama serve` is running in another terminal
- Check `OLLAMA_URL` environment variable

**"Module not found" errors:**
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify virtual environment is activated

**Video/Audio playback issues:**
- Restart Ollama service
- Check model compatibility with your system


## Author

Created with ᥫ᭡ for those who appreciate cute desktop companions and local AI.
