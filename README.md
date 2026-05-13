# Meowgotchi

A small PySide6 desktop pet app with a local Ollama chat page.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull gemma3:1b
```

## Run

Start Ollama if it is not already running:

```bash
ollama serve
```

Run the app:

```bash
python3 main.py
```

Use a different Ollama model:

```bash
OLLAMA_MODEL=tinyllama python3 main.py
```

## Project Layout

```text
assets/              Images and fonts used by the app
meowgotchi/          Application package
  app.py             QApplication startup and page navigation
  config.py          Runtime configuration
  menu_page.py       Ollama chat UI
  ollama_client.py   Local Ollama API client
  paths.py           Project asset paths
  pet.py             Desktop pet widget
  ui_helpers.py      Shared UI helpers
main.py              Thin app launcher
```
