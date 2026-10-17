from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from chronnosai_a0m import cpu_percent, virtual_memory

app = FastAPI(title="ChronnosAI A0M API", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    platform: str


@app.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok", platform="android-termux")


@app.get("/status")
def status() -> dict:
    vm = virtual_memory() or {"total": None, "available": None, "used": None, "free": None}
    return {
        "cpu_percent": cpu_percent(0.1),
        "memory": vm,
        "service": "chronnosai_a0m",
    }


@app.get("/")
def root() -> dict:
    return {"message": "ChronnosAI A0M API is running."}
