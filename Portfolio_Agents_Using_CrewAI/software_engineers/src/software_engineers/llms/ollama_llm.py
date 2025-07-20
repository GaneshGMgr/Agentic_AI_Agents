from crewai.llms.base_llm import BaseLLM
import requests
import time
import json


class Ollama(BaseLLM):
    def __init__(self, model_name="llama3:latest", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')

    def _remove_non_serializable(self, data):
        """Remove entries from a dictionary that can't be converted to JSON."""
        clean = {}
        for key, value in data.items():
            try:
                json.dumps(value)
                clean[key] = value
            except (TypeError, OverflowError):
                print(f"Skipping non-serializable: {key} = {value}")
        return clean

    def _pretty_print(self, label, data):
        """Print dictionary data safely, replacing non-serializables."""
        def fallback(o): return f"<<non-serializable: {repr(o)}>>"
        print(f"{label}:\n{json.dumps(data, indent=2, default=fallback)}")

    def call(self, prompt: str, max_retries: int = 3, **kwargs) -> str:
        """Send a single prompt to Ollama with retry logic."""
        clean_kwargs = self._remove_non_serializable(kwargs)
        payload = {
            "model": self.model_name,
            "prompt": str(prompt),
            "stream": False,
            **clean_kwargs
        }

        for attempt in range(max_retries):
            try:
                self._pretty_print("Sending to Ollama (generate)", payload)

                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=600
                )

                print("Received response:", response.status_code)
                response.raise_for_status()
                return response.json().get("response", "")

            except requests.exceptions.RequestException as e:
                print(f"Request failed ({attempt + 1}/{max_retries}): {e}")
                time.sleep(1)
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

        return "Failed to get response from Ollama after retries"

    def chat(self, messages, **kwargs):
        """Send a list of messages to Ollama (chat-style)."""
        clean_kwargs = self._remove_non_serializable(kwargs)
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            **clean_kwargs
        }

        try:
            self._pretty_print("Sending to Ollama (chat)", payload)

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=600
            )

            print("Received chat response:", response.status_code)
            response.raise_for_status()
            data = response.json()

            return {
                "role": "assistant",
                "content": data.get("message", {}).get("content", "")
            }

        except Exception as e:
            print(f"Chat error: {e}")
            return {
                "role": "assistant",
                "content": "Failed to chat with Ollama"
            }
