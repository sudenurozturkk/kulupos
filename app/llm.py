"""Thin client for a local Ollama server running Gemma 4.

Nothing in here talks to the internet: every request goes to OLLAMA_URL,
which defaults to the Ollama daemon on this machine.
"""
from __future__ import annotations

import json
import os

import httpx

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
MODEL = os.environ.get("PANO_MODEL", "gemma4:e4b")
NUM_CTX = int(os.environ.get("PANO_NUM_CTX", "8192"))
TIMEOUT = httpx.Timeout(600.0, connect=5.0)


class LLMError(RuntimeError):
    pass


async def health() -> dict:
    """Is Ollama up, and is the model pulled?"""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            r.raise_for_status()
    except httpx.HTTPError:
        return {"ollama": False, "model": MODEL, "model_ready": False}
    names = {m.get("name", "") for m in r.json().get("models", [])}
    ready = MODEL in names or f"{MODEL}:latest" in names
    return {"ollama": True, "model": MODEL, "model_ready": ready}


async def chat(
    messages: list[dict],
    schema: dict | None = None,
    temperature: float = 0.1,
    num_ctx: int = NUM_CTX,
) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "think": False,
        "keep_alive": "30m",
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    if schema is not None:
        payload["format"] = schema  # Ollama structured outputs: grammar-constrained JSON
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
    except httpx.HTTPError as e:
        raise LLMError(f"Ollama'ya ulaşılamadı ({OLLAMA_URL}): {e}") from e
    if r.status_code != 200:
        raise LLMError(f"Ollama {r.status_code}: {r.text[:300]}")
    return r.json()["message"]["content"]


async def chat_json(messages: list[dict], schema: dict, **kw) -> dict:
    raw = await chat(messages, schema=schema, **kw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Grammar-constrained output should always parse, but be defensive.
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end > start:
            return json.loads(raw[start : end + 1])
        raise LLMError(f"Model JSON döndürmedi: {raw[:200]}")
