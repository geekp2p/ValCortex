import os, base64, io
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from PIL import Image

OLLAMA = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434").rstrip("/")
TEXT_MODEL = os.getenv("OLLAMA_TEXT_MODEL", "gpt-oss:20b")
VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "llama3.2-vision:11b")

allow_origins = [x.strip() for x in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if x.strip()]

app = FastAPI(title="ValCortex", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    stream: Optional[bool] = False

async def ollama_chat(payload: Dict[str, Any]) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(f"{OLLAMA}/api/chat", json=payload)
        r.raise_for_status()
        return r.json()

def image_to_base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode("utf-8")

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{OLLAMA}/api/tags")
            r.raise_for_status()
        return {"ok": True, "ollama": "ready"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/models")
async def models():
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(f"{OLLAMA}/api/tags")
        r.raise_for_status()
        return r.json()

@app.post("/v1/chat")
async def chat(req: ChatRequest):
    model = req.model or TEXT_MODEL
    payload = {
        "model": model,
        "messages": [m.model_dump() for m in req.messages],
        "stream": bool(req.stream),
    }
    out = await ollama_chat(payload)
    return {"model": model, "response": out}

@app.post("/v1/vision")
async def vision(
    image: UploadFile = File(...),
    prompt: str = Form("Describe this image in Thai."),
    model: Optional[str] = Form(None),
):
    used_model = model or VISION_MODEL
    img_bytes = await image.read()
    try:
        _ = Image.open(io.BytesIO(img_bytes))  # validate image
    except Exception:
        return {"error": "Invalid image"}

    payload = {
        "model": used_model,
        "messages": [{
            "role": "user",
            "content": prompt,
            "images": [image_to_base64(img_bytes)],
        }],
        "stream": False,
    }
    out = await ollama_chat(payload)
    return {"model": used_model, "response": out}

class SimplePrompt(BaseModel):
    prompt: str
    model: Optional[str] = None

@app.post("/v1/simple")
async def simple(req: SimplePrompt):
    payload = {
        "model": req.model or TEXT_MODEL,
        "messages": [{"role":"user","content": req.prompt}],
        "stream": False,
    }
    out = await ollama_chat(payload)
    return {"model": payload["model"], "response": out}
