# Module 3 demos

## Groq Jupyter notebooks

These three notebooks cover the Module 3 concepts using Groq directly. They do not require OpenRouter or Claude.

| Demo | Notebook | Concept |
| --- | --- | --- |
| 1 | `Demonstration1/Demo1_Groq_Prompting_Strategies.ipynb` | Compare zero-shot, few-shot, and step-guided prompting |
| 2 | `Demonstration2/Demo2_Groq_Structured_Extraction.ipynb` | Extract and validate a structured customer support ticket |
| 3 | `Demonstration3/Demo3_Groq_Function_Routing.ipynb` | Route a customer request to a mock backend tool and draft a reply |

Install the notebook dependencies into the Python interpreter you will use as the notebook kernel:

```powershell
py -m pip install -r .\Module_3\requirements-groq-notebooks.txt
```

Open a notebook in VS Code and select the Python interpreter where `groq` and `ipykernel` are installed. The notebooks also run in offline preview mode without a key, so the lesson flow can be shown without making API calls.

For live model calls, copy `.env.example` to `.env` in this folder and replace `your_groq_key_here` with your Groq API key. The notebooks read that local file or the `GROQ_API_KEY` environment variable. `.env` is ignored by Git; do not put a key in a notebook or commit it. The notebooks use Groq model `openai/gpt-oss-120b`.

## FastAPI extensions

The separate [`FastAPI_Groq_Extensions`](FastAPI_Groq_Extensions/README.md) project extends the Module 2 FastAPI pattern with the same three Module 3 concepts. Each demo has a FastAPI backend and an interactive Swagger page. Start a demo with its `start_demo.ps1` script, then open the `/docs` URL listed in that project's README. The key is read from the configured Module 2 `.env` file or a project-local `.env`; it is not stored in the source files.

## Existing Streamlit apps

The original Streamlit app source folders still use Claude through OpenRouter and can be launched using their own instructions. The Groq notebooks and FastAPI extensions are separate implementations.
