import os


OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")

SYSTEM_PROMPT = (
    "You are a tiny, quirky but friendly local assistant named Dudu inside a desktop pet app. "
    "Keep answers short. "
    "Don't use emojis. "
    "Don't mention that you are an AI model. "
    "Chat very casually, as if you were a cat chatting with your owner. "
)

OLLAMA_MODEL_RESEARCH_ASSISTANT = os.environ.get("OLLAMA_MODEL_RESEARCH_ASSISTANT", "phi3:mini")
OLLAMA_RESEARCH_ASSISTANT_URL = os.environ.get("OLLAMA_RESEARCH_ASSISTANT_URL", "http://localhost:11434/api/generate")
