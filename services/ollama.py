import httpx
from core.settings import OLLAMA_HOST

def generate_response(model: str, prompt: str) -> str:
    try:
        response = httpx.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60.0,
        )
        return response.json().get("response", "Error generating response.")
    except Exception as e:
        return f"Erro: {e}"
