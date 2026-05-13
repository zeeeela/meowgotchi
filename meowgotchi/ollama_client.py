import json
import urllib.error
import urllib.request

from meowgotchi.config import OLLAMA_MODEL, OLLAMA_URL


def chat(messages):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return None, f"Ollama error {error.code}: {error.reason}"
    except urllib.error.URLError:
        return None, "Cannot reach Ollama. Run: ollama serve"
    except TimeoutError:
        return None, "Ollama took too long to answer."

    message = data.get("message", {}).get("content", "").strip()
    return message or "Ollama returned an empty response.", None

