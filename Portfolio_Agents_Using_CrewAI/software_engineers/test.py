# test.py

import sys
import os

# Add the path to src/ to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from software_engineers.llms.ollama_llm import Ollama

# def test_call():
#     print("🧪 Testing call()...")
#     ollama = Ollama(model_name="llama3")
#     prompt = "What is the capital of Japan?"
#     response = ollama.call(prompt)
#     print("Prompt:", prompt)
#     print("Response:", response)
#     print("-" * 40)

def test_chat():
    print("🧪 Testing chat()...")
    ollama = Ollama(model_name="deepseek-r1:latest")
    messages = [
        {"role": "user", "content": "Hi, who are you?"},
        {"role": "assistant", "content": "I'm an AI model here to help you."},
        {"role": "user", "content": "Tell me a fun fact about space?"}
    ]
    response = ollama.chat(messages)
    print("Messages:", messages)
    print("Response:", response["content"])
    print("-" * 40)

if __name__ == "__main__":
    # test_call()
    test_chat()
