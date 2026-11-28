param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("1", "2", "3")]
    [string]$Demo
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$module2Env = Join-Path $projectRoot "..\..\Module_2\Demonstration 2\streamlit-ai-streaming\.env"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Environment not found. Create it and install requirements first; see README.md."
}
if (Test-Path -LiteralPath $module2Env) {
    $env:GROQ_ENV_FILE = (Resolve-Path -LiteralPath $module2Env).Path
}
elseif (-not (Test-Path -LiteralPath (Join-Path $projectRoot ".env"))) {
    throw "Module 2 Groq env file not found. Set GROQ_API_KEY in this project's .env instead."
}
$apps = @{
    "1" = @{ Module = "demo1_prompting.main:app"; Port = 8101 }
    "2" = @{ Module = "demo2_structured_extraction.main:app"; Port = 8102 }
    "3" = @{ Module = "demo3_function_routing.main:app"; Port = 8103 }
}
$selected = $apps[$Demo]
Push-Location $projectRoot
try {
    & $python -m uvicorn $selected.Module --host 127.0.0.1 --port $selected.Port --reload
}
finally {
    Pop-Location
}
