# Demonstration 1: Building Your First FastAPI LLM Endpoint

This demonstration teaches how to build, configure, and serve a RESTful FastAPI endpoint powered by Groq's high-speed LLM inference engine.

---

## 1. Prerequisites & Environment

- **Python Version**: Python 3.12+ / Python 3.14 (Virtual environment is pre-configured in `.venv`)
- **Working Directory**: `Module_2/Demonstration 1/fastapi-llm-app`

### Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  cd "Module_2\Demonstration 1\fastapi-llm-app"
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (cmd)**:
  ```cmd
  cd "Module_2\Demonstration 1\fastapi-llm-app"
  .\.venv\Scripts\activate.bat
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
   *(Obtain a key from [Groq Console](https://console.groq.com/keys))*

---

## 3. Starting the Server

Run Uvicorn from the demo directory:
```powershell
.\.venv\Scripts\uvicorn.exe src.main:app --host 127.0.0.1 --port 8000 --reload
```
*(Or in VS Code: Press `F5` and select **Demo 1: FastAPI Server (Port 8000)**)*

The server will be available at:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`

---

## 4. Testing the Endpoints

### Test 1: Health Check (GET /)
In your browser or PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method Get
```
**Expected Output**:
```json
{"message": "FastAPI LLM Application is running."}
```

### Test 2: Generate LLM Response (POST /generate)
Run the included client test script in a second terminal:
```powershell
.\.venv\Scripts\python.exe test_api.py
```
*(Or use PowerShell `Invoke-RestMethod`)*:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/generate" -Method Post -ContentType "application/json" -Body '{"prompt": "Explain Agentic AI in one paragraph."}'
```
**Expected Output**:
```json
{
  "response": "Agentic AI refers to...",
  "model": "llama-3.3-70b-versatile",
  "status": "success"
}
```
