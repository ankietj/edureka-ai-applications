#!/usr/bin/env python3
"""
Lightweight Automated Validation Suite for Module 2 Classroom Demonstrations
Tests syntax, dependencies, configurations, application endpoints, streaming behavior,
and multimodal features across Demo 1, Demo 2, and Demo 3 using their respective virtual environments.
"""

import sys
import os
import py_compile
import json
import time
import subprocess
import argparse
from pathlib import Path
from unittest.mock import MagicMock

ROOT_DIR = Path(__file__).resolve().parent
MODULE_2_DIR = ROOT_DIR / "Module_2"
DEMO_1_DIR = MODULE_2_DIR / "Demonstration 1" / "fastapi-llm-app"
DEMO_2_DIR = MODULE_2_DIR / "Demonstration 2" / "streamlit-ai-streaming"
DEMO_3_DIR = MODULE_2_DIR / "Demonstration 3" / "gradio-fastapi-ai-assistant"

passed_tests = 0
failed_tests = 0
audit_results = []

def record(test_name: str, passed: bool, details: str = ""):
    global passed_tests, failed_tests
    status = "PASS" if passed else "FAIL"
    if passed:
        passed_tests += 1
        print(f"  [PASS] {test_name}" + (f" -> {details}" if details else ""))
    else:
        failed_tests += 1
        print(f"  [FAIL] {test_name} -> {details}")
    audit_results.append({"test": test_name, "status": status, "details": details})


def test_syntax():
    print("\n--- 1. Python Syntax Validation ---")
    python_files = list(MODULE_2_DIR.rglob("*.py"))
    clean_files = [f for f in python_files if ".venv" not in f.parts and "__pycache__" not in f.parts]
    for py_file in clean_files:
        rel_path = py_file.relative_to(ROOT_DIR)
        try:
            py_compile.compile(str(py_file), doraise=True)
            record(f"Syntax: {rel_path}", True)
        except py_compile.PyCompileError as e:
            record(f"Syntax: {rel_path}", False, str(e))


def test_demo_1():
    print("\n--- 2. Demo 1: FastAPI LLM Application Validation ---")
    src_path = str(DEMO_1_DIR / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from fastapi.testclient import TestClient
        import config as d1_config
        import main as d1_main

        # Check config
        record("Demo 1 Config Loaded", True, f"Model: {d1_config.MODEL_NAME}")
        has_real_key = bool(d1_config.GROQ_API_KEY and d1_config.GROQ_API_KEY != "your_api_key" and d1_config.GROQ_API_KEY.startswith("gsk_"))
        record("Demo 1 Credential Status", True, "Live Groq Key configured" if has_real_key else "Placeholder detected (your_api_key); mock tests enabled")

        # TestClient
        client = TestClient(d1_main.app)

        # GET /
        res_home = client.get("/")
        record("Demo 1 GET / Home", res_home.status_code == 200, res_home.json().get("message", ""))

        # Pydantic validation rejection
        res_invalid = client.post("/generate", json={"invalid_field": "val"})
        record("Demo 1 Schema Validation (Pydantic 422 on invalid request)", res_invalid.status_code == 422)

        # Mock LLM generation test
        mock_choice = MagicMock()
        mock_choice.message.content = "Agentic AI is an autonomous, goal-directed AI system."
        mock_response = MagicMock(choices=[mock_choice])

        original_create = d1_main.client.chat.completions.create
        d1_main.client.chat.completions.create = MagicMock(return_value=mock_response)

        res_gen = client.post("/generate", json={"prompt": "Explain Agentic AI in one paragraph."})
        record("Demo 1 POST /generate (Mocked LLM)", res_gen.status_code == 200 and res_gen.json().get("status") == "success", f"Output: {res_gen.json().get('response')[:50]}...")

        d1_main.client.chat.completions.create = original_create
    except Exception as exc:
        record("Demo 1 Execution", False, str(exc))


def test_demo_2():
    print("\n--- 3. Demo 2: Streamlit + FastAPI SSE Streaming Validation ---")
    src_path = str(DEMO_2_DIR / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from fastapi.testclient import TestClient
        import config as d2_config
        import sse_backend as d2_backend

        record("Demo 2 Config Loaded", True, f"Model: {d2_config.MODEL_NAME}")

        client = TestClient(d2_backend.app)

        # GET /
        res_home = client.get("/")
        record("Demo 2 GET / Home", res_home.status_code == 200, res_home.json().get("message", ""))

        # Mocked SSE Streaming test
        mock_tokens = ["Streaming ", "LLM ", "response ", "via ", "SSE."]
        def mock_stream_fn(*args, **kwargs):
            for tok in mock_tokens:
                c = MagicMock()
                c.choices = [MagicMock(delta=MagicMock(content=tok))]
                yield c

        original_create = d2_backend.client.chat.completions.create
        d2_backend.client.chat.completions.create = MagicMock(side_effect=mock_stream_fn)

        with client.stream("POST", "/stream", json={"messages": [{"role": "user", "content": "Hello"}]}) as response:
            status_ok = response.status_code == 200
            collected = []
            has_done = False
            for line in response.iter_lines():
                if not line:
                    continue
                if line == "data: [DONE]":
                    has_done = True
                elif line.startswith("data: "):
                    payload = json.loads(line[6:])
                    collected.append(payload.get("content", ""))

            stream_passed = status_ok and has_done and ("".join(collected) == "".join(mock_tokens))
            record("Demo 2 SSE POST /stream Progressive Delivery", stream_passed, f"Tokens received: {collected}, [DONE] flag: {has_done}")

        # Non-streaming endpoint
        mock_single_choice = MagicMock()
        mock_single_choice.message.content = "Complete response text."
        d2_backend.client.chat.completions.create = MagicMock(return_value=MagicMock(choices=[mock_single_choice]))
        res_gen = client.post("/generate", json={"messages": [{"role": "user", "content": "Hello"}]})
        record("Demo 2 POST /generate (Non-streaming)", res_gen.status_code == 200 and "response" in res_gen.json())

        d2_backend.client.chat.completions.create = original_create

        # Streamlit app syntax / structure check
        import ast
        app_code = (DEMO_2_DIR / "src" / "app.py").read_text(encoding="utf-8")
        ast.parse(app_code)
        record("Demo 2 Streamlit App Source Validation", True, "app.py parsed cleanly with valid syntax and AST")
    except Exception as exc:
        record("Demo 2 Execution", False, str(exc))


def test_demo_3():
    print("\n--- 4. Demo 3: Gradio + FastAPI Multimodal Assistant Validation ---")
    src_path = str(DEMO_3_DIR / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from fastapi.testclient import TestClient
        import config as d3_config
        import fastapi_backend as d3_backend
        import app as d3_app

        record("Demo 3 Config Loaded", True, f"Text Model: {d3_config.MODEL_NAME}, Vision: {d3_backend.VISION_MODEL_NAME}")

        client = TestClient(d3_backend.app)

        # GET /
        res_home = client.get("/")
        record("Demo 3 GET / Home", res_home.status_code == 200, res_home.json().get("message", ""))

        # GET /generate
        mock_choice = MagicMock()
        mock_choice.message.content = "GET endpoint response."
        original_create = d3_backend.client.chat.completions.create
        d3_backend.client.chat.completions.create = MagicMock(return_value=MagicMock(choices=[mock_choice]))

        res_get_gen = client.get("/generate?prompt=TestPrompt")
        record("Demo 3 GET /generate Endpoint", res_get_gen.status_code == 200 and res_get_gen.json().get("status") == "success")

        # File extraction tests
        class DummyUpload:
            def __init__(self, name):
                self.name = name

        txt_file = DummyUpload(str(DEMO_3_DIR / "sample_data" / "sample_doc.txt"))
        pdf_file = DummyUpload(str(DEMO_3_DIR / "sample_data" / "sample.pdf"))
        img_path = str(DEMO_3_DIR / "sample_data" / "sample_image.png")

        txt_content = d3_app.extract_file_text(txt_file)
        pdf_content = d3_app.extract_file_text(pdf_file)
        b64, mime = d3_app.encode_image(img_path)

        record("Demo 3 Text File (.txt) Ingestion", bool(txt_content and "Agentic AI" in txt_content))
        record("Demo 3 PDF File (.pdf) Ingestion (pypdf)", bool(pdf_content and len(pdf_content) > 0))
        record("Demo 3 Image Base64 Encoding (.png)", bool(b64 and mime == "image/png"))

        # Multimodal Vision POST /generate
        mock_vis_choice = MagicMock()
        mock_vis_choice.message.content = "Vision description: Agentic AI Test Banner."
        d3_backend.client.chat.completions.create = MagicMock(return_value=MagicMock(choices=[mock_vis_choice]))

        payload_vis = {
            "prompt": "Describe image",
            "image_base64": b64,
            "image_mime_type": mime
        }
        res_vis = client.post("/generate", json=payload_vis)
        record("Demo 3 Multimodal POST /generate (Vision Model Route)", res_vis.status_code == 200 and res_vis.json().get("model") == d3_backend.VISION_MODEL_NAME)

        # Gradio Blocks instantiation verification
        record("Demo 3 Gradio Blocks UI Definition", d3_app.demo is not None and hasattr(d3_app.demo, "blocks"))

        d3_backend.client.chat.completions.create = original_create
    except Exception as exc:
        record("Demo 3 Execution", False, str(exc))


def run_orchestrated():
    print("=" * 70)
    print("MODULE 2 AUTOMATED VALIDATION SUITE (ORCHESTRATOR)")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1. Syntax check
    test_syntax()

    # 2. Demo 1
    d1_py = DEMO_1_DIR / ".venv" / "Scripts" / "python.exe"
    proc_d1 = subprocess.run([str(d1_py), str(__file__), "--demo", "1"], capture_output=True, text=True)
    print(proc_d1.stdout)
    if proc_d1.stderr:
        for err_line in proc_d1.stderr.splitlines():
            if "StarletteDeprecationWarning" not in err_line:
                print(f"  [STDERR D1] {err_line}")

    # 3. Demo 2
    d2_py = DEMO_2_DIR / ".venv" / "Scripts" / "python.exe"
    proc_d2 = subprocess.run([str(d2_py), str(__file__), "--demo", "2"], capture_output=True, text=True)
    print(proc_d2.stdout)
    if proc_d2.stderr:
        for err_line in proc_d2.stderr.splitlines():
            if "StarletteDeprecationWarning" not in err_line:
                print(f"  [STDERR D2] {err_line}")

    # 4. Demo 3
    d3_py = DEMO_3_DIR / ".venv" / "Scripts" / "python.exe"
    proc_d3 = subprocess.run([str(d3_py), str(__file__), "--demo", "3"], capture_output=True, text=True)
    print(proc_d3.stdout)
    if proc_d3.stderr:
        for err_line in proc_d3.stderr.splitlines():
            if "StarletteDeprecationWarning" not in err_line:
                print(f"  [STDERR D3] {err_line}")

    all_exit_codes = [proc_d1.returncode, proc_d2.returncode, proc_d3.returncode]
    print("\n" + "=" * 70)
    if any(code != 0 for code in all_exit_codes):
        print("ORCHESTRATOR RESULT: SOME TESTS FAILED.")
        sys.exit(1)
    else:
        print("ORCHESTRATOR RESULT: ALL 3 DEMOS VALIDATED SUCCESSFULLY!")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", type=int, choices=[1, 2, 3], help="Run tests for specific demo")
    args = parser.parse_args()

    if args.demo == 1:
        test_demo_1()
        sys.exit(0 if failed_tests == 0 else 1)
    elif args.demo == 2:
        test_demo_2()
        sys.exit(0 if failed_tests == 0 else 1)
    elif args.demo == 3:
        test_demo_3()
        sys.exit(0 if failed_tests == 0 else 1)
    else:
        run_orchestrated()


if __name__ == "__main__":
    main()
