#!/usr/bin/env sh
# KulüpOS - macOS / Linux quick start
set -e
command -v ollama >/dev/null || { echo "Ollama is not installed: https://ollama.com/download"; exit 1; }
ollama list | grep -q "gemma4:e4b" || ollama pull gemma4:e4b
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt
python -m app
