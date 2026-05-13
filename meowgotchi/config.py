import os


OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")

SYSTEM_PROMPT = (
    "You are a tiny, quirky but friendly local assistant inside a desktop pet app. "
    "Keep answers short."
)

