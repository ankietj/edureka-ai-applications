import base64
import mimetypes
import os
import requests
import gradio as gr
from pypdf import PdfReader

FASTAPI_URL = "http://127.0.0.1:8000/generate"


def extract_file_text(uploaded_file):
    if uploaded_file is None:
        return ""

    # Support both Gradio string filepaths (Gradio 4/5/6) and file-like objects with a .name attribute
    if isinstance(uploaded_file, str):
        file_path = uploaded_file
    elif hasattr(uploaded_file, "name"):
        file_path = uploaded_file.name
    else:
        file_path = str(uploaded_file)

    if file_path.lower().endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                return file.read()
        except Exception as error:
            return f"[Error reading text file: {error}]"

    if file_path.lower().endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_parts.append(extracted)
            full_text = "\n".join(text_parts).strip()
            if not full_text:
                return "[Note: The PDF was uploaded successfully, but contains no extractable text. It may be a scanned image or non-OCR document.]"
            return full_text
        except Exception as error:
            return f"[Error reading PDF file: {error}]"

    return "Unsupported file type. Please upload a .txt or .pdf file."


def encode_image(uploaded_image):
    if uploaded_image is None:
        return None, None

    if isinstance(uploaded_image, str):
        image_path = uploaded_image
    elif hasattr(uploaded_image, "name"):
        image_path = uploaded_image.name
    else:
        image_path = str(uploaded_image)

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "image/png"

    try:
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")
        return image_base64, mime_type
    except Exception:
        return None, None


def generate_ai_response(prompt, uploaded_file, uploaded_image):
    if not prompt or not prompt.strip():
        if uploaded_file is not None:
            prompt = "Summarize the key information from the uploaded file."
        elif uploaded_image is not None:
            prompt = "Analyze and describe the content of the uploaded image."
        else:
            return "Please enter a prompt before generating a response."

    file_text = extract_file_text(uploaded_file)
    image_base64, image_mime_type = encode_image(uploaded_image)

    prompt_parts = [
        "User prompt:",
        prompt
    ]

    if file_text:
        prompt_parts.extend(
            [
                "\nUploaded file content:",
                file_text[:4000]
            ]
        )

    if uploaded_image is not None:
        prompt_parts.extend(
            [
                "\nImage instruction:",
                "Analyze the uploaded image and include a clear summary of what it contains."
            ]
        )

    final_prompt = "\n".join(prompt_parts)

    try:
        response = requests.post(
            FASTAPI_URL,
            json={
                "prompt": final_prompt,
                "image_base64": image_base64,
                "image_mime_type": image_mime_type
            },
            timeout=90
        )

        response.raise_for_status()
        data = response.json()

        ai_response = data.get(
            "response",
            "No response returned."
        )

        model_used = data.get(
            "model",
            "Unknown model"
        )

        status = data.get(
            "status",
            "Unknown status"
        )

        return f"""
## AI Response

{ai_response}

---

### Response Metadata

- **Model Used:** `{model_used}`
- **Status:** `{status}`
"""

    except requests.exceptions.ConnectionError:
        return """
## Backend Connection Error

The Gradio app could not connect to the FastAPI backend.

Make sure the backend is running with:

```bash
uvicorn fastapi_backend:app --reload
```
"""

    except requests.exceptions.Timeout:
        return """
## Request Timeout

The backend took too long to respond. Try again with a shorter prompt or a smaller file.
"""

    except requests.exceptions.HTTPError as error:
        return f"""
## HTTP Error

The backend returned an error:

{error}
"""

    except Exception as error:
        return f"""
## Unexpected Error

{error}
"""


with gr.Blocks(title="Gradio AI Assistant") as demo:

    gr.Markdown(
        """
        # Gradio AI Assistant with FastAPI Backend

        Enter a prompt, upload a PDF/text file or image, and generate an AI response through a FastAPI backend.
        """
    )

    with gr.Row():

        with gr.Column(scale=1):

            prompt_input = gr.Textbox(
                label="Prompt",
                placeholder="Example: Summarize the uploaded PDF or describe the uploaded image.",
                lines=5
            )

            file_input = gr.File(
                label="Optional File Upload (.pdf or .txt)",
                file_types=[".pdf", ".txt"]
            )

            image_input = gr.Image(
                label="Optional Image Upload",
                type="filepath"
            )

            generate_button = gr.Button(
                "Generate Response",
                variant="primary"
            )

        with gr.Column(scale=1):

            output_markdown = gr.Markdown(
                label="AI Response"
            )

    generate_button.click(
        fn=generate_ai_response,
        inputs=[
            prompt_input,
            file_input,
            image_input
        ],
        outputs=output_markdown
    )

if __name__ == "__main__":
    share_env = os.getenv("GRADIO_SHARE", "False").lower() in ("true", "1", "yes")
    try:
        demo.launch(share=share_env)
    except Exception as exc:
        print(f"Gradio share failed ({exc}), launching locally...")
        demo.launch(share=False)
