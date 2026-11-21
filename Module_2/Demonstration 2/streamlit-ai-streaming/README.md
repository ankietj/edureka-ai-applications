# Demonstration 2: Streaming AI Responses with Streamlit and FastAPI

This demonstration showcases real-time Server-Sent Events (SSE) streaming from a FastAPI backend to an interactive Streamlit chat interface.

---

## 1. Prerequisites & Environment

- **Python Version**: Python 3.12+ / Python 3.14 (Virtual environment is pre-configured in `.venv`)
- **Working Directory**: `Module_2/Demonstration 2/streamlit-ai-streaming`

### Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  cd "Module_2\Demonstration 2\streamlit-ai-streaming"
  .\.venv\Scripts\Activate.ps1
  ```

---

## 2. API Credentials Configuration

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and set your Groq API Key:
   ```ini
   GROQ_API_KEY=gsk_your_actual_key_here
   MODEL_NAME=llama-3.3-70b-versatile
   ENVIRONMENT=development
   ```

---

## 3. Starting the Demonstration (Two Terminals Required)

> **Important**: Ensure port 8000 is not in use by Demonstration 1 or 3 before launching.

### Terminal 1: Launch FastAPI SSE Backend
```powershell
cd "Module_2\Demonstration 2\streamlit-ai-streaming"
.\.venv\Scripts\uvicorn.exe src.sse_backend:app --host 127.0.0.1 --port 8000 --reload
```
*Backend URL*: `http://127.0.0.1:8000`

### Terminal 2: Launch Streamlit Frontend
```powershell
cd "Module_2\Demonstration 2\streamlit-ai-streaming"
.\.venv\Scripts\streamlit.exe run src\app.py --server.port 8501
```
*Frontend URL*: Automatically opens in your browser at `http://localhost:8501`

*(Or in VS Code: Run **Demo 2: FastAPI SSE Backend** in launch dropdown, then run **Demo 2: Streamlit Frontend**)*

---

## 4. Testing the Application

1. Open `http://localhost:8501` in your browser.
2. In the chat box at the bottom, enter:
   ```text
   Explain Agentic AI in simple terms.
   ```
3. Click send (or press Enter).
4. Observe the progressive streaming effect: tokens arrive chunk-by-chunk via SSE with a live cursor indicator (`▌`), and conversation history is retained in session state.
