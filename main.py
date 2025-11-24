from fastapi import FastAPI
from pydantic import BaseModel
import os
import time
import httpx

app = FastAPI(title="Paperpod FastAPI Example")


class ComputeRequest(BaseModel):
    a: float
    b: float


@app.get("/")
async def root():
    return {
        "service": "paperpod-fastapi-example",
        "status": "ok",
        "env": {
            "POD_NAME": os.getenv("POD_NAME", "unknown"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "local"),
        },
    }


@app.post("/compute")
async def compute(req: ComputeRequest):
    """Fake 'useful' endpoint: sum + product + latency."""
    result = {
        "sum": req.a + req.b,
        "product": req.a * req.b,
    }
    # fake latency / work
    time.sleep(0.3)
    return result


@app.get("/fetch")
async def fetch_example(url: str = "https://example.com"):
    """Show outbound HTTP works inside the container."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(url)
        return {
            "url": url,
            "status_code": r.status_code,
            "content_length": len(r.text),
        }