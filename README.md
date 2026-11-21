# Module 2 — Classroom Demonstration Environment Guide

This repository contains all three classroom demonstrations for **Module 2: FastAPI, Streamlit & Gradio for AI Apps**. Every demonstration is pre-configured, tested, and ready for immediate live execution in VS Code.

---

## Demonstrations Overview

| Demo | Title | Architecture | Ports | Primary Test Flow |
|---|---|---|---|---|
| **Demo 1** | **Building Your First FastAPI LLM Endpoint** | FastAPI + Groq LLM | Backend: `8000` | REST API `/generate` & Swagger UI `/docs` |
| **Demo 2** | **Streaming AI Responses with Streamlit** | FastAPI SSE Backend + Streamlit UI | Backend: `8000`<br>Frontend: `8501` | Progressive token streaming via Server-Sent Events |
| **Demo 3** | **Gradio AI Assistant with FastAPI Backend** | FastAPI Backend + Gradio Multimodal UI | Backend: `8000`<br>Frontend: `7860` | Text, PDF/TXT document analysis, and image input |

---

## Quick Start in VS Code

### 1. Open the Project in VS Code
Open this folder (`7_11_26`) in VS Code. The `.vscode/` workspace configurations (`launch.json`, `settings.json`, `tasks.json`) will be loaded automatically.

### 2. Configure Your Groq API Key
All three demonstrations integrate with Groq. Update your key in the `.env` file of each demonstration (or copy from `.env.example`):
- `Module_2/Demonstration 1/fastapi-llm-app/.env`
- `Module_2/Demonstration 2/streamlit-ai-streaming/.env`
- `Module_2/Demonstration 3/gradio-fastapi-ai-assistant/.env`

Add your key:
```ini
GROQ_API_KEY=gsk_your_actual_key_here
```

### 3. Run Automated Validation
Run the built-in test suite to verify all environments, dependencies, and endpoints:
```powershell
python validate_all_demos.py
```
*(Or in VS Code: Run **Run Automated Validation Suite** in the Run & Debug menu)*

---

## Detailed Demonstration Execution Instructions

### Demonstration 1: FastAPI LLM Application

1. **Working Directory**: `Module_2/Demonstration 1/fastapi-llm-app`
2. **Virtual Environment**: `.venv`
3. **Launch in VS Code**:
   - Open **Run & Debug** (`Ctrl+Shift+D` or `Cmd+Shift+D`).
   - Select **Demo 1: FastAPI Server (Port 8000)** and press `F5`.
4. **Manual Terminal Command**:
   ```powershell
   cd "Module_2\Demonstration 1\fastapi-llm-app"
   .\.venv\Scripts\uvicorn.exe src.main:app --host 127.0.0.1 --port 8000 --reload
   ```
5. **Browser URL**:
   - Health check: `http://127.0.0.1:8000/`
   - Swagger Documentation: `http://127.0.0.1:8000/docs`
6. **Test Client**:
   Run the test script in a separate terminal:
   ```powershell
   .\.venv\Scripts\python.exe test_api.py
   ```
   *Expected Response*: JSON containing `"status": "success"`, model name, and generated answer.

---

### Demonstration 2: Streamlit + FastAPI SSE Streaming

> **Terminal Note**: This demo requires two terminals (Backend on port 8000 and Frontend on port 8501). Ensure Demo 1 or Demo 3 is stopped before starting.

1. **Working Directory**: `Module_2/Demonstration 2/streamlit-ai-streaming`
2. **Virtual Environment**: `.venv`
3. **Launch in VS Code**:
   - Step 1: Run **Demo 2: FastAPI SSE Backend (Port 8000)**.
   - Step 2: Run **Demo 2: Streamlit Frontend (Port 8501)**.
4. **Manual Terminal Commands**:
   - **Terminal 1 (Backend)**:
     ```powershell
     cd "Module_2\Demonstration 2\streamlit-ai-streaming"
     .\.venv\Scripts\uvicorn.exe src.sse_backend:app --host 127.0.0.1 --port 8000 --reload
     ```
   - **Terminal 2 (Frontend)**:
     ```powershell
     cd "Module_2\Demonstration 2\streamlit-ai-streaming"
     .\.venv\Scripts\streamlit.exe run src\app.py --server.port 8501
     ```
5. **Browser URL**: `http://localhost:8501`
6. **Sample Input**: Enter `"Explain Agentic AI in simple terms."` in the chat input.
7. **Expected Output**: Tokens appear live via Server-Sent Events with a streaming cursor indicator (`▌`).

---

### Demonstration 3: Gradio AI Assistant + FastAPI Backend

> **Terminal Note**: This demo requires two terminals (Backend on port 8000 and Frontend on port 7860). Ensure Demo 1 or Demo 2 is stopped before starting.

1. **Working Directory**: `Module_2/Demonstration 3/gradio-fastapi-ai-assistant`
2. **Virtual Environment**: `.venv`
3. **Launch in VS Code**:
   - Step 1: Run **Demo 3: FastAPI Backend (Port 8000)**.
   - Step 2: Run **Demo 3: Gradio Frontend (Port 7860)**.
4. **Manual Terminal Commands**:
   - **Terminal 1 (Backend)**:
     ```powershell
     cd "Module_2\Demonstration 3\gradio-fastapi-ai-assistant"
     .\.venv\Scripts\uvicorn.exe src.fastapi_backend:app --host 127.0.0.1 --port 8000 --reload
     ```
   - **Terminal 2 (Frontend)**:
     ```powershell
     cd "Module_2\Demonstration 3\gradio-fastapi-ai-assistant"
     .\.venv\Scripts\python.exe src\app.py
     ```
5. **Browser URL**: `http://127.0.0.1:7860`
6. **Sample Test Inputs**: Pre-packaged test files are available in `sample_data/`:
   - `sample_data/sample_doc.txt` (text file)
   - `sample_data/sample.pdf` (PDF document)
   - `sample_data/sample_image.png` (PNG image)
7. **Expected Output**: Rich Markdown output including the generated response, model used, and request status.

---

## Port Allocation & Management

Because all three FastAPI backends default to port `8000`:
- **Run one demonstration at a time**.
- Stop the current demonstration's backend terminal (`Ctrl+C`) before starting the next demonstration.
- To check or free port `8000` in PowerShell:
  ```powershell
  Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess, State
  ```
