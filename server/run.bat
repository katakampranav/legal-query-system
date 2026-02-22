@echo off
REM Run script for development mode (Windows)
REM Uses uv to manage environment automatically

setlocal enabledelayedexpansion
setx PYTHONUNBUFFERED 1

REM Install/update dependencies using uv (creates .venv automatically)
echo Installing dependencies with uv...
uv sync

REM Create mock readline module for Windows (Pinecone needs it)
if not exist ".venv\Lib\site-packages\readline.py" (
    echo # Mock readline module for Windows > .venv\Lib\site-packages\readline.py
)

REM Run the application using uv (automatically uses .venv)
echo Starting Legal QA Server...
uv run uvicorn src.app.api:app --host 0.0.0.0 --port 8000

pause
