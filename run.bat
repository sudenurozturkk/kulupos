@echo off
REM KulüpOS - Windows quick start
where ollama >nul 2>nul || (echo Ollama is not installed: https://ollama.com/download & pause & exit /b 1)
ollama list | findstr /C:"gemma4:e4b" >nul || ollama pull gemma4:e4b
if not exist .venv (python -m venv .venv)
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt
python -m app
