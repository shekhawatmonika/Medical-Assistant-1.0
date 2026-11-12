import requests
from config import OLLAMA_URL, MODEL_NAME

def generate_answer(question, rag_context="", database_context="", api_context=""):
    prompt = f"""
You are a healthcare appointment information assistant.

Safety rules:
- You are not a doctor.
- Do not diagnose diseases.
- Do not prescribe medicines.
- Do not provide emergency treatment instructions.
- Use only the supplied context.
- Do not invent information.
- If information is unavailable, clearly say so.

RAG DOCUMENTS:
{rag_context}

APPOINTMENT DATABASE:
{database_context}

PUBLIC API INFORMATION:
{api_context}

USER QUESTION:
{question}

Give a concise and clear answer.
"""
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["response"]
