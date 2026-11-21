# Demonstration 3: Gradio AI Assistant with FastAPI Backend

This demonstration showcases a full-featured multimodal AI assistant integrating a Gradio UI with a FastAPI REST backend. It supports text prompts, document text extraction (.pdf and .txt), and image analysis using Groq's vision models.

---

## 1. Prerequisites & Environment

- **Python Version**: Python 3.12+ / Python 3.14 (Virtual environment is pre-configured in `.venv`)
- **Working Directory**: `Module_2/Demonstration 3/gradio-fastapi-ai-assistant`

### Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  cd "Module_2\Demonstration 3\gradio-fastapi-ai-assistant"
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
   VISION_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
   ENVIRONMENT=development
   GRADIO_SHARE=false
   ```

---

## 3. Starting the Demonstration (Two Terminals Required)

> **Important**: Ensure port 8000 is not in use by Demonstration 1 or 2 before launching.

### Terminal 1: Launch FastAPI Backend
```powershell
cd "Module_2\Demonstration 3\gradio-fastapi-ai-assistant"
.\.venv\Scripts\uvicorn.exe src.fastapi_backend:app --host 127.0.0.1 --port 8000 --reload
```
*Backend URL*: `http://127.0.0.1:8000`

### Terminal 2: Launch Gradio Frontend
```powershell
cd "Module_2\Demonstration 3\gradio-fastapi-ai-assistant"
.\.venv\Scripts\python.exe src\app.py
```
*Frontend URL*: Open `http://127.0.0.1:7860` in your web browser.

*(Or in VS Code: Run **Demo 3: FastAPI Backend** in launch dropdown, then run **Demo 3: Gradio Frontend**)*

---

## 4. Testing Core Interactions

Pre-prepared sample files are provided in `sample_data/`:
- `sample_data/sample.pdf` (sample 1-page PDF)
- `sample_data/sample_doc.txt` (sample text document)
- `sample_data/sample_image.png` (sample image)

### Test Workflow A: Text Prompt
1. In the Prompt box, enter:
   ```text
   Explain the difference between proactive and reactive agents.
   ```
2. Click **Generate Response**.
3. View the rendered Markdown response and model metadata.

### Test Workflow B: Document Analysis (.pdf or .txt)
1. In the Prompt box, enter:
   ```text
   Summarize the key points in this uploaded document.
   ```
2. In **Optional File Upload**, upload `sample_data/sample.pdf` or `sample_data/sample_doc.txt`.
3. Click **Generate Response**.

### Test Workflow C: Multimodal Image Analysis
1. In the Prompt box, enter:
   ```text
   Describe what is shown in this image.
   ```
2. In **Optional Image Upload**, upload `sample_data/sample_image.png`.
3. Click **Generate Response**.
