# Module 3 FastAPI + Groq extensions

This is a new project built beside the original Module 3 demos. It reuses the Module 2 FastAPI patterns—Pydantic request/response models, a shared Groq client, and routes that call Groq—while adding the three Module 3 concepts. The original Module 2 and Module 3 folders are not edited by this project.

## Project structure

```text
FastAPI_Groq_Extensions/
├── shared/                         # Groq key/model config and ShopEase policy
├── demo1_prompting/                # Compare three prompting strategies
├── demo2_structured_extraction/    # Extract and validate a support ticket
├── demo3_function_routing/         # Choose a tool, run a mock action, reply
├── requirements.txt
├── start_demo.ps1
└── .env.example
```

Each demo is its own FastAPI app with Swagger UI, so learners can call the API at `/docs` and inspect validated request/response schemas.

## Install once

From this project folder in PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The start script reuses the Groq key in the existing Module 2 Demo 2 `.env` without copying or printing it. If you prefer a project-local key, copy `.env.example` to `.env` and add `GROQ_API_KEY`; the project-local setting takes precedence over the external env file.

## Run a demo

In separate PowerShell terminals, from this folder, start whichever demos you want to show. They use separate ports and can run at the same time:

```powershell
.\start_demo.ps1 -Demo 1
.\start_demo.ps1 -Demo 2
.\start_demo.ps1 -Demo 3
```

Then open the corresponding Swagger page:

| Demo | Topic | Swagger UI |
| --- | --- | --- |
| 1 | Zero-shot, few-shot, step-guided prompting | http://127.0.0.1:8101/docs |
| 2 | Structured support-ticket extraction | http://127.0.0.1:8102/docs |
| 3 | Groq tool calling with a mock backend | http://127.0.0.1:8103/docs |

Use **Try it out** in Swagger. Each request schema includes a sample payload.

## Suggested lecture progression

1. Begin with the Module 2 Groq request and FastAPI route learners already know.
2. Demo 1 changes the prompt and measures answers/token use.
3. Demo 2 turns free-form text into a Pydantic-validated object.
4. Demo 3 lets the model select a function, then lets application code execute it and return an observation to the model.

All Demo 3 backend operations are mock examples. No real order, refund, shipment, or escalation system is contacted.
