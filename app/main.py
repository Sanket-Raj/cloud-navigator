from fastapi import FastAPI
from pydantic import BaseModel
from app.chat_engine import process_query

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    result = process_query(req.message)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
