# 🏥 Medical Assistant — Streamlit + Local LLM + RAG
Live project: https://medical-assistant-v-1.streamlit.app
A portfolio-ready educational Medical Appointment Assistant.

## Architecture

User → Streamlit → RAG/ChromaDB → SQLite/Public API → Ollama → Llama 3.2 → Answer

## No FastAPI

This project uses only Streamlit. FastAPI is not required.

## API Keys

The local version requires:
- Ollama API key: No
- OpenAI API key: No
- Gemini API key: No
- Hugging Face token: No
- ChromaDB key: No
- SQLite key: No

Internet is needed initially to install packages and download the Sentence Transformers model.

## Setup in VS Code

1. Open this folder in VS Code.
2. Open Terminal.
3. Create environment:

```bash
python -m venv venv
```

4. Activate on Windows:

```powershell
venv\Scripts\activate
```

5. Install packages:

```bash
pip install -r requirements.txt
```

6. Install Ollama from https://ollama.com/
7. Download Llama:

```bash
ollama pull llama3.2
```

8. Test:

```bash
ollama run llama3.2
```

9. Run the app:

```bash
streamlit run streamlit_app.py
```

10. Open:

```text
http://localhost:8501
```

## Features

- Local Llama 3.2
- RAG with ChromaDB
- Local embeddings
- SQLite appointment booking
- Public openFDA API example
- Streamlit UI
- Source display

## Automatically created

After first run:
- `chroma_db/`
- `appointments.db`

These are not included in the ZIP.

## Medical safety

This is an educational/administrative prototype. Do not use it for diagnosis, prescribing medication, emergency decisions, or replacing a qualified healthcare professional. Use synthetic/demo data for portfolio demonstrations.
